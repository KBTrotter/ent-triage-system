from sqlmodel import SQLModel
from app.core.database import engine

print("Creating tables...")
SQLModel.metadata.create_all(engine)
print("Done.")

