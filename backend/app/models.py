import uuid
from datetime import date, datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Message(SQLModel):
    message: str
    
class Patient(SQLModel, table=True):
    __tablename__ = "Patient"
    __table_args__ = {"schema": "ent"}
    
    patient_id: uuid.UUID = Field(
        primary_key=True,
        sa_column_kwargs={"name": "patientID"}
    )
    first_name: str = Field(sa_column_kwargs={"name": "firstName"})
    last_name: str = Field(sa_column_kwargs={"name": "lastName"})
    dob: date = Field(sa_column_kwargs={"name": "DOB"})
    contact_info: str = Field(sa_column_kwargs={"name": "contactInfo"})
    insurance_info: str = Field(sa_column_kwargs={"name": "insuranceInfo"})
    returning_patient: bool = Field(sa_column_kwargs={"name": "returningPatient"})
    language_preference: str = Field(sa_column_kwargs={"name": "languagePreference"})
    verified: bool

class TriageCaseBase(SQLModel):
    transcript: str
    ai_confidence: Optional[float] = Field(
        default=None, 
        sa_column_kwargs={"name": "AIConfidence"}
    )
    ai_summary: Optional[str] = Field(
        default=None, 
        sa_column_kwargs={"name": "AISummary"}
    )
    status: str = "pending"
    ai_urgency: Optional[str] = Field(
        default=None, 
        sa_column_kwargs={"name": "AIUrgency"}
    )

class TriageCaseCreate(TriageCaseBase):
    patient_id: uuid.UUID

class TriageCaseUpdate(SQLModel):
    transcript: Optional[str] = None
    ai_confidence: Optional[float] = None
    ai_summary: Optional[str] = None
    status: Optional[str] = None
    resolution_reason: Optional[str] = None
    override_summary: Optional[str] = None
    summary_status: Optional[str] = None
    ai_urgency: Optional[str] = None
    override_urgency: Optional[str] = None

class TriageCase(TriageCaseBase, table=True):
    __tablename__ = "TriageCase"
    __table_args__ = {"schema": "ent"}
    
    case_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"name": "caseID"}
    )
    patient_id: uuid.UUID = Field(
        foreign_key="ent.Patient.patientID",
        sa_column_kwargs={"name": "patientID"}
    )
    date_created: date = Field(
        default_factory=date.today,
        sa_column_kwargs={"name": "dateCreated"}
    )
    created_by: Optional[uuid.UUID] = Field(
        default=None,
        sa_column_kwargs={"name": "createdBy"}
    )
    resolution_reason: Optional[str] = Field(
        default=None,
        sa_column_kwargs={"name": "resolutionReason"}
    )
    resolution_timestamp: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"name": "resolutionTimestamp"}
    )
    resolved_by: Optional[uuid.UUID] = Field(
        default=None,
        sa_column_kwargs={"name": "resolvedBy"}
    )
    override_summary: Optional[str] = Field(
        default=None,
        sa_column_kwargs={"name": "overrideSummary"}
    )
    summary_status: Optional[str] = Field(
        default=None,
        sa_column_kwargs={"name": "summaryStatus"}
    )
    override_urgency: Optional[str] = Field(
        default=None,
        sa_column_kwargs={"name": "overrideUrgency"}
    )

class TriageCaseResolve(SQLModel):
    resolution_reason: str

class TriageCasePublic(TriageCaseBase):
    case_id: uuid.UUID
    first_name: str
    last_name: str
    dob: date
    date_created: date
    created_by: Optional[uuid.UUID] = None
    resolution_reason: Optional[str] = None
    resolution_timestamp: Optional[datetime] = None
    resolved_by: Optional[uuid.UUID] = None
    override_summary: Optional[str] = None
    summary_status: Optional[str] = None
    override_urgency: Optional[str] = None

class TriageCasesPublic(SQLModel):
    data: list[TriageCasePublic]
    count: int