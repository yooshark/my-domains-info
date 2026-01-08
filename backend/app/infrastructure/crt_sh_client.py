from typing import Any

from app.core.settings import CrtShClientSettings
from app.infrastructure.base import BaseRequestsClient


class CrtShClient(BaseRequestsClient):
    def __init__(self, cfg: CrtShClientSettings):
        self.base_url = cfg.BASE_URL
        self.timeout = cfg.TIMEOUT

    async def get_subdomains(self, domain: str) -> dict[str, Any]:
        return await self.get(
            params={
                "q": domain,
                "output": "json",
            },
        )
