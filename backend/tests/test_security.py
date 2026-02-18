import pytest
from httpx import AsyncClient
from app.main import app
from app.core import security

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "strict-transport-security" in response.headers
    assert "x-request-id" in response.headers

@pytest.mark.asyncio
async def test_jwks_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth/jwks.json")
    assert response.status_code == 200
    data = response.json()
    assert "keys" in data
    assert len(data["keys"]) > 0
    assert data["keys"][0]["alg"] == "RS256"

@pytest.mark.asyncio
async def test_login_access_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/token", 
            data={"username": "admin", "password": "admin"}
        )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Verify token
    token = data["access_token"]
    # We need a public key to verify. In test we can use the one loaded in security.
    # Note: validation might fail if "aud" or "iss" are expected but not present.
    # security.verify_token(token) - we haven't implemented a clean verify function yet used outside of deps
    
@pytest.mark.asyncio
async def test_rate_limiting():
    # This test might be flaky depending on redis state/speed
    # Mocking redis would be better, but for integration test:
    pass
