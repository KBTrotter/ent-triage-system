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

import uuid
from datetime import date, datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Message(SQLModel):
    message: str

# ============= PATIENT MODELS =============
class PatientBase(SQLModel):
    firstName: str
    lastName: str
    DOB: Optional[date] = None
    contactInfo: Optional[str] = None
    insuranceInfo: Optional[str] = None
    returningPatient: bool = False
    languagePreference: Optional[str] = None
    verified: bool = False

class Patient(PatientBase, table=True):
    __tablename__ = "Patient"
    __table_args__ = {"schema": "ent"}
    
    patientID: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

class PatientUpdate(SQLModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    DOB: Optional[date] = None
    contactInfo: Optional[str] = None
    insuranceInfo: Optional[str] = None
    returningPatient: Optional[bool] = None
    languagePreference: Optional[str] = None
    verified: Optional[bool] = None

# ============= TRIAGE CASE MODELS =============
class TriageCaseBase(SQLModel):
    transcript: Optional[str] = None
    AIConfidence: Optional[float] = None
    AISummary: Optional[str] = None
    status: str = "pending"
    AIUrgency: Optional[str] = None
    clinicianSummary: Optional[str] = None
    overrideSummary: Optional[str] = None
    summaryStatus: Optional[str] = None
    overrideUrgency: Optional[str] = None

class TriageCase(TriageCaseBase, table=True):
    __tablename__ = "TriageCase"
    __table_args__ = {"schema": "ent"}
    
    caseID: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    patientID: uuid.UUID = Field(foreign_key="ent.Patient.patientID")
    dateCreated: date = Field(default_factory=date.today)
    createdBy: Optional[uuid.UUID] = None
    resolutionReason: Optional[str] = None
    resolutionTimestamp: Optional[datetime] = None
    resolvedBy: Optional[uuid.UUID] = None

class TriageCaseCreate(SQLModel):
    patientID: uuid.UUID
    transcript: str
    AIConfidence: Optional[float] = None
    AISummary: Optional[str] = None
    AIUrgency: Optional[str] = None

class TriageCaseUpdate(SQLModel):
    transcript: Optional[str] = None
    status: Optional[str] = None
    overrideSummary: Optional[str] = None
    overrideUrgency: Optional[str] = None
    clinicianSummary: Optional[str] = None
    resolutionReason: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    DOB: Optional[date] = None
    contactInfo: Optional[str] = None
    insuranceInfo: Optional[str] = None
    returningPatient: Optional[bool] = None
    languagePreference: Optional[str] = None
    verified: Optional[bool] = None

class TriageCaseResolve(SQLModel):
    resolutionReason: str

class TriageCasePublic(TriageCaseBase, PatientBase):
    caseID: uuid.UUID
    patientID: uuid.UUID
    dateCreated: date
    createdBy: Optional[uuid.UUID] = None
    resolutionReason: Optional[str] = None
    resolutionTimestamp: Optional[datetime] = None
    resolvedBy: Optional[uuid.UUID] = None

class TriageCasesPublic(SQLModel):
    data: list[TriageCasePublic] 
    count: int