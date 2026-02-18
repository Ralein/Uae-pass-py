import pytest
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.models import Base, User, Credentials
from app.core.encryption import cipher_suite
from sqlalchemy import text, select

# Use a separate test database or the main one if comfortable
# For simplicity in this scaffold, we use the main one but clean up
DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

@pytest.fixture
async def db_session():
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
        
    await engine.dispose()

@pytest.mark.asyncio
async def test_user_creation_and_encryption(db_session):
    # Create User
    user_id = uuid.uuid4()
    national_id = "784-1234-5678901-1"
    user = User(
        id=user_id,
        national_id=national_id,
        email="test@example.com",
        phone="+971500000000",
        full_name="Test User"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    # Verify Decryption on load
    assert user.national_id == national_id
    
    # Verify Encryption in DB (using raw SQL to see ciphertext)
    result = await db_session.execute(
        text("SELECT national_id FROM users WHERE id = :id"), 
        {"id": user_id}
    )
    encrypted_value = result.scalar()
    
    # It should not be the plain text
    assert encrypted_value != national_id.encode('utf-8')
    assert encrypted_value != national_id
    
    # Clean up
    await db_session.delete(user)
    await db_session.commit()

@pytest.mark.asyncio
async def test_credentials_link(db_session):
    user = User(national_id="999", email="c@example.com", phone="999", full_name="Creds Test")
    db_session.add(user)
    await db_session.flush()
    
    creds = Credentials(user_id=user.id, password_hash="hash", pin_hash="pin")
    db_session.add(creds)
    await db_session.commit()
    
    # Verify relationship
    await db_session.refresh(user)
    assert user.credentials is not None
    assert user.credentials.password_hash == "hash"
    
    await db_session.delete(user)
    await db_session.commit()
