import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_registration():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/registration/register", 
            json={
                "national_id": "784-2024-1234567-2",
                "email": "api@example.com",
                "phone": "+971501111111",
                "full_name": "API User"
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

@pytest.mark.asyncio
async def test_otp_flow_api():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Generate
        resp_gen = await ac.post(
            "/api/v1/otp/generate",
            json={"identifier": "784-2024-1234567-2"}
        )
        assert resp_gen.status_code == 200
        data_gen = resp_gen.json()
        request_id = data_gen["request_id"]
        code = data_gen["dev_code"] # extracted from dev response
        
        # Verify
        resp_ver = await ac.post(
            "/api/v1/otp/verify",
            json={"request_id": request_id, "otp": code}
        )
        assert resp_ver.status_code == 200
        assert resp_ver.json()["status"] == "verified"

@pytest.mark.asyncio
async def test_user_me_unauthorized():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/user/me")
    assert response.status_code == 401
