from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.services.user_service import UserService
from app.models.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    service = UserService(db)
    # Check if exists logic should be in service, raising exception if duplicate
    # For now, we assume service handles it or we catch integrity errors
    
    try:
        user = await service.register_user(user_in)
        return UserResponse(
            id=str(user.id),
            is_active=user.is_active,
            # national_id etc are masked/encrypted, maybe don't return them in response
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
