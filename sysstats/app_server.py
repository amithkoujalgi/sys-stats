import asyncio
import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import sysstats
from sysstats.routes import stats

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

templates_path = os.path.join(Path(sysstats.__file__).parent, 'templates')
app.mount("/static", StaticFiles(directory=templates_path), name="static")
templates = Jinja2Templates(directory=templates_path)

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


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {
        "request": request,
        "title": "Sys Stats",
        "message": "Sys Stats",
        "processes": stats.processes()
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/stats", response_class=HTMLResponse)
async def get_stats(request: Request):
    context = {
        "request": request,
        "title": "Sys Stats",
        "message": "Sys Stats",
        "stats": stats.resource_usage()
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/ports", response_class=HTMLResponse)
async def get_net_connections(request: Request):
    context = {
        "request": request,
        "title": "Sys Stats",
        "message": "Sys Stats",
        "ports": stats.net_connections()
    }
    return templates.TemplateResponse("index.html", context)


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
    logging.info(f"Web UI at: http://{HOST}:{PORT}")
    asyncio.run(server_app.serve())
