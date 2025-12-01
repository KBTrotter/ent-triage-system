from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    JWT_SECRET_KEY: str = "access-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: list = ["http://localhost:5173"]
    
    DB_USER: str
    DB_PW: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    DEBUG: bool = False
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from components"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()