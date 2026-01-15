from httpx import AsyncClient


class TestHealthCheckRoute:
    async def test_health_check_returns_true(self, api_client: AsyncClient) -> None:
        resp = await api_client.get("/api/utils/health-check/")
        assert resp.status_code == 200
        assert resp.json() is True
