import pytest
import uuid
from httpx import AsyncClient
from app.main import app
from app.services.token_service import TokenService

@pytest.mark.asyncio
async def test_oidc_config():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth/.well-known/openid-configuration")
    assert response.status_code == 200
    data = response.json()
    assert "issuer" in data
    assert "authorization_endpoint" in data

@pytest.mark.asyncio
async def test_refresh_flow():
    # Mock Token Creation
    auth_data = await TokenService.create_tokens("user123")
    refresh_token = auth_data.refresh_token.replace('bearer ', '') # schema might have minimal string
    # Actually schema has it as field, let's just use what create_tokens returns
    
    # Refresh
    new_tokens = await TokenService.refresh_token(auth_data.refresh_token)
    assert new_tokens is not None
    assert new_tokens.access_token != auth_data.access_token
    
    # Replay (should fail)
    retry = await TokenService.refresh_token(auth_data.refresh_token)
    assert retry is None
