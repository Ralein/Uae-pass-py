import hmac
import hashlib
import json
from app.models.audit import AuditLog
from app.core.secrets_manager import secrets_provider

AUDIT_SECRET = secrets_provider.get_secret("AUDIT_CHAIN_SECRET") or "audit-secret-key"

def sign_audit_entry(entry_data: dict, previous_hash: str) -> str:
    """
    Computes HMAC for an audit entry, chaining it to the previous entry.
    entry_data: dict containing event_type, actor_id, ip_address, metadata, timestamp
    previous_hash: The signature of the previous audit log.
    """
    # Canonicalize data for consistent hashing
    payload = json.dumps(entry_data, sort_keys=True)
    chain_content = f"{previous_hash}{payload}"
    
    signature = hmac.new(
        AUDIT_SECRET.encode(),
        chain_content.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return signature

def verify_audit_chain(current_entry: AuditLog, previous_entry: AuditLog) -> bool:
    """
    Verifies if the current entry's signature matches the computed signature based on previous entry.
    """
    prev_hash = previous_entry.signature if previous_entry else "GENESIS"
    
    # Reconstruct data payload from the model
    # Note: timestamps and serialization must match exactly how it was signed.
    # In a real implementation, we might store the canonical payload used for signing 
    # or ensure strict serialization rules.
    # For now, we assume simple metadata reconstruction.
    
    # This function is a placeholder for the verification logic
    # which requires careful timestamp handling.
    return True 
