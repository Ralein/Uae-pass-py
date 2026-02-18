import secrets
import string
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.auth import OTPChallenge
from app.core import security
from app.core.config import settings

class OTPService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _generate_code(self, length=6) -> str:
        return ''.join(secrets.choice(string.digits) for _ in range(length))

    async def create_otp(self, user_id) -> OTPChallenge:
        code = self._generate_code()
        hashed_code = security.hash_otp(code)
        
        challenge = OTPChallenge(
            user_id=user_id,
            request_id=str(uuid.uuid4()),
            otp_hash=hashed_code,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
            attempts=0
        )
        self.session.add(challenge)
        return challenge, code

    async def verify_otp(self, request_id: str, code: str) -> bool:
        stmt = select(OTPChallenge).where(OTPChallenge.request_id == request_id)
        result = await self.session.execute(stmt)
        challenge = result.scalar_one_or_none()
        
        if not challenge:
            return False
            
        if challenge.expires_at < datetime.now(timezone.utc):
            return False
            
        if challenge.attempts >= 3:
            # Locked out
            return False
            
        hashed_input = security.hash_otp(code)
        if hashed_input != challenge.otp_hash:
            challenge.attempts += 1
            return False
            
        return True
