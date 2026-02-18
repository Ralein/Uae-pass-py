import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import ForeignKey, String
from app.models.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type: Mapped[str] = mapped_column(String, index=True)
    actor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Nullable for system events
    ip_address: Mapped[str] = mapped_column(String)
    
    metadata_blob: Mapped[dict] = mapped_column(JSONB)
    
    # Integrity chain
    previous_hash: Mapped[str] = mapped_column(String, nullable=True)
    signature: Mapped[str] = mapped_column(String) # HMAC of this record
    
    user: Mapped["User"] = relationship("User", back_populates="audit_logs")
