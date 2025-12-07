"""AI triage package.

This package encapsulates all AI‑driven functionality for the ENT triage
system.  It provides a set of schemas, a prompt template, a client for
interacting with a large language model (LLM), and FastAPI routes for
invoking the triage service.  All modules in this package adhere to the
project conventions established in the production backend.
"""

# Re-export commonly used types for convenience
from .schemas import TriageRequest, TriageResponse  # noqa: F401
