import logging
import time
import traceback
from sys import platform

import psutil
from humanfriendly import format_timespan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def processes():
    processlist = []
    for process in psutil.process_iter():
        process: psutil.Process
        try:
            processlist.append(
                dict(
                    name=process.name(),
                    pid=process.pid,
                    status=process.status(),
                    create_time=process.create_time(),
                    running_since=format_timespan(time.time() - process.create_time()),
                    parent=process.parent().name(),
                    cmdline=' '.join(process.cmdline()),
                    username=process.username(),
                    memory_usage=round(process.memory_info().rss / (1024 * 1024), 2),
                    cpu_usage=round(process.cpu_percent(), 2)
                )
            )
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
            active=round(psutil.virtual_memory().active / (1024 * 1024), 2),
            inactive=round(psutil.virtual_memory().inactive / (1024 * 1024), 2),
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


def net_connections():
    if platform == "darwin":
        logger.error('net-connections API unsupported on Mac OSX')
        return []
    elif platform == "win32":
        logger.error('net-connections API unsupported on Windows')
        return []
    elif platform == "linux" or platform == "linux2":
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
    else:
        logger.error(f'Unknown platform - {platform}')
