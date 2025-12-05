from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "User" 
    __table_args__ = {"schema": "ent"}

    userID: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    firstName: str
    role: str
    passwordHash: str
    lastLogin: datetime = Field(default_factory=datetime.utcnow)
    lastName: str
    email: str = Field(unique=True)

    refreshTokens: List["RefreshToken"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"primaryjoin": "User.userID==RefreshToken.user_id"} # specify join condition, only way this was able to work
    )

class RefreshToken(SQLModel, table=True):
    __tablename__ = "RefreshToken" 
    __table_args__ = {"schema": "ent"} 

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    token: str = Field(unique=True, nullable=False)
    expires_at: datetime
    revoked: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="ent.User.userID")

    user: Optional["User"] = Relationship(back_populates="refreshTokens")