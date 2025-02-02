import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from app.main import app

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_package_types(async_client):
    response = await async_client.get("/package_types")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3

@pytest.mark.asyncio
async def test_register_package_and_get_it(async_client):
    package_data = {
        "name": "Test Package",
        "weight": 1.5,
        "type_id": 2,  # Предположим, 2 соответствует "электронике"
        "content_value": 1000.0
    }
    response = await async_client.post("/packages", json=package_data)
    assert response.status_code == status.HTTP_200_OK
    registered = response.json()
    assert "id" in registered
    package_id = registered["id"]

    # Запрос конкретной посылки
    response = await async_client.get(f"/packages/{package_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == package_data["name"]
    assert isinstance(data["type_name"], str)

@pytest.mark.asyncio
async def test_get_packages_with_pagination(async_client):
    response = await async_client.get("/packages", params={"page": 1, "page_size": 10})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
