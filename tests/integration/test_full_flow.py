import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from backend.app.main import app


@pytest.mark.asyncio
async def test_full_api_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        health = await client.get("/health")
        assert health.status_code == 200

        docs = await client.get("/api/openapi.json")
        assert docs.status_code == 200

        register = await client.post("/api/auth/register", json={
            "username": "integration_user",
            "password": "securepassword123",
        })
        assert register.status_code in (201, 400)

        login = await client.post("/api/auth/login", json={
            "username": "integration_user",
            "password": "securepassword123",
        })
        assert login.status_code == 200

        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        messages = await client.get("/api/messages/", headers=headers)
        assert messages.status_code == 200

        media = await client.get("/api/media/", headers=headers)
        assert media.status_code == 200

        stories = await client.get("/api/stories/", headers=headers)
        assert stories.status_code == 200

        autoreply = await client.get("/api/autoreply/", headers=headers)
        assert autoreply.status_code == 200

        stats = await client.get("/api/statistics/account", headers=headers)
        assert stats.status_code == 200

        system = await client.get("/api/system/health")
        assert system.status_code == 200

        stop = await client.post("/api/system/emergency-stop", json={"stop_all": True})
        assert stop.status_code == 200
