import asyncio
import contextlib
import platform
from typing import Any

import uvicorn
from fastapi import FastAPI

from app.core import di
from app.core.settings import AppSettings


async def main() -> None:
    async with di.container, di.container.context() as context:
        app_settings = await context.resolve(AppSettings)
        app = await context.resolve(FastAPI)

        app_configs: dict[str, Any] = {
            "proxy_headers": True,
            "forwarded_allow_ips": "*",
        }
        if app_settings.DEVELOP:
            app_configs |= app_settings.get_develop_settings()
        else:
            app_configs |= app_settings.get_prod_settings()

        if platform.system() == "Linux":
            app_configs["loop"] = "uvloop"

        config = uvicorn.Config(
            app,
            **app_configs,
        )

        server = uvicorn.Server(config)
        await server.serve()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
