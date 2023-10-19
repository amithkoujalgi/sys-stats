import os
from pathlib import Path

import eventlet
import socketio

import sys_stats
from sys_stats.api import stats

static_path = os.path.join(Path(sys_stats.__file__).parent, 'socketio_impl', 'static')

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': f"{static_path}/",
})


@sio.event
def connect(sid, environ):
    print('Client connected:', sid)


@sio.on('list_processes')
def list_processes(sid, data):
    sio.emit("process-list", stats.processes(search_keyword=''))
    print('Received message:', data)


@sio.on('list_ports')
def list_ports(sid, data):
    sio.emit("port-list", stats.net_connections())
    print('Received message:', data)


@sio.on('resource_usage')
def resource_usage(sid, data):
    sio.emit("resource-usage", stats.resource_usage())
    print('Received message:', data)


@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8070)), app)
