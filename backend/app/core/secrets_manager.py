from abc import ABC, abstractmethod
import os
from typing import Optional
from app.core.config import settings

class SecretsProvider(ABC):
    @abstractmethod
    def get_secret(self, key: str) -> str:
        pass

class EnvironmentSecretsProvider(SecretsProvider):
    def get_secret(self, key: str) -> str:
        """
        Retrieves a secret from environment variables or settings.
        Configuration keys in settings take precedence if they match known settings.
        Otherwise falls back to os.environ.
        """
        # Map generic keys to specific settings attributes if needed
        if key == "ENCRYPTION_KEY":
            return settings.ENCRYPTION_KEY
        if key == "SECRET_KEY":
            return settings.SECRET_KEY
        
        return os.environ.get(key, "")

# Factory or Singleton to get the configured provider
def get_secrets_provider() -> SecretsProvider:
    # In the future, this can switch based on settings.SECRETS_PROVIDER_TYPE
    return EnvironmentSecretsProvider()

secrets_provider = get_secrets_provider()
