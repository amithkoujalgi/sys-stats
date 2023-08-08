import asyncio
import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.route import stats

app_title = "Sys Stats API"
app_version = "0.0.1"
app_desc = "<p>REST API Playground</p><p><a href='/redoc' target='_blank'>ReDoc</a> | <a href='/docs' target='_blank'>API Docs</a></p>"

origins = os.getenv("CORS_ORIGINS", "*").split(
    " "
)  # provide all the allowed origins as space separated
app = FastAPI(
    title=app_title,
    version=app_version,
    description=app_desc,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # To hide the schema section from swagger docs
        "requestSnippetsEnabled": True,
        "displayRequestDuration": True,
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "syntaxHighlight": True,
        "syntaxHighlight.activate": True,
        "syntaxHighlight.theme": "tomorrow-night",
        "tryItOutEnabled": True,
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    stats.router,
    prefix="/api/stats",
    tags=["stats"],
)

if __name__ == "__main__":
    HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    PORT = int(os.getenv("SERVER_PORT", 8070))
    HTTP_GATEWAY_TIMEOUT_SECONDS = int(os.getenv("HTTP_GATEWAY_TIMEOUT_SECONDS", 180))

    logging.info(f"Starting web server on {HOST}:{PORT}")
    config = uvicorn.Config(
        app,
        host=HOST,
        port=PORT,
        timeout_keep_alive=HTTP_GATEWAY_TIMEOUT_SECONDS,
        server_header=False,
    )
    server_app = uvicorn.Server(config=config)
    app.debug = True
    # noinspection HttpUrlsUsage
    logging.info(
        f"HTTP gateway timeout is set to {HTTP_GATEWAY_TIMEOUT_SECONDS} seconds."
    )
    # noinspection HttpUrlsUsage
    logging.info(f"API Docs at: http://{HOST}:{PORT}/docs")
    # noinspection HttpUrlsUsage
    logging.info(f"ReDoc at: http://{HOST}:{PORT}/redoc")
    asyncio.run(server_app.serve())
