from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.services.otp import OTPService
from app.models.schemas.auth import OTPRequest, OTPVerify
from app.core.limiter import RateLimiter

router = APIRouter()

@router.post("/generate", dependencies=[Depends(RateLimiter(requests=3, window=60))])
async def generate_otp(
    request: OTPRequest,
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    # In a real app, we look up the user by identifier First.
    # user = await UserService(db).get_by_identifier(request.identifier)
    # if not user: ...
    
    # For scaffold, assume we find a user_id based on identifier (or Create a dummy one for testing OTP flow separately)
    import uuid
    dummy_user_id = uuid.uuid4() 
    
    service = OTPService(db)
    challenge, code = await service.create_otp(dummy_user_id)
    await db.commit()
    
    # In production: Send SMS/Email via NotificationService
    # In dev: Return code or log it
    
    return {
        "message": "OTP sent", 
        "request_id": challenge.request_id,
        "dev_code": code # REMOVE IN PROD
    }

@router.post("/verify", dependencies=[Depends(RateLimiter(requests=5, window=60))])
async def verify_otp(
    verify_in: OTPVerify,
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    service = OTPService(db)
    is_valid = await service.verify_otp(verify_in.request_id, verify_in.otp)
    await db.commit()
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        
    return {"status": "verified", "message": "OTP correct"}
