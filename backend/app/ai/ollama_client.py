"""
Simple client for interacting with an Ollama server.

This module wraps HTTP calls to the Ollama REST API and provides
functions specific to the ENT triage assistant.  It also includes
retry logic and integrates the JSON repair utility to make
responses more robust.

If you are deploying this code, set the `OLLAMA_HOST` and
`OLLAMA_PORT` environment variables to point at your EC2 instance
running Ollama.  For example:

    export OLLAMA_HOST=ec2-xx-xx-xx-xx.compute.amazonaws.com
    export OLLAMA_PORT=11434

Alternatively, edit the `OLLAMA_HOST` and `OLLAMA_PORT` constants
below.  The default models for chat, summarisation and ranking can
also be overridden via environment variables if desired.
"""

from __future__ import annotations

import os
import json
import time
from typing import Any, Dict, List

import requests

from .prompts import (
    build_triage_prompt,
    build_summarization_prompt,
    build_ranking_prompt,
    get_verification_questions,
)
from .json_utils import repair_json

# Host and port of the Ollama server.  Users should override via
# environment variables.  Note that the API path is hard‑coded.
OLLAMA_HOST: str = os.environ.get("OLLAMA_HOST", "localhost")
OLLAMA_PORT: str = os.environ.get("OLLAMA_PORT", "11434")

# Default model names for each task.  These can be overridden via
# environment variables or by passing the `model` argument explicitly
# to each helper function.
DEFAULT_CHAT_MODEL: str = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.1")
DEFAULT_SUMMARY_MODEL: str = os.environ.get("OLLAMA_SUMMARY_MODEL", "mistral")
DEFAULT_RANK_MODEL: str = os.environ.get("OLLAMA_RANK_MODEL", "llama3.1")


def _ollama_url() -> str:
    """Construct the base URL for the Ollama API."""
    return f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"


def call_model(prompt: str, model: str, *, format: str | None = None, max_retries: int = 3) -> Dict[str, Any]:
    """Call the Ollama `/api/generate` endpoint with a prompt.

    Args:
        prompt: The prompt to send to the model.
        model: The model identifier (e.g. "llama3.1").
        format: Optional output format hint.  If provided, it is
            passed through to the API (e.g. "json").  This can
            encourage the model to produce JSON but is not
            strictly required since our prompts instruct JSON.
        max_retries: Number of times to retry if the response
            cannot be parsed as JSON.  Defaults to 3.

    Returns:
        The JSON‑decoded response from the model.  The full JSON
        object returned by Ollama is returned.  If the model's
        generated response field contains JSON, you will need to
        parse it separately via `repair_json`.

    Raises:
        requests.RequestException: On network errors.
        ValueError: If the model returns a non‑OK status code.
    """
    url = _ollama_url()
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if format:
        payload["format"] = format

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            start_time = time.perf_counter()
            resp = requests.post(url, json=payload, timeout=300)
            duration = time.perf_counter() - start_time
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            # Network or HTTP error
            if attempt >= max_retries:
                raise
            continue

        # The model response should be in the "response" field.
        # Attempt to parse it as JSON; if it fails, we retry.
        content = data.get("response", "").strip()
        if not content:
            # No content returned; treat as error
            if attempt >= max_retries:
                return data
            continue

        try:
            repaired = repair_json(content)
            # Attach parse duration and latency for diagnostics.
            data["parsed_json"] = repaired
            data["latency_seconds"] = duration
            return data
        except json.JSONDecodeError:
            # Parsing failed; maybe due to model glitch.  Retry.
            if attempt >= max_retries:
                # Return raw data on last attempt to allow caller to
                # handle or report the error.
                data["latency_seconds"] = duration
                return data
            continue

    # Should not reach here; return last response if any
    raise RuntimeError("Failed to obtain valid response from Ollama")


def generate_triage(user_message: str, *, model: str | None = None) -> Dict[str, Any]:
    """Generate a triage chat response for a patient's message.

    This helper wraps `call_model` using the triage prompt template
    and the default chat model.  The returned dictionary will
    contain both the original model response and a parsed JSON
    representation in the `parsed_json` field on success.

    Args:
        user_message: The latest patient message to triage.
        model: Optional override of the model name.

    Returns:
        The raw Ollama response dictionary augmented with
        `parsed_json` on success.
    """
    prompt = build_triage_prompt(user_message)
    return call_model(prompt, model or DEFAULT_CHAT_MODEL)


def summarize_call(transcript: str, *, model: str | None = None) -> Dict[str, Any]:
    """Generate a structured summary for a call transcript.

    Args:
        transcript: The full transcript of the conversation.
        model: Optional override of the summarisation model.

    Returns:
        The raw Ollama response dictionary augmented with
        `parsed_json` on success.
    """
    prompt = build_summarization_prompt(transcript)
    return call_model(prompt, model or DEFAULT_SUMMARY_MODEL)


def rank_cases(summaries: List[Dict[str, Any]], *, model: str | None = None) -> Dict[str, Any]:
    """Rank a list of case summaries by urgency.

    Args:
        summaries: A list of summary dicts.  Each summary should include
            at least an "id", "primary_symptom", "urgency_score" and
            optionally "red_flags".
        model: Optional override of the ranking model.

    Returns:
        The raw Ollama response dictionary augmented with
        `parsed_json` on success, containing the ranked list.
    """
    prompt = build_ranking_prompt(summaries)
    return call_model(prompt, model or DEFAULT_RANK_MODEL)


def get_verification_questions_response() -> Dict[str, Any]:
    """Return verification questions packaged similarly to other responses.

    The verification questions are static and do not require an LLM call.
    This helper wraps them in a dictionary with a `parsed_json` key and
    placeholder fields for `response` and `latency_seconds` to align with
    the structure returned by other functions in this module.

    Returns:
        A dictionary containing the verification questions under
        `parsed_json` and dummy metadata fields.
    """
    questions = get_verification_questions()
    return {
        "parsed_json": {"questions": questions},
        "response": None,
        "latency_seconds": 0.0,
    }