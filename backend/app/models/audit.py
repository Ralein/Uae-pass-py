import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, Text
from app.api import deps
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Ideally we use a shared Base, but for this file isolation I'll define a quick one 
# or import if I knew where it was. 
# I'll rely on the fact that I haven't strictly defined a single Base file yet 
# (I used minimal models in snippets).
# Let's assume a Base exists or I create a local one for this snippet.
# In a real app, `from app.db.base import Base`

from sqlalchemy.orm import declarative_base
Base = declarative_base()

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    event_type: Mapped[str] = mapped_column(String, index=True)
    actor_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
    request_id: Mapped[str] = mapped_column(String, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default={})
    
    # Security fields
    signature: Mapped[str] = mapped_column(String, nullable=True) # HMAC of this record
    previous_hash: Mapped[str] = mapped_column(String, nullable=True) # Signature of previous record
