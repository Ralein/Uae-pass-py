import pytest
from app.core import security, masking
from app.core.secrets_manager import EnvironmentSecretsProvider
from app.services import audit_monitor

def test_password_hashing():
    pwd = "my_secure_password"
    hashed = security.get_password_hash(pwd)
    assert hashed != pwd
    assert security.verify_password(pwd, hashed)
    assert not security.verify_password("wrong", hashed)

def test_pin_hashing():
    pin = "1234"
    hashed = security.hash_pin(pin)
    assert hashed != pin
    assert security.verify_pin(pin, hashed)

def test_otp_hashing():
    otp = "123456"
    hashed = security.hash_otp(otp)
    assert len(hashed) == 64 # SHA256 hex digest length

def test_masking():
    assert masking.mask_email("test@example.com") == "te***t@example.com"
    assert masking.mask_phone("+971501234567") == "+971***4567"

def test_audit_signature():
    data = {"event": "login"}
    prev_hash = "abc"
    sig = audit_monitor.sign_audit_entry(data, prev_hash)
    assert len(sig) == 64
    
    # Ensure changing data changes signature
    sig2 = audit_monitor.sign_audit_entry({"event": "logout"}, prev_hash)
    assert sig != sig2
