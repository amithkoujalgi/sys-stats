import logging
import time

import psutil
from fastapi import APIRouter
from humanfriendly import format_timespan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/processes")
def processes():
    processlist = []
    for process in psutil.process_iter():
        process: psutil.Process
        try:
            processlist.append(dict(
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
            ))
        except Exception as e:
            print(f'Could not add process - {process.name()}. Error: {e}')
    processlist = sorted(processlist, key=lambda x: x['cpu_usage'], reverse=True)
    return processlist


@router.get("/resource-usage")
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


def get_open_ports():
    psutil.net_connections(kind='inet')
    open_ports = []
    for conn in psutil.net_connections(kind='inet'):
        try:
            port_info = {
                "local_address": f"{conn.laddr.ip}:{conn.laddr.port}",
                "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                "status": conn.status,
                "pid": conn.pid if conn.pid else "N/A",
                "process_name": psutil.Process(conn.pid).name() if conn.pid else "N/A"
            }
            open_ports.append(port_info)
        except Exception as e:
            print(f"couldn't add {conn}")
    return open_ports
