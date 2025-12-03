from typing import Annotated, Generator
from fastapi import Depends
from sqlmodel import Session
from app.core.database import engine

def get_db() -> Generator[Session, None, None]:
    """Database session dependency"""
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]