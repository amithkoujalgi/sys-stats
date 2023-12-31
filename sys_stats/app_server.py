import os
from pathlib import Path

import eventlet
import socketio

import sys_stats
from sys_stats.api import stats

static_path = os.path.join(Path(sys_stats.__file__).parent, 'static')

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': f"{static_path}/",
})


@sio.event
def connect(sid, environ):
    print('Client connected:', sid)


@sio.on('list_processes')
def list_processes(sid, data):
    search_keyword = data['search_keyword']
    sio.emit("process-list", stats.processes(search_keyword=search_keyword))


@sio.on('list_ports')
def list_ports(sid, data):
    search_keyword = data['search_keyword']
    sio.emit("port-list", stats.net_connections(search_keyword))


@sio.on('resource_usage')
def resource_usage(sid, data):
    sio.emit("resource-usage", stats.resource_usage())


@sio.on('kill_process')
def kill_process(sid, data):
    _pid_to_kill = int(data['process_id'])
    sio.emit("process-kill-status", {
        "status": stats.kill_process_by_pid(_pid_to_kill),
        "pid": _pid_to_kill
    })


@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)


if __name__ == "__main__":
    HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    PORT = int(os.getenv("SERVER_PORT", 8070))
    # noinspection PyUnresolvedReferences
    eventlet.wsgi.server(eventlet.listen((HOST, PORT)), app)
