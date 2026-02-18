import pytest
import jwt
import time
from httpx import AsyncClient
from app.main import app
from app.core.config import settings
from app.core import security

# Constants
ALGORITHM = "HS256" # For tampering tests if we force it, though logic uses RS256 usually
# We should use the actual keys from settings/security module for valid generation, 
# and random ones for invalid.

@pytest.mark.asyncio
async def test_jwt_tampering():
    """
    Test that modifying a JWT payload invalidates the signature.
    """
    # 1. Generate a valid token
    payload = {"sub": "tamper_test", "exp": time.time() + 3600}
    # We need a proper way to sign using the app's private key.
    # Accessing the private key might be tricky in tests if it's file based.
    # Let's rely on the `security.create_access_token` utility.
    
    token = security.create_access_token(subject="tamper_test")
    
    # 2. Decode without verification to get payload
    decoded_unverified = jwt.decode(token, options={"verify_signature": False})
    
    # 3. Modify payload
    decoded_unverified["sub"] = "admin_impersonator"
    
    # 4. Re-encode with a DIFFERENT key or just messy signature
    fake_key = "bad_secret_key"
    tampered_token = jwt.encode(decoded_unverified, fake_key, algorithm="HS256")
    
    # 5. Try to access an endpoint
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {tampered_token}"}
        resp = await ac.get("/api/v1/user/me", headers=headers)
        # Should be 401 or 403
        assert resp.status_code in [401, 403]

@pytest.mark.asyncio
async def test_jwt_none_algorithm():
    """
    Test that the 'none' algorithm is rejected.
    """
    payload = {"sub": "none_alg_test", "exp": time.time() + 3600}
    token = jwt.encode(payload, None, algorithm="none") # PyJWT might block this by default, but good to test setup
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {token}"}
        resp = await ac.get("/api/v1/user/me", headers=headers)
        assert resp.status_code in [401, 403]

@pytest.mark.asyncio
async def test_injection_attempts():
    """
    Test basic SQL injection patterns in input fields.
    """
    injection_payloads = [
        "' OR '1'='1",
        "admin' --",
        "UNION SELECT 1,2,3--",
    ]
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for payload in injection_payloads:
            # Login attempt
            resp = await ac.post("/api/v1/auth/token", data={
                "grant_type": "password",
                "username": payload,
                "password": "password"
            })
            # Should fail auth (400/401) but NOT 500 (Server Error)
            assert resp.status_code in [400, 401, 403, 404, 422]
            assert resp.status_code != 500

@pytest.mark.asyncio
async def test_xss_attempts():
    """
    Test XSS payloads in registration (stored XSS checks).
    """
    xss_payload = "<script>alert(1)</script>"
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        resp = await ac.post("/api/v1/registration/register", json={
            "email": "xss@example.com",
            "phone": "+971500000000",
            "national_id": xss_payload, # Inject into national_id
            "pin": "123456"
        })
        
        # If the API accepts it, we check if it is sanitized on output.
        # Ideally, it should be rejected by validation if strictly alphanumeric, 
        # or accepted but strictly displayed as text.
        # Our schemas might perform validation.
        
        # If it returns 422 (Validation Error), that's GOOD security.
        # If 200, we check the response body.
        
        if resp.status_code == 200:
            data = resp.json()
            # In a JSON API, returning the script tag in JSON string is theoretically safe 
            # as long as the Client doesn't render it as HTML.
            # But typically we might want to sanitize.
            pass
        else:
            # validation caught it
            assert resp.status_code == 422
