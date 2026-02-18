import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy import ForeignKey, String, Integer, DateTime
from app.models.base import Base

class OTPChallenge(Base):
    __tablename__ = "otp_challenges"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[str] = mapped_column(String, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    otp_hash: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    
class DeviceSession(Base):
    __tablename__ = "device_sessions"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    device_fingerprint: Mapped[str] = mapped_column(String, index=True)
    refresh_token_hash: Mapped[str] = mapped_column(String, unique=True)
    user_agent: Mapped[str] = mapped_column(String)
    ip_address: Mapped[str] = mapped_column(String) # Consider using INET type in production
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    user: Mapped["User"] = relationship("User", back_populates="device_sessions")
