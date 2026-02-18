from datetime import timedelta
import uuid
from typing import Optional
from app.core import security
from app.core.config import settings
from app.core.redis import redis_client
from app.models.schemas.auth import AuthResponse

class TokenService:
    @staticmethod
    async def create_tokens(subject: str, scopes: list[str] = []) -> AuthResponse:
        # Access Token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            subject=subject, expires_delta=access_token_expires
        )
        
        # Refresh Token (Opaque or JWT, here using Opaque for easy revocation)
        refresh_token = str(uuid.uuid4())
        refresh_expires_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        
        # Store Refresh Token in Redis with link to Subject
        # Key: "refresh:{token}" -> "subject"
        await redis_client.setex(
            f"refresh:{refresh_token}", 
            refresh_expires_seconds, 
            subject
        )
        
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token
        )

    @staticmethod
    async def refresh_token(refresh_token: str) -> Optional[AuthResponse]:
        # Check validity and rotation
        key = f"refresh:{refresh_token}"
        subject = await redis_client.get(key)
        
        if not subject:
            return None
            
        # Revoke used refresh token (Rotation)
        await redis_client.delete(key)
        
        # Issue new pair
        return await TokenService.create_tokens(subject=subject)

    @staticmethod
    async def revoke_token(refresh_token: str) -> None:
        await redis_client.delete(f"refresh:{refresh_token}")
