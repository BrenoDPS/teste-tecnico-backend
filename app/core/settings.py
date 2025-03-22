from pydantic_settings import BaseSettings
from typing import List

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
    BACKEND_CORS_ORIGINS: List[str] = ["*"]  # Em produção, especifique os domínios permitidos
    
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
            "ACCESS_TOKEN_EXPIRE_MINUTES": "30"
        }

settings = Settings()        
