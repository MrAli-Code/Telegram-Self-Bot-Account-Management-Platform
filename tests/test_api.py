import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from backend.app.main import app


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_api_docs(client):
    response = await client.get("/api/openapi.json")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "testpassword123",
    })
    assert response.status_code in (201, 400)


@pytest.mark.asyncio
async def test_login_user(client):
    await client.post("/api/auth/register", json={
        "username": "logintest",
        "password": "testpassword123",
    })
    response = await client.post("/api/auth/login", json={
        "username": "logintest",
        "password": "testpassword123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_messages_endpoint(client):
    response = await client.get("/api/messages/")
    assert response.status_code in (200, 401)


@pytest.mark.asyncio
async def test_media_endpoint(client):
    response = await client.get("/api/media/")
    assert response.status_code in (200, 401)


@pytest.mark.asyncio
async def test_stories_endpoint(client):
    response = await client.get("/api/stories/")
    assert response.status_code in (200, 401)


@pytest.mark.asyncio
async def test_autoreply_endpoint(client):
    response = await client.get("/api/autoreply/")
    assert response.status_code in (200, 401)


@pytest.mark.asyncio
async def test_statistics_endpoint(client):
    response = await client.get("/api/statistics/account")
    assert response.status_code in (200, 401)


@pytest.mark.asyncio
async def test_system_health_endpoint(client):
    response = await client.get("/api/system/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_emergency_stop_endpoint(client):
    response = await client.post("/api/system/emergency-stop", json={"stop_all": True})
    assert response.status_code == 200
    data = response.json()
    assert "stopped" in data
