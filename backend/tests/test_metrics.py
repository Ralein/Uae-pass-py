import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_metrics_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/metrics")
    assert response.status_code == 200
    assert "auth_success_total" in response.text

@pytest.mark.asyncio
async def test_auth_metrics_increment():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Fail login
        await ac.post("/api/v1/auth/token", data={"grant_type": "password", "username": "bad", "password": "bad"})
        
        # Check metrics
        response = await ac.get("/metrics")
        assert 'auth_failure_total{method="password",reason="invalid_creds"}' in response.text
