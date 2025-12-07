"""Asynchronous client for invoking the large language model (LLM).

This module defines a thin wrapper around an underlying LLM service
which generates a structured triage assessment from a call transcript
and patient context.  It caches results in Redis to avoid redundant
computations and leverages the prompt template defined in
``app.ai.prompt``.  To integrate with Ollama running on AWS or another
deployment, set the ``OLLAMA_BASE_URL`` and ``OLLAMA_MODEL_NAME``
environment variables in your ``.env`` file.
"""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

from app.core.config import get_settings
from app.core.redis import redis_client
from .prompt import TRIAGE_PROMPT_TEMPLATE


@dataclass
class TriageResultData:
    """Structured triage result returned by the LLM."""

    summary: str
    urgency_level: int
    urgency_label: str
    recommended_action: str
    notes: Optional[str] = None


class TriageLLMClient:
    """Abstraction over an LLM service used to generate triage results."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def generate_triage(
        self, call_text: str, patient_context: Optional[Dict[str, Any]] = None
    ) -> TriageResultData:
        """Generate a triage assessment from the call text and context.

        This method first checks Redis for a cached result keyed by the
        transcript.  If a cached value exists, it is returned without
        contacting the LLM.  Otherwise it composes a prompt, issues an
        HTTP POST to the Ollama server, parses the returned JSON and
        caches the result for a limited time.

        :param call_text: The transcript of the patient's call.
        :param patient_context: Optional dictionary containing additional
            context about the patient (e.g. age, name).  This is embedded
            in the prompt as JSON.
        :returns: A :class:`TriageResultData` instance with structured
            triage information.
        :raises ValueError: If the response from Ollama cannot be parsed.
        """
        # Compute a deterministic cache key based on the call text and
        # patient context.  We include the context so that calls for the
        # same transcript but different patient attributes result in
        # independent cache entries.
        context_str = json.dumps(patient_context or {}, sort_keys=True, default=str)
        key_material = f"{call_text}::{context_str}".encode("utf-8")
        cache_key = "ai_triage:" + hashlib.md5(key_material).hexdigest()

        # Attempt to fetch a cached JSON string from Redis
        cached = redis_client.get(cache_key)
        if cached:
            try:
                data = json.loads(cached)
                return TriageResultData(**data)
            except Exception:
                # If cache entry is corrupted, delete it and fall back to LLM call
                redis_client.delete(cache_key)

        # Compose the prompt using the template
        prompt = TRIAGE_PROMPT_TEMPLATE.format(
            call_text=call_text,
            patient_context=context_str,
        )

        # Ensure Ollama configuration is present
        if not self.settings.OLLAMA_BASE_URL or not self.settings.OLLAMA_MODEL_NAME:
            raise ValueError(
                "OLLAMA_BASE_URL and OLLAMA_MODEL_NAME must be configured in the environment"
            )

        # Issue the request to the LLM
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url=f"{self.settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": self.settings.OLLAMA_MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                },
            )

        # Parse the JSON response.  Ollama returns an object with a
        # ``response`` field containing our model's output as a JSON
        # string.  We unwrap that and load it into a dict.
        try:
            response_json = response.json()
            raw_output = response_json.get("response", "")
            data = json.loads(raw_output)
        except Exception as exc:
            raise ValueError(
                f"Ollama returned invalid response: {response.text}"
            ) from exc

        # Store the result in Redis with a TTL of one hour to prevent
        # unbounded cache growth.  The TTL can be tuned via the environment.
        redis_client.setex(cache_key, 3600, json.dumps(data))

        return TriageResultData(**data)
