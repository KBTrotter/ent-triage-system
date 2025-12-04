"""
AI utilities and FastAPI routes for the ENT triage system.

This package contains prompt templates, helper utilities for parsing
and repairing JSON returned from language models, a simple client
for calling an Ollama server, test scripts for validating model
behaviour, and a FastAPI router to expose the AI functionality
through the existing backend.

The user should place any environment-specific configuration
such as the Ollama server host and port in environment variables
or modify the constants in `ollama_client.py`.  See that module
for details.
"""

from . import prompts  # noqa: F401
from . import json_utils  # noqa: F401
from . import ollama_client  # noqa: F401
from . import routes  # noqa: F401