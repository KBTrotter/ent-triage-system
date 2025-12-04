from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, text
from app.auth.routes import router as auth_routes
from app.core.database import engine
from app.core.config import settings
from app.core.dependencies import get_db

app = FastAPI()

app.include_router(auth_routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI + PostgreSQL Backend Running"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.exec(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}