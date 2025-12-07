"""Application configuration using environment variables.

The :class:`Settings` class encapsulates all configurable aspects of
the system, including JWT secrets, database credentials, Redis
connection strings and LLM settings.  Values are loaded from a
``.env`` file if present and can also be provided via the process
environment.  Pydantic's BaseSettings handles type coercion and
validation automatically.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Central configuration for the ENT triage backend."""

    # JWT / authentication settings
    JWT_SECRET_KEY: str = "access-secret"
    JWT_ALGORITHM: str = "HS256"
    REFRESH_SECRET_KEY: str = "refresh-secret"
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    COOKIE_SECURE: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    # Redis configuration.  A valid Redis URL is required for the
    # authentication refresh token store as well as caching AI triage
    # responses.  Example: ``redis://localhost:6379/0``.
    REDIS_URL: str

    # Database credentials.  These values are used to build the
    # SQLAlchemy connection URL for the Postgres database.  By
    # convention the database lives in the ``ent`` schema.
    DB_USER: str
    DB_PW: str
    DB_HOST: str
    DB_PORT: str = "5432"
    DB_NAME: str

    # LLM/Ollama integration settings.  These values configure the
    # base URL of the Ollama server and the specific model to invoke
    # when generating triage results.  Both values may be left blank
    # during development; an error will be raised at runtime if they
    # are missing when a triage request is executed.
    OLLAMA_BASE_URL: str = ""
    OLLAMA_MODEL_NAME: str = ""

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """Construct the full database connection string.

        Using a property here allows the URL to be derived from the
        component pieces defined above.  If you need to support
        different database engines, adjust this string accordingly.
        """
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PW}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instantiate the settings at module import time.  Because BaseSettings
# caches values internally, subsequent imports will reuse the same
# object.  This instance is used throughout the codebase.
settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    """Return a cached copy of the application settings.

    While the ``settings`` object above can be imported directly, this helper
    mirrors the pattern used in the original AI backend.  It allows code to
    obtain a fresh, memoized Settings instance without re-reading the
    environment.  Because :class:`pydantic_settings.BaseSettings` caches
    values internally, repeated calls to this function return the same
    object.
    """
    return settings
