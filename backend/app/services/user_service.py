from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas.user import UserCreate
from app.repositories.user_repo import UserRepository
from app.models.user import User

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def register_user(self, data: UserCreate) -> User:
        # Logic to check existing user (needs blind index or similar)
        # For now, just create
        user = await self.repo.create(data)
        await self.session.commit()
        await self.session.refresh(user)
        return user
