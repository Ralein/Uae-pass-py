from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.core.config import settings
from app.services.token_service import TokenService
from app.core import security

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/.well-known/openid-configuration")
async def oidc_configuration():
    return {
        "issuer": settings.OIDC_ISSUER,
        "authorization_endpoint": f"{settings.OIDC_ISSUER}{settings.API_V1_STR}/auth/authorize",
        "token_endpoint": f"{settings.OIDC_ISSUER}{settings.API_V1_STR}/auth/token",
        "userinfo_endpoint": f"{settings.OIDC_ISSUER}{settings.API_V1_STR}/auth/userinfo",
        "jwks_uri": f"{settings.OIDC_ISSUER}{settings.API_V1_STR}/auth/jwks.json",
        "response_types_supported": ["code", "token", "id_token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["RS256"],
        "scopes_supported": ["openid", "profile", "email", "phone"]
    }

from app.services.risk_service import RiskService, RiskAction
from app.models.schemas.risk import AuthContext
from app.core.limiter import RateLimiter

@router.post("/token", dependencies=[Depends(RateLimiter(requests=10, window=60))])
async def token_endpoint(request: Request):
    # Simplified handling for multiple grant types
    # In production, strictly parse form data according to spec
    form = await request.form()
    grant_type = form.get("grant_type")
    
    # Extract Context
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    # Fingerprint would typically come from a header or cookie set by frontend SDK
    fingerprint = request.headers.get("x-device-fingerprint", "unknown")
    
    auth_context = AuthContext(
        ip_address=client_ip, 
        user_agent=user_agent, 
        fingerprint=fingerprint,
        user_id=form.get("username") # Tentative, verified after creds check
    )
    
    risk_service = RiskService()
    risk_assessment = await risk_service.assess_risk(auth_context)
    
    if risk_assessment.action == RiskAction.BLOCK:
        raise HTTPException(status_code=403, detail="Login blocked due to high risk")
    
    # If STEP_UP, we might return a specific error or challenge. 
    # For OIDC, we might require 'acr_values' to be met.
    # For now, let's just log or warn in this simple flow.
    # if risk_assessment.action == RiskAction.STEP_UP: ... 
    
    # ... Continue with Authentication ...
    
    if grant_type == "password":
        # Handled by existing endpoint or logic here
        # For now, we reuse standard login logic or call service
        username = form.get("username")
        password = form.get("password")
        # Validate User (Mocked for now as we did in Phase 2, or use UserService)
        if username == "admin" and password == "admin":
             # Record Success for Risk Engine (Learn IP)
             await risk_service.record_success(auth_context)
             return await TokenService.create_tokens(subject=username)
        raise HTTPException(status_code=400, detail="Invalid credentials")
        
    elif grant_type == "refresh_token":
        refresh_token = form.get("refresh_token")
        new_tokens = await TokenService.refresh_token(refresh_token)
        if not new_tokens:
             raise HTTPException(status_code=400, detail="Invalid refresh token")
        return new_tokens
        
    raise HTTPException(status_code=400, detail="Unsupported grant type")

@router.get("/userinfo")
async def userinfo(token: str = Depends(oauth2_scheme)):
    # Verify token
    try:
        payload = security.verify_token_claims(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    return {
        "sub": payload.get("sub"),
        "name": "Test User", # Fetch from DB
        "email": "test@example.com"
    }

@router.post("/revoke")
async def revoke_token(request: Request):
    form = await request.form()
    token = form.get("token")
    if token:
        await TokenService.revoke_token(token)
    return {"status": "ok"}
