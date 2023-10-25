#!/usr/bin/env python
import argparse
import logging
import os
from pathlib import Path

import eventlet

import sys_stats
from sys_stats.app_server import app


def main():
    parser = argparse.ArgumentParser(description="Start sys-stats server")
    parser.add_argument("operation", type=str, help="Operation to perform. [start]/[version]")
    parser.add_argument("--port", "-p", type=int, help="Override the default port ().")

    args = parser.parse_args()

    operation = args.operation
    port = args.port

    if operation == 'start':
        if port:
            _start(port=port)
        _start()
    elif operation == 'version':
        _version()
    else:
        print(f'Invalid operation - {operation}')


def _start(port: int = 8070):
    host: str = "0.0.0.0"
    logging.info(f"Starting web server on {host}:{port}")
    logging.info(f"Web UI at: http://{host}:{port}")
    eventlet.wsgi.server(eventlet.listen((host, port)), app)


def _version():
    static_path = os.path.join(Path(sys_stats.__file__).parent.parent)
    pkgs = os.listdir(static_path)
    for p in pkgs:
        if 'sys_stats-' in p:
            ver = p.replace('sys_stats-', '').replace('.dist-info', '')
            print(ver)


if __name__ == "__main__":
    main()
