"""
Utility functions for working with JSON returned by language models.

The models may occasionally produce malformed JSON (e.g. single quotes,
trailing commas, missing quotes around keys).  The functions in
this module attempt to repair such outputs so they can be parsed
reliably.  They are deliberately simple and conservative; if
repairing fails, a JSONDecodeError will be propagated.
"""

from __future__ import annotations

import json
import ast
import re
from typing import Any


def repair_json(s: str) -> Any:
    """Attempt to parse potentially malformed JSON into a Python object.

    This function tries multiple strategies to coerce the model's
    output into valid JSON.  It is not bullet‑proof but handles
    common cases such as:
      * single quotes instead of double quotes
      * trailing commas in objects or arrays
      * Python dict syntax (unquoted keys)

    Args:
        s: The raw string returned from the model.

    Returns:
        A Python object parsed from the JSON.

    Raises:
        json.JSONDecodeError: If parsing fails after repair attempts.
    """
    if not isinstance(s, str):
        raise TypeError("Input to repair_json must be a string")

    # First try normal JSON parsing.
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass

    # Replace single quotes with double quotes (common in model output).
    maybe = s.replace("'", '"')
    try:
        return json.loads(maybe)
    except json.JSONDecodeError:
        pass

    # Remove trailing commas (in objects or arrays) using regex.
    no_trailing_commas = re.sub(r",(\s*[}\]])", r"\1", maybe)
    try:
        return json.loads(no_trailing_commas)
    except json.JSONDecodeError:
        pass

    # As a last resort, try parsing with ast.literal_eval which can
    # handle Python dict syntax.  Convert into JSON string first.
    try:
        obj = ast.literal_eval(s)
        # Convert the Python object back into JSON string then parse.
        return json.loads(json.dumps(obj))
    except Exception:
        # If all attempts fail, re‑raise the original JSON error.
        raise json.JSONDecodeError(
            "Unable to parse or repair JSON", s, 0
        )