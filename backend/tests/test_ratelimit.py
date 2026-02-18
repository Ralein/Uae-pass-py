import pytest
from httpx import AsyncClient
from app.main import app
from app.core.redis import redis_client

@pytest.mark.asyncio
async def test_otp_rate_limit():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Clear redis first to ensure clean state
        await redis_client.flushdb()
        
        # Limit is 3 per minute
        for _ in range(3):
            resp = await ac.post("/api/v1/otp/generate", json={"identifier": "limit_test"})
            assert resp.status_code == 200
            
        # 4th should fail
        resp = await ac.post("/api/v1/otp/generate", json={"identifier": "limit_test"})
        assert resp.status_code == 429

@pytest.mark.asyncio
async def test_token_rate_limit():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await redis_client.flushdb()
        
        # Limit is 10 per minute
        # We can't easily loop 10 times quickly without mocking internal service calls which might fail on other things
        # But /token requires valid form data usually. 
        # Using a valid request structure but failing auth is enough to trigger rate limit middleware?
        # Yes, middleware runs before handler logic usually, OR dependency runs before handler.
        
        # Sending 11 bad requests
        for _ in range(10):
            await ac.post("/api/v1/auth/token", data={"grant_type": "password", "username": "bad", "password": "bad"})
            
        resp = await ac.post("/api/v1/auth/token", data={"grant_type": "password", "username": "bad", "password": "bad"})
        assert resp.status_code == 429
