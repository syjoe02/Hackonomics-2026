import json
import re
from typing import Any, List


def clean_json_response(data: Any) -> List[dict]:
    """
    Normalize Gemini responses into a Python list.

    Handles:
    - markdown ```json blocks
    - raw JSON strings
    - already parsed Python lists
    - malformed trailing commas
    """

    if isinstance(data, list):
        return data

    if not data or not isinstance(data, str):
        return []

    text = data.strip()

    # remove markdown fences
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)

    # remove JS-style comments
    text = re.sub(r"//.*", "", text)

    # try direct load first
    try:
        return json.loads(text)
    except Exception:
        pass

    # extract JSON array safely
    match = re.search(
        r"$begin:math:display$\\s\*\{\.\*\}\\s\*$end:math:display$", text, re.DOTALL
    )
    if not match:
        return []

    json_text = match.group(0)

    # remove trailing commas
    json_text = re.sub(r",\s*}", "}", json_text)
    json_text = re.sub(r",\s*]", "]", json_text)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        return []
