from pydantic import BaseModel
import os

class Settings(BaseModel):
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "access-secret")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: list = ["http://localhost:5173"]

settings = Settings()