"""Application entrypoint for the unified ENT triage backend.

This module wires up the FastAPI application, configures CORS and
includes all route modules.  It preserves the original structure of
the production backend (Folder A) while adding the AI triage
capabilities from Folder B.  The Redis and LLM settings are loaded
via the shared ``app.core.config`` module.
"""

import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, text

from app.auth.routes import router as auth_routes
from app.routes.triageCase import router as triage_routes
from app.routes.user import router as user_routes
from app.ai.routes import router as ai_routes
from app.core.config import settings
from app.core.dependencies import get_db

# Configure root logger.  In a production deployment this should
# probably be configured by the container or an external logging
# framework but it is included here for completeness.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Instantiate the FastAPI application
app = FastAPI(title="ENT Triage System")

# Configure CORS from the settings.  The list of allowed origins is
# defined in the ``.env`` file and loaded via pydantic settings.  You
# can extend this list to include your front‑end domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers defined in the project.  The order here
# determines how route conflicts are resolved.  AI routes are
# explicitly mounted under the "/ai" prefix to avoid collisions with
# existing endpoints.
app.include_router(auth_routes)
app.include_router(triage_routes)
app.include_router(user_routes)
app.include_router(ai_routes, prefix="/ai", tags=["ai"])


@app.get("/")
def root() -> dict[str, str]:
    """Return a simple message indicating that the backend is running."""
    return {"message": "FastAPI + PostgreSQL Backend Running"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)) -> dict[str, str]:
    """Perform a basic database health check.

    This endpoint attempts to execute a simple SELECT statement
    against the configured database engine.  On success it returns
    ``{"status": "healthy", "database": "connected"}``; otherwise it
    returns an ``unhealthy`` status along with the error message.
    """
    try:
        db.exec(text("SELECT 1"))
        logger.info("Health check: database connected")
        return {"status": "healthy", "database": "connected"}
    except Exception as exc:  # pragma: no cover - error path logging only
        logger.error(f"Health check failed: {exc}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(exc),
        }
