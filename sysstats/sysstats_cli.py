#!/usr/bin/env python
import argparse
import asyncio
import logging
import os

import uvicorn

from sysstats.app_server import app


def main():
    parser = argparse.ArgumentParser(description="Start sys-stats server")
    parser.add_argument("operation", type=str, help="Instruction to start.")
    parser.add_argument("--port", "-p", type=int, help="Override the default port ().")

    args = parser.parse_args()

    operation = args.operation
    port = args.port

    if operation == 'start':
        if port:
            _start(port=port)
        _start()
    else:
        print(f'Invalid operation - {operation}')


def _start(port: int = 8070):
    host: str = "0.0.0.0"
    HTTP_GATEWAY_TIMEOUT_SECONDS = int(os.getenv("HTTP_GATEWAY_TIMEOUT_SECONDS", 180))
    logging.info(f"Starting web server on {host}:{port}")
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        timeout_keep_alive=HTTP_GATEWAY_TIMEOUT_SECONDS,
        server_header=False,
    )
    server_app = uvicorn.Server(config=config)
    app.debug = True
    logging.info(f"Web UI at: http://{host}:{port}")
    asyncio.run(server_app.serve())


if __name__ == "__main__":
    main()
