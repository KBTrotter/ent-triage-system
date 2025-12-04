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


def build_triage_prompt(conversation: list[dict]) -> str:
    """
    Build a structured, clinically guided ENT triage prompt.
    The model must conduct a structured interview, asking ONE question at a time.
    """

    system_instructions = """
    You are a medical triage assistant specializing in ENT (Ear, Nose, and Throat).
    Your goal is to collect structured clinical information to determine urgency.

    Follow this exact order of questions. Ask ONE question at a time.
    Wait for the user's answer before asking the next question.

    QUESTIONS TO ASK (in order):
    1. DURATION: "How long have you had this symptom?"
    2. SEVERITY: "Is your throat pain mild, moderate, or severe?"
    3. STABILITY: "Is the symptom getting better, worse, or staying the same?"
    4. AGGRAVATING FACTORS: "What makes the symptoms worse?"
    5. RELIEVING FACTORS: "What makes the symptoms better?"
    6. PREDISPOSING FACTORS: "Do you have diabetes, immune suppression, or other risk factors?"
    7. ASSOCIATED SYMPTOMS: "Are there other symptoms that occur with this?"
    8. CORRELATING DATA: "Have you had any test results, scans, or found any neck masses?"

    RED FLAG CONDITIONS (critical):
    - difficulty breathing
    - drooling
    - inability to swallow
    - neck swelling
    - spitting up blood
    - fever over 102F
    - rapid progression

    RULES:
    - If a red flag is mentioned, IMMEDIATELY stop asking further questions.
    - Respond with a short message advising urgent evaluation.
    - Set urgency_level="emergent"

    OUTPUT:
    Always respond with a valid JSON dictionary with the following fields:
    {
    "next_question": string | null,
    "duration": string | null,
    "severity": string | null,
    "stability": string | null,
    "aggravating_factors": string | null,
    "relieving_factors": string | null,
    "predisposing_factors": string | null,
    "associated_symptoms": string | null,
    "correlating_data": string | null,
    "red_flags_present": boolean,
    "red_flags": list[str],
    "urgency_level": "low" | "moderate" | "high" | "emergent",
    "triage_complete": boolean
    }

    CONSTRAINTS:
    - Never hallucinate answers
    - Only fill fields that the user has mentioned
    - Ask only ONE question at a time
    - Never output natural language outside JSON
    - Never output explanations outside JSON
    """

    conversation_text = "\n".join(
        f"{turn['role']}: {turn['content']}" for turn in conversation
    )

    full_prompt = f"{system_instructions}\n\nConversation so far:\n{conversation_text}\n\nRespond with JSON only."
    return full_prompt


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


# ---------------------------------------------------------------------------
# Verification questions
#
# Before beginning an AI‑driven triage session, callers need to be verified
# and some basic intake information collected.  These questions are asked
# prior to any interaction with the language model.  They are returned as
# a simple list of strings so they can be presented by the frontend without
# requiring an inference call.  Keeping the questions in this module
# centralises their definition so they can be updated easily in one place.

def get_verification_questions() -> list[str]:
    """Return a list of standard questions used to verify the patient.

    These questions help confirm the caller's identity and collect
    essential demographic and medical history before triage begins.  They
    are deliberately kept simple and do not depend on any model output.

    Returns:
        A list of questions as strings.
    """
    #! QUESTIONS

    """
    (timing) How long have you had this symptom?

    (severity) Is your “throat” pay mild or severe?

    (stability or progressive) Is your symptom getting better or worse?

    (aggravating factors) What specifically makes the symptoms worse?

    (revealing factors) What specifically makes the symptoms better?

    (contingent/pre-disposing factors) Is your immune system suppressed, diabetes?

    (associating symptoms) Are there other symptoms that your finding when this occurs?

    (correlating data) Test Results that implicate a more sever situation? Suspicious mass in your neck?
    """
    return [
        "What is your full name?",
        "What is your date of birth?",
        "What is your phone number or email address?",
        "Do you have any known allergies to medications?",
        "Do you have any chronic medical conditions we should be aware of?",
    ]