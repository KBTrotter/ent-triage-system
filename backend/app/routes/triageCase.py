import uuid
from typing import Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, func, select
from app.core.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models import (
    TriageCase,
    TriageCaseCreate,
    TriageCasePublic,
    TriageCasesPublic,
    TriageCaseUpdate,
    TriageCaseResolve,
    Message,
    Patient,
)

router = APIRouter(prefix="/triage-cases", tags=["triage-cases"])

@router.get("/", response_model=TriageCasesPublic)
def get_all_cases(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    count_statement = select(func.count()).select_from(TriageCase)
    count = db.exec(count_statement).one()
    
    statement = select(TriageCase, Patient).join(Patient).limit(limit)
    results = db.exec(statement).all()
    
    cases_public = [
        TriageCasePublic(
            **case.model_dump(),
            first_name=patient.first_name,
            last_name=patient.last_name,
            dob=patient.dob,
        )
        for case, patient in results
    ]

    return TriageCasesPublic(data=cases_public, count=count)

@router.get("/status/{status}", response_model=TriageCasesPublic)
def get_cases_by_status(
    status: str,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    count_statement = (
        select(func.count())
        .select_from(TriageCase)
        .where(TriageCase.status == status)
    )
    count = db.exec(count_statement).one()
    
    statement = (
        select(TriageCase)
        .where(TriageCase.status == status)
        .limit(limit)
    )
    cases = db.exec(statement).all()

    return TriageCasesPublic(data=cases, count=count)

@router.get("/{id}", response_model=TriageCasePublic)
def get_specific_case(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    case = db.get(TriageCase, id)
    if not case:
        raise HTTPException(status_code=404, detail="Triage case not found")
    return case

@router.post("/", response_model=TriageCasePublic)
def create_new_case(
    new_case: TriageCaseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    case = TriageCase.model_validate(new_case)
    # uncomment this once the user ids are proper uuids
    # case.created_by = current_user["userID"]
    
    db.add(case)
    db.commit()
    db.refresh(case)
    return case

@router.put("/{id}", response_model=TriageCasePublic)
def update_case(
    id: uuid.UUID,
    update: TriageCaseUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    if update.status.lower() == "resolved" or update.resolution_reason:
        raise HTTPException(status_code=403, detail="Triage case cannot be resolved through generic update")
    
    case = db.get(TriageCase, id)
    if not case:
        raise HTTPException(status_code=404, detail="Triage case not found")
    
    update_dict = update.model_dump(exclude_unset=True)
    case.sqlmodel_update(update_dict)
    
    db.add(case)
    db.commit()
    db.refresh(case)
    return case

@router.delete("/{id}")
def delete_case(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Message:
    case = db.get(TriageCase, id)
    if not case:
        raise HTTPException(status_code=404, detail="Triage case not found")
    
    db.delete(case)
    db.commit()
    return Message(message="Triage case deleted successfully")

@router.patch("/{id}/resolve", response_model=TriageCasePublic)
def resolve_case(
    id: uuid.UUID,
    update: TriageCaseResolve,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    case = db.get(TriageCase, id)
    if not case:
        raise HTTPException(status_code=404, detail="Triage case not found")
    
    case.status = "resolved"
    case.resolution_reason = update.resolution_reason
    # uncomment this once the user ids are proper uuids
    # case.resolved_by = current_user["userID"]
    case.resolution_timestamp = datetime.now()

    db.add(case)
    db.commit()
    db.refresh(case)
    return case