from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistema de Gestão de Garantias"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API para gestão de suppliers, transações e analytics"

    # Banco de dados
    DATABASE_URL: str = "sqlite:///./warranty.db"

    # Segurança
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]

    # Métodos HTTP permitidos
    ALLOWED_METHODS: List[str] = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
    ]

    # Headers permitidos
    ALLOWED_HEADERS: List[str] = [
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
    ]

    # Paginação
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1000

    # Cache (para implementação futura)
    REDIS_URL: str | None = None
    CACHE_EXPIRE_MINUTES: int = 60

    # Logs
    LOG_LEVEL: str = "INFO"

    # Swagger UI
    SWAGGER_UI_OAUTH2_REDIRECT_URL: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

        # Exemplo de variáveis necessárias no .env
        env_example = {
            "DATABASE_URL": "sqlite:///./warranty.db",
            "SECRET_KEY": "your-secret-key-here",
            "ALGORITHM": "HS256",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        }

        @field_validator("SECRET_KEY")
        @classmethod
        def validate_secret_key(cls, v):
            if len(v.encode()) < 32:
                raise ValueError("SECRET_KEY deve ter pelo menos 32 bytes")
            return v


settings = Settings()
