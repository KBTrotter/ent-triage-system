"""API routes for AI‑driven triage operations.

This router exposes endpoints under the ``/ai`` prefix.  The primary
endpoint ``POST /ai/triage`` accepts a call transcript and patient
identifier, invokes the LLM client to generate a triage assessment and
persists the result in the database.  It then returns structured JSON
back to the caller.  A secondary endpoint allows retrieval of a
previously generated triage result by ID.
"""

from __future__ import annotations

import uuid
from datetime import datetime, date
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.dependencies import get_db
from app.models import Patient, Encounter, TriageResult
from .schemas import TriageRequest, TriageResponse
from .llm_client import TriageLLMClient


router = APIRouter(prefix="", tags=["ai"])


@router.post(
    "/triage",
    response_model=TriageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Perform AI triage on a call transcript",
    description="Generate a structured ENT triage assessment from a call transcript and save it.",
)
async def perform_triage(
    request: TriageRequest,
    db: Session = Depends(get_db),
) -> TriageResponse:
    """Process a triage request by invoking the AI model and persisting the result.

    This endpoint validates that the patient exists, creates a new
    ``Encounter`` record, invokes the LLM client to produce a triage
    summary and urgency rating, stores the resulting data in the
    ``TriageResult`` table and returns it to the caller.

    Error responses:

    * ``404 Not Found`` – if the supplied patient ID does not exist.
    * ``400 Bad Request`` – if the call text is empty or missing.
    """
    # Validate call text
    if not request.call_text or request.call_text.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="call_text must not be empty",
        )

    # Look up the patient by primary key; patient_id is a string
    try:
        patient_uuid = uuid.UUID(request.patient_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient_id must be a valid UUID",
        )
    patient = db.get(Patient, patient_uuid)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {request.patient_id} not found",
        )

    # Create an encounter entry; callTimestamp is optional
    encounter = Encounter(
        patientID=patient.patientID,
        callText=request.call_text,
        callTimestamp=request.call_timestamp or datetime.utcnow(),
    )
    db.add(encounter)
    db.commit()
    db.refresh(encounter)

    # Compute patient age (approximate) for LLM context
    age: Any = None
    if hasattr(patient, "DOB") and patient.DOB:
        # Compute age in years; approximate by year difference accounting for month/day
        today = date.today()
        age = today.year - patient.DOB.year - (
            (today.month, today.day) < (patient.DOB.month, patient.DOB.day)
        )

    # Invoke the LLM to generate the triage assessment
    llm_client = TriageLLMClient()
    triage_data = await llm_client.generate_triage(
        call_text=request.call_text,
        patient_context={
            "age": age,
            "first_name": getattr(patient, "firstName", None),
            "last_name": getattr(patient, "lastName", None),
        },
    )

    # Persist the triage result
    triage_result = TriageResult(
        encounterID=encounter.encounterID,
        summary=triage_data.summary,
        urgencyLevel=triage_data.urgency_level,
        urgencyLabel=triage_data.urgency_label,
        recommendedAction=triage_data.recommended_action,
        notes=triage_data.notes,
    )
    db.add(triage_result)
    db.commit()
    db.refresh(triage_result)

    # Build and return the response
    return TriageResponse(
        triage_id=str(triage_result.triageID),
        encounter_id=str(encounter.encounterID),
        patient_id=str(patient.patientID),
        summary=triage_result.summary,
        urgency_level=triage_result.urgencyLevel,
        urgency_label=triage_result.urgencyLabel,
        recommended_action=triage_result.recommendedAction,
        notes=triage_result.notes,
        created_at=triage_result.createdAt,
    )


@router.get(
    "/triage/{triage_id}",
    response_model=TriageResponse,
    summary="Retrieve a triage result by its ID",
    description="Return the stored triage result for the given identifier.",
)
def get_triage_by_id(triage_id: str, db: Session = Depends(get_db)) -> TriageResponse:
    # Parse triage ID as UUID
    try:
        triage_uuid = uuid.UUID(triage_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="triage_id must be a valid UUID",
        )
    result = db.get(TriageResult, triage_uuid)
    if result is None:
        raise HTTPException(status_code=404, detail="Triage result not found")
    encounter = db.get(Encounter, result.encounterID)
    if encounter is None:
        raise HTTPException(status_code=500, detail="Encounter record missing for triage result")
    return TriageResponse(
        triage_id=str(result.triageID),
        encounter_id=str(result.encounterID),
        patient_id=str(encounter.patientID),
        summary=result.summary,
        urgency_level=result.urgencyLevel,
        urgency_label=result.urgencyLabel,
        recommended_action=result.recommendedAction,
        notes=result.notes,
        created_at=result.createdAt,
    )
