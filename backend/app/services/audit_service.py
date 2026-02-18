import json
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.audit import AuditLog
from app.core import masking
from app.services.audit_monitor import sign_audit_entry

class AuditService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_event(
        self, 
        event_type: str, 
        actor_id: str = None, 
        ip_address: str = None, 
        request_id: str = None, 
        meta: dict = {}
    ):
        # 1. Mask PII in metadata
        masked_meta = self._mask_metadata(meta)
        
        # 2. Get previous hash (for chaining)
        # Verify if we need strict serialization here.
        # This is a potential bottleneck. In high throughput, use a buffered queue or redis for previous hash.
        # For this implementation, we query DB.
        stmt = select(AuditLog).order_by(desc(AuditLog.timestamp)).limit(1)
        result = await self.session.execute(stmt)
        prev_log = result.scalar_one_or_none()
        prev_hash = prev_log.signature if prev_log else "GENESIS"
        
        # 3. Create Record
        log_entry = AuditLog(
            event_type=event_type,
            actor_id=actor_id,
            ip_address=ip_address,
            request_id=request_id,
            metadata_json=masked_meta,
            previous_hash=prev_hash
        )
        
        # 4. Sign
        # Prepare data for signing
        sign_data = {
            "event": event_type,
            "actor": actor_id,
            "ip": ip_address,
            "rid": request_id,
            "meta": masked_meta,
            "ts": datetime.now(timezone.utc).isoformat() # Approx, or use fixed
        }
        # In real logic, we'd use the exact internal timestamp of the object
        # Since we haven't flushed, we can't get DB-generated timestamp easily unless we set it manually
        # Let's reuse the default or set it
        # Setting it manually for consistency
        log_entry.timestamp = datetime.now(timezone.utc)
        sign_data["ts"] = log_entry.timestamp.isoformat()
        
        signature = sign_audit_entry(sign_data, prev_hash)
        log_entry.signature = signature
        
        self.session.add(log_entry)
        # We usually commit here or let caller commit. 
        # For audit, we often want immediate commit to ensure trace.
        await self.session.commit()
        
    def _mask_metadata(self, meta: dict) -> dict:
        new_meta = meta.copy()
        if "email" in new_meta:
            new_meta["email"] = masking.mask_email(new_meta["email"])
        if "phone" in new_meta:
            new_meta["phone"] = masking.mask_phone(new_meta["phone"])
        if "national_id" in new_meta:
            new_meta["national_id"] = masking.mask_national_id(new_meta["national_id"])
        return new_meta
