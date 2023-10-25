import logging
import subprocess
import time
import traceback
from sys import platform

import psutil
from humanfriendly import format_timespan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def processes(search_keyword: str):
    processlist = []
    for process in psutil.process_iter():
        process: psutil.Process
        try:
            cmdline = ' '.join(process.cmdline())
            process_dict = dict(
                name=process.name(),
                pid=process.pid,
                status=process.status(),
                create_time=process.create_time(),
                running_since=format_timespan(time.time() - process.create_time()),
                parent=process.parent().name(),
                cmdline=cmdline,
                username=process.username(),
                memory_usage=round(process.memory_info().rss / (1024 * 1024), 2),
                cpu_usage=round(process.cpu_percent(), 2)
            )
            if search_keyword is None or search_keyword.strip() == '':
                processlist.append(process_dict)
            else:
                search_keyword = search_keyword.lower()
                if search_keyword in process.name().lower() or search_keyword in str(
                        process.pid).lower() or search_keyword in cmdline.lower():
                    processlist.append(process_dict)
        except Exception as e:
            logger.error(f'Could not add process - {process.name()}. Error: {e}')
    processlist = sorted(processlist, key=lambda x: x['cpu_usage'], reverse=True)
    return processlist


def resource_usage():
    return dict(
        memory=dict(
            percent=psutil.virtual_memory().percent,
            total=round(psutil.virtual_memory().total / (1024 * 1024), 2),
            used=round(psutil.virtual_memory().used / (1024 * 1024), 2),
            available=round(psutil.virtual_memory().available / (1024 * 1024), 2),
            free=round(psutil.virtual_memory().free / (1024 * 1024), 2),
            # active=round(psutil.virtual_memory().active / (1024 * 1024), 2),
            # inactive=round(psutil.virtual_memory().inactive / (1024 * 1024), 2),
            # wired=round(psutil.virtual_memory().wired / (1024 * 1024), 2),
        ),
        cpu_usage=dict(
            per_cpu=psutil.cpu_percent(interval=0, percpu=True),
            combined=psutil.cpu_percent(interval=0)
        )
    )


def kill_process_by_pid(pid: int) -> bool:
    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait()
        logger.info(f"Process with PID {pid} has been terminated.")
        return True
    except psutil.NoSuchProcess:
        logger.error(f"No process found with PID {pid}.")
        return True
    except Exception as e:
        logger.error(traceback.format_exc())
        return False


def __list_open_ports_with_lsof():
    """
    macOS specific implementation
    :return:
    """
    open_ports = []
    try:
        cmd = ['lsof', '-i', '-n', '-P']
        # print(f'running: {" ".join(cmd)}')
        output = subprocess.check_output(cmd, universal_newlines=True)
        lines = output.split('\n')
        for line in lines[1:]:
            parts = line.split()
            if '(LISTEN)' in parts and ('IPv4' in parts or 'IPv6' in parts):
                pid = int(parts[1])
                process_name = ''
                process_owner = ''
                process_cmd = ''
                if pid > 0:
                    process = psutil.Process(pid=pid)
                    process_name = process.name()
                    process_owner = process.username()
                    process_cmd = ' '.join(process.cmdline())
                listen_port = dict(
                    fd='NA',
                    family='NA',
                    type='NA',
                    laddr=dict(ip=parts[8].rsplit(':', 1)[0], port=parts[8].rsplit(':', 1)[1]),
                    raddr='NA',
                    status='LISTEN',
                    pid=pid,
                    process_name=process_name,
                    process_owner=process_owner,
                    process_cmd=process_cmd
                )
                open_ports.append(listen_port)
    except subprocess.CalledProcessError:
        pass
    return open_ports


def __list_open_ports_netstat_windows():
    """
    Windows specific implementation
    :return:
    """
    open_ports = []
    try:
        output = subprocess.check_output(['netstat', '-ano'], universal_newlines=True)
        lines = output.split('\n')
        for line in lines[4:]:
            parts = line.split()
            if len(parts) > 0 and parts[0] == 'TCP' and 'LISTENING' in parts:
                pid = int(parts[4])
                process_name = ''
                process_owner = ''
                process_cmd = ''
                if pid > 0:
                    process = psutil.Process(pid=pid)
                    process_name = process.name()
                port = parts[1].split(':')[-1]
                host = parts[1].replace(f':{port}', '')
                listen_port = dict(
                    fd='NA',
                    family='NA',
                    type='NA',
                    laddr=dict(ip=host, port=port),
                    raddr='NA',
                    status='LISTEN',
                    pid=pid,
                    process_name=process_name,
                    process_owner=process_owner,
                    process_cmd=process_cmd
                )
                open_ports.append(listen_port)
    except subprocess.CalledProcessError:
        pass
    return open_ports


def __list_open_ports_standard():
    """
    Generic *nix implementation
    :return:
    """
    conns = psutil.net_connections(kind='inet')
    port_mappings = []
    for con in conns:
        process_name = ''
        process_owner = ''
        process_cmd = ''
        if con.pid is not None:
            process = psutil.Process(pid=con.pid)
            process_name = process.name()
            process_owner = process.username()
            process_cmd = ' '.join(process.cmdline())
        port_mappings.append(
            dict(
                fd=con.fd,
                family=con.family,
                type=con.type,
                laddr=con.laddr,
                raddr=con.raddr,
                status=con.status,
                pid='' if con.pid is None else con.pid,
                process_name=process_name,
                process_owner=process_owner,
                process_cmd=process_cmd
            )
        )
    port_mappings = list(filter(lambda port: port['status'] == 'LISTEN', port_mappings))
    return port_mappings


def net_connections(search_keyword: str = ''):
    """
    Lists TCP ports open for listening
    :return:
    """
    _port_list = None
    if platform == "darwin":
        # logger.error('net-connections API unsupported on Mac OSX')
        _port_list = __list_open_ports_with_lsof()
    elif platform == "win32":
        # logger.error('net-connections API unsupported on Windows')
        _port_list = __list_open_ports_netstat_windows()
    elif platform == "linux" or platform == "linux2":
        _port_list = __list_open_ports_standard()
    else:
        logger.error(f'Unknown platform - {platform}')

    if search_keyword == None or search_keyword == '':
        return _port_list

    _port_list_filtered = []
    for p in _port_list:
        if search_keyword in str(p['pid']) or search_keyword in p['laddr']['port'] or search_keyword.lower() in p[
            'process_name'].lower() or search_keyword.lower() in p['process_cmd'].lower():
            _port_list_filtered.append(p)

    return _port_list_filtered
