import contextlib
import logging
from collections.abc import AsyncIterator

import fastapi
from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.adapters.api.main import api_router
from app.core import di, settings

logger = logging.getLogger("app")


@contextlib.asynccontextmanager
async def lifespan(_: fastapi.FastAPI) -> AsyncIterator[None]:
    logger.info("Application is starting...")
    yield
    logger.info("Application has stopped")


def new_server(
    app_cfg: settings.AppSettings,
) -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        debug=app_cfg.DEBUG,
        title=app_cfg.PROJECT_NAME,
        docs_url="/api/docs" if app_cfg.DEBUG else None,
        version=app_cfg.VERSION,
        lifespan=lifespan,
    )

    app.add_middleware(AioInjectMiddleware, container=di.container)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_cfg.ALLOW_ORIGINS,
        allow_origin_regex=app_cfg.ALLOW_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    if not app_cfg.DEVELOP:
        app.mount("/", StaticFiles(directory="static", html=True), name="frontend")
    return app
