from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core import security
from app.core.config import settings

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    # TODO: Authenticate user against DB
    # For Phase 2 scaffolding, we mock authentication
    if form_data.username != "admin" or form_data.password != "admin":
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(
        subject=form_data.username
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.get("/jwks.json")
def get_jwks() -> Any:
    """
    Serve public keys in JWK format for signature verification by other services/gateways.
    """
    # This is a simplified JWK representation. 
    # In production, use a library or properly formatted JWK structure.
    # For now, returning the PEM or a basic JWK-like structure.
    
    # Normally we convert PEM to JWK parameters (n, e)
    # Using python-jose or similar to export JWK
    from jose import jwk
    
    key = jwk.construct(security.PUBLIC_KEY, algorithm="RS256")
    return {"keys": [key.to_dict()]}
