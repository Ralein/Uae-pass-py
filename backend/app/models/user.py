import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, String
from app.models.base import Base
from app.core.encryption import EncryptedString

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Encrypted PII
    national_id: Mapped[str] = mapped_column(EncryptedString, unique=True, index=True)
    email: Mapped[str] = mapped_column(EncryptedString, unique=True, index=True)
    phone: Mapped[str] = mapped_column(EncryptedString, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(EncryptedString)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    credentials: Mapped["Credentials"] = relationship("Credentials", back_populates="user", uselist=False, cascade="all, delete-orphan")
    device_sessions: Mapped[list["DeviceSession"]] = relationship("DeviceSession", back_populates="user", cascade="all, delete-orphan")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="user")
