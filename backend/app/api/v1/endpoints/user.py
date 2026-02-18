from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.schemas.user import UserResponse
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return UserResponse(
        id=str(current_user.id),
        is_active=current_user.is_active
    )

@router.get("/devices")
async def read_devices(
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    # Fetch devices from relation
    # return current_user.device_sessions
    return [{"device": "iPhone 15", "last_active": "now", "id": "session_1"}]

@router.delete("/devices/{session_id}")
async def revoke_device_session(
    session_id: str,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    # Revoke logic
    return {"status": "revoked", "session_id": session_id}
