"""
Standalone test script for the ENT triage assistant models.

Run this script from the command line to verify connectivity to your
Ollama server and to inspect the output of the different tasks.  You
must set the `OLLAMA_HOST` and `OLLAMA_PORT` environment variables
before running, or edit `ai/ollama_client.py` to point at your
server.

Example usage::

    export OLLAMA_HOST=ec2-xx-xx-xx-xx.compute.amazonaws.com
    export OLLAMA_PORT=11434
    python -m app.ai.tests

The script will send sample prompts to the models and print the
parsed JSON responses along with timing information.
"""

from __future__ import annotations

import json
import time

from .ollama_client import (
    generate_triage,
    summarize_call,
    rank_cases,
    get_verification_questions_response,
)


def test_triage():
    print("Testing triage model...", flush=True)
    user_message = "I've had a sore throat and earache for three days and now I can't swallow without severe pain."
    result = generate_triage(user_message)
    print("Raw response:", result.get("response"))
    parsed = result.get("parsed_json")
    print("Parsed JSON:", json.dumps(parsed, indent=2))
    print(f"Latency: {result.get('latency_seconds', 'n/a'):.2f}s\n")


def test_summarization():
    print("Testing summarisation model...", flush=True)
    transcript = (
        "Patient: My daughter has been complaining of ear pain for a few hours."
        "\nDoctor: Has she had any fever or discharge?"
        "\nPatient: She says it's moderate pain, no fever yet, but she has a sore throat too."
        "\nDoctor: How long has the sore throat been present?"
        "\nPatient: About a day."
    )
    result = summarize_call(transcript)
    print("Raw response:", result.get("response"))
    parsed = result.get("parsed_json")
    print("Parsed JSON:", json.dumps(parsed, indent=2))
    print(f"Latency: {result.get('latency_seconds', 'n/a'):.2f}s\n")


def test_ranking():
    print("Testing ranking model...", flush=True)
    # Create dummy summaries for testing; in practice these would come
    # from the summarisation stage and include real IDs.
    summaries = [
        {"id": "case1", "primary_symptom": "ear pain", "urgency_score": 3, "red_flags": []},
        {"id": "case2", "primary_symptom": "nosebleed", "urgency_score": 4, "red_flags": ["active bleeding"]},
        {"id": "case3", "primary_symptom": "difficulty breathing", "urgency_score": 5, "red_flags": ["airway compromise"]},
    ]
    result = rank_cases(summaries)
    print("Raw response:", result.get("response"))
    parsed = result.get("parsed_json")
    print("Parsed JSON:", json.dumps(parsed, indent=2))
    print(f"Latency: {result.get('latency_seconds', 'n/a'):.2f}s\n")

def test_verification():
    print("Testing verification questions...", flush=True)
    result = get_verification_questions_response()
    parsed = result.get("parsed_json")
    print("Verification questions:", parsed)



def main():
    try:
        test_triage()
    except Exception as e:
        print(f"Triage test failed: {e}")
    try:
        test_summarization()
    except Exception as e:
        print(f"Summarisation test failed: {e}")
    try:
        test_ranking()
    except Exception as e:
        print(f"Ranking test failed: {e}")
    try:
        test_verification()
    except Exception as e:
        print(f"Verification test failed: {e}")


if __name__ == "__main__":
    main()