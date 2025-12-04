"""
FastAPI router exposing the AI triage functionality.

This router defines three endpoints:

  * **POST /ai/chat** – given a patient's message, return a structured
    triage response with follow‑up question, extracted symptoms,
    red flags and urgency.
  * **POST /ai/summarize** – given a full call transcript, return a
    structured summary with key ENT complaint attributes.
  * **POST /ai/rank** – given a list of summary objects, return a
    ranked ordering by urgency.

Each endpoint delegates to helper functions in `ollama_client.py`.
"""

from __future__ import annotations

from typing import Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .ollama_client import generate_triage, summarize_call, rank_cases, get_verification_questions_response


router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""
    message: str = Field(..., description="The patient's latest message")


class SummarizeRequest(BaseModel):
    """Request body for the summarisation endpoint."""
    transcript: str = Field(..., description="Full call transcript to summarise")


class SummaryItem(BaseModel):
    """Summary item used for ranking."""
    id: str
    primary_symptom: str
    urgency_score: int
    red_flags: List[str] = Field(default_factory=list)


class RankRequest(BaseModel):
    """Request body for the ranking endpoint."""
    summaries: List[SummaryItem] = Field(..., description="List of summaries to rank", min_length=1)


# Response model for verification questions
class VerifyResponse(BaseModel):
    """Schema for the verification questions endpoint response.

    Contains a list of questions to ask the patient before triage begins.
    """
    questions: List[str]


@router.post("/chat")
async def chat_endpoint(req: ChatRequest) -> Any:
    """Handle a triage chat message and return structured information."""
    try:
        result = generate_triage(req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {e}")
    parsed = result.get("parsed_json")
    if parsed is None:
        # If parsing failed return the raw response for debugging
        return {"raw_response": result.get("response"), "error": "unable to parse JSON"}
    return parsed


@router.post("/summarize")
async def summarize_endpoint(req: SummarizeRequest) -> Any:
    """Summarise a call transcript and return structured data."""
    try:
        result = summarize_call(req.transcript)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {e}")
    parsed = result.get("parsed_json")
    if parsed is None:
        return {"raw_response": result.get("response"), "error": "unable to parse JSON"}
    return parsed


@router.post("/rank")
async def rank_endpoint(req: RankRequest) -> Any:
    """Rank a list of case summaries by urgency."""
    # Convert Pydantic models into plain dicts for the ranker
    summaries_list = [item.dict() for item in req.summaries]
    try:
        result = rank_cases(summaries_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {e}")
    parsed = result.get("parsed_json")
    if parsed is None:
        return {"raw_response": result.get("response"), "error": "unable to parse JSON"}
    return parsed


@router.get("/verify", response_model=VerifyResponse)
async def verify_endpoint() -> Any:
    """Return initial verification questions for the patient.

    These static questions are used to confirm the caller's identity and collect
    essential demographic and medical information before starting the AI triage
    conversation.  No inference call is required for this endpoint.
    """
    try:
        result = get_verification_questions_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    parsed = result.get("parsed_json")
    if parsed is None:
        return {"error": "unable to retrieve verification questions"}
    return parsed