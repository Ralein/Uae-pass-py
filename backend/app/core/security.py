from datetime import datetime, timedelta, timezone
from typing import Any, Union
from pathlib import Path

from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.secrets_manager import secrets_provider
import hashlib

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# Pepper should be stored securely (e.g. Vault), separate from database
PEPPER = secrets_provider.get_secret("SECURITY_PEPPER") or "default_pepper_change_me"

def load_private_key() -> str:
    path = Path(settings.JWT_PRIVATE_KEY_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Private key not found at {path}")
    return path.read_text()

def load_public_key() -> str:
    path = Path(settings.JWT_PUBLIC_KEY_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Public key not found at {path}")
    return path.read_text()

# Cache keys
PRIVATE_KEY = load_private_key()
PUBLIC_KEY = load_public_key()

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token_claims(token: str) -> dict:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.JWTError:
        raise Exception("Could not validate credentials")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # If using pepper, we might need to verify differently if the pepper is involved in the hash generation
    # Passlib handles salt automatically. If we use a pepper, we usually append it to the password.
    if PEPPER:
        plain_password = f"{plain_password}{PEPPER}"
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    if PEPPER:
        password = f"{password}{PEPPER}"
    return pwd_context.hash(password)

def hash_pin(pin: str) -> str:
    # PINS are short, so Argon2 settings might need tuning for speed vs security
    # For now sharing the context, but in prod consider a separate context
    if PEPPER:
        pin = f"{pin}{PEPPER}"
    return pwd_context.hash(pin)

def verify_pin(plain_pin: str, hashed_pin: str) -> bool:
    if PEPPER:
        plain_pin = f"{plain_pin}{PEPPER}"
    return pwd_context.verify(plain_pin, hashed_pin)

def hash_otp(otp: str) -> str:
    # OTPs are short lived, fast hashing (SHA256) with salt/pepper is usually enough 
    # OR create a fast argon2 profile. 
    # Using SHA256 for speed and simplicity for now.
    return hashlib.sha256(f"{otp}{PEPPER}".encode()).hexdigest()

def get_salted_identifier(identifier: str) -> str:
    # Used for looking up encrypted fields by a consistent hash (blind index)
    return hashlib.sha256(f"{identifier}{PEPPER}".encode()).hexdigest()
