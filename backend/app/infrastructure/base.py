from typing import Any

import httpx


class BaseRequestsClient:
    timeout: int
    base_url: str

    async def _request(
        self, method: str, path: str, params: dict[str, Any] | None
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.request(method, path, params=params)
            r.raise_for_status()
            return r.json()

    async def get(
        self, added_path: str = "", params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        path = self.base_url
        if added_path:
            path = f"{path}/{added_path}"
        return await self._request("GET", path, params)

    async def get_ip_info(self, ip: str) -> dict[str, Any]:
        return await self.get(added_path=ip)
