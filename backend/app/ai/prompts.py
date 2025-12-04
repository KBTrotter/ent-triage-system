"""
Prompt templates for the ENT triage assistant.

These templates are designed to work with large language models
hosted on an Ollama server. Each template instructs the model to
produce structured JSON output so that the frontend can parse
responses deterministically.

Usage:
    from app.ai.prompts import build_triage_prompt
    prompt = build_triage_prompt("Patient complains of ear pain for two days.")
    # pass `prompt` into the Ollama API via `ollama_client.call_model()`
"""

from textwrap import dedent


def build_triage_prompt(user_message: str) -> str:
    """Return a system prompt for the triage chat task.

    The model is instructed to ask concise follow‑up questions, extract
    symptoms and red flags, and return a JSON object.  The caller
    provides the user's latest message.

    Args:
        user_message: The most recent patient input.

    Returns:
        A formatted prompt string ready to be sent to the model.
    """
    prompt = dedent(
        f"""
        You are an otolaryngology (ENT) triage assistant helping to
        collect information from a patient.  The patient has provided
        the following message:

        "{user_message.strip()}"

        Your tasks:
        1. Identify and list all symptoms mentioned, noting their
           severity (mild/moderate/severe) and duration where possible.
        2. Detect any red‑flag symptoms for ENT emergencies (e.g., airway
           compromise, active bleeding, sudden hearing loss, difficulty
           swallowing, high fever).  Flag these clearly.
        3. Ask a single concise follow‑up question to clarify missing
           information that is critical for triage.  Do not ask more
           than one question at a time.
        4. Assess an overall urgency level: "low", "medium", or "high"
           based on the presented information.

        Respond **only** with a JSON object matching this schema:
        {{
          "follow_up_question": string,
          "symptoms": [{{"name": string, "duration": string, "severity": string}}],
          "red_flags": [string],
          "urgency": string
        }}

        Do not include any additional fields or narrative text.  The
        JSON must be syntactically valid and parseable.  If no red
        flags are present, return an empty list for "red_flags".
        """
    )
    return prompt


def build_summarization_prompt(transcript: str) -> str:
    """Return a prompt for summarising a call transcript.

    The summarisation prompt asks the model to extract key ENT
    complaint attributes and present them in a structured JSON
    object.  Use this after a call completes to produce a record.

    Args:
        transcript: The full conversation or call transcript.

    Returns:
        A prompt string for the summarisation model.
    """
    prompt = dedent(
        f"""
        You are an otolaryngology (ENT) triage assistant reviewing a
        transcript of a call between a patient and a healthcare
        provider.  Your job is to create a concise structured summary
        of the patient's ENT complaint for use by medical staff.

        Call transcript:
        "{transcript.strip()}"

        From this transcript, extract and fill in the following
        fields:
        - primary_symptom: the main ENT complaint (e.g. "ear pain").
        - secondary_symptoms: a list of other symptoms described.
        - duration: how long the primary symptom has been present.
        - severity: mild / moderate / severe.
        - possible_diagnoses: a short list of plausible ENT diagnoses
          (e.g. otitis media, sinusitis, tonsillitis).
        - urgency_score: an integer from 1 (least urgent) to 5 (most
          urgent) representing the need for prompt evaluation.
        - recommendation: a brief recommendation for next steps (e.g.
          "schedule non‑urgent appointment", "go to emergency room").

        Respond **only** with a JSON object matching this schema:
        {{
          "primary_symptom": string,
          "secondary_symptoms": [string],
          "duration": string,
          "severity": string,
          "possible_diagnoses": [string],
          "urgency_score": int,
          "recommendation": string
        }}

        Do not include any explanation or additional fields.  Ensure
        that the JSON is valid and parseable.
        """
    )
    return prompt


def build_ranking_prompt(summaries: list[dict]) -> str:
    """Return a prompt for ranking multiple cases by urgency.

    Given a list of case summaries (already extracted via
    build_summarization_prompt), the model is asked to assign a
    ranking based on ENT urgency.  Each summary in the list must
    contain at least an "id" and an "urgency_score" field.

    Args:
        summaries: A list of dictionaries representing case summaries.
          Each dictionary should include keys like "id", "primary_symptom",
          "urgency_score", and "red_flags".

    Returns:
        A prompt string instructing the model to rank the cases.
    """
    # Compose a bullet list of cases for the model to consider.
    cases_text_lines = []
    for case in summaries:
        # We'll ensure each summary has an id and urgency_score for ranking.
        cid = case.get("id", "unknown")
        primary = case.get("primary_symptom", "unknown symptom")
        urgency = case.get("urgency_score", "?")
        red_flags = ", ".join(case.get("red_flags", [])) or "none"
        cases_text_lines.append(f"Case {cid}: primary_symptom='{primary}', urgency_score={urgency}, red_flags={red_flags}")
    cases_text = "\n".join(cases_text_lines)

    prompt = dedent(
        f"""
        You are an otolaryngology (ENT) triage assistant asked to
        prioritise a list of cases from most urgent to least urgent.
        Each case is described by its primary symptom, an estimated
        urgency score (1–5) and any identified red flags.

        Cases to rank:
        {cases_text}

        Rank the cases and return a JSON array of objects in
        descending order of urgency.  Each object must contain:
        - id: the case identifier
        - rank: position in the queue starting from 1 (1 is most urgent)
        - score: an updated urgency score (int 1–5) reflecting your
          judgement
        - explanation: a short explanation for the assigned rank

        Example response:
        [
          {{"id": "A", "rank": 1, "score": 5, "explanation": "active bleeding"}},
          {{"id": "B", "rank": 2, "score": 4, "explanation": "severe pain and fever"}}
        ]

        Do not include any extra commentary or fields.  The JSON
        array must be valid and parseable.
        """
    )
    return prompt