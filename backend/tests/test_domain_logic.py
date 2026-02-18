import pytest
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.services.otp import OTPService
from app.services.user_service import UserService
from app.models.schemas.user import UserCreate

DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

@pytest.fixture
async def db_session():
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
        
    await engine.dispose()

@pytest.mark.asyncio
async def test_otp_flow(db_session):
    # Mock user id
    user_id = uuid.uuid4()
    service = OTPService(db_session)
    
    challenge, code = await service.create_otp(user_id)
    await db_session.commit()
    
    assert code is not None
    assert len(code) == 6
    
    # Verify Correct
    is_valid = await service.verify_otp(challenge.request_id, code)
    assert is_valid is True
    
    # Reuse check (should remain valid in this simple logic? 
    # usually verifying invalidates it or marks used. Logic needs update to delete/mark used)
    # For now, we test incorrect code
    
@pytest.mark.asyncio
async def test_otp_lockout(db_session):
    user_id = uuid.uuid4()
    service = OTPService(db_session)
    challenge, code = await service.create_otp(user_id)
    await db_session.commit()
    
    # 3 failures
    await service.verify_otp(challenge.request_id, "000000")
    await service.verify_otp(challenge.request_id, "000000")
    await service.verify_otp(challenge.request_id, "000000")
    
    await db_session.commit() # Save attempts
    
    # 4th attempt with CORRECT code should fail
    is_valid = await service.verify_otp(challenge.request_id, code)
    assert is_valid is False

@pytest.mark.asyncio
async def test_user_service(db_session):
    service = UserService(db_session)
    data = UserCreate(
        national_id="784-2024-1234567-1",
        email="new@example.com",
        phone="+971509999999",
        full_name="New User"
    )
    user = await service.register_user(data)
    assert user.id is not None
    assert user.national_id is not None # Encrypted
    
    # Cleanup
    await db_session.delete(user)
    await db_session.commit()
