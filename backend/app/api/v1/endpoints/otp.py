from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.services.otp import OTPService
from app.services.audit_service import AuditService
from app.models.schemas.auth import OTPRequest, OTPVerify
from app.core.limiter import RateLimiter
from app.core.metrics import OTP_GENERATED, OTP_VERIFIED, OTP_FAILED
from app.core.notification import get_notification_provider

router = APIRouter()

@router.post("/generate", dependencies=[Depends(RateLimiter(requests=3, window=60))])
async def generate_otp(
    otp_in: OTPRequest,
    request: Request,
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
    
    # Audit
    audit = AuditService(db)
    await audit.log_event(
        event_type="OTP_GENERATED", 
        actor_id=str(dummy_user_id), 
        ip_address=request.client.host if request.client else "unknown",
        meta={"identifier": otp_in.identifier}
    )
    
    OTP_GENERATED.inc()
    await db.commit()
    
    # Send Notification
    notifier = get_notification_provider()
    # Assuming identifier is phone for now, or determining based on format
    # For MVP we treat identifier as recipient
    await notifier.send_sms(otp_in.identifier, f"Your OTP is: {code}")
    
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
        OTP_FAILED.inc()
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        
    OTP_VERIFIED.inc()
    return {"status": "verified", "message": "OTP correct"}
