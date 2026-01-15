from httpx import AsyncClient


async def test_frontend_mount(api_client: AsyncClient) -> None:
    response = await api_client.get("/")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert "<!doctype html>" in response.text


async def test_404_on_non_frontend_page(api_client: AsyncClient) -> None:
    response = await api_client.get("/some/way")
    assert response.status_code in (200, 404)
    assert response.status_code == 404
