from typing import Any, Type
from cryptography.fernet import Fernet
from sqlalchemy.types import TypeDecorator, LargeBinary
from app.core.secrets_manager import secrets_provider

# Initialize Fernet with the key from secrets provider
key = secrets_provider.get_secret("ENCRYPTION_KEY")
cipher_suite = Fernet(key.encode() if len(key) > 10 else Fernet.generate_key())

class EncryptedString(TypeDecorator):
    """EncryptedString column type for SQLAlchemy.
    
    Encrypts data on the way in, decrypts on the way out.
    """
    impl = LargeBinary
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            value = value.encode('utf-8')
        return cipher_suite.encrypt(value)

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is None:
            return None
        return cipher_suite.decrypt(value).decode('utf-8')
