from typing import List, Union, Any
from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "UAE Digital Identity Platform"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "uae_identity_db"
    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str, None] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Union[str, None], info: dict) -> Any:
        if isinstance(v, str):
            return v
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URI: Union[RedisDsn, str, None] = None

    @field_validator("REDIS_URI", mode="before")
    @classmethod
    def assemble_redis_connection(cls, v: Union[str, None], info: dict) -> Any:
        if isinstance(v, str):
            return v
        values = info.data
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_HOST"),
            port=values.get("REDIS_PORT"),
            path=f"/{values.get('REDIS_DB') or '0'}",
        )
    
    # Security
    SECRET_KEY: str = "changeme"  # Fallback/Encryption key
    ENCRYPTION_KEY: str = "change_me_to_a_valid_fernet_key_base64"  # For Field Level Encryption
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    OIDC_ISSUER: str = "http://localhost:8000"  # Changes based on deployment
    
    # Rate Limiting
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Auth
    JWT_PRIVATE_KEY_PATH: str = "certs/private.pem"
    JWT_PUBLIC_KEY_PATH: str = "certs/public.pem"
    
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
