"""LocalLab umbrella CLI package."""

import json
import os
from pathlib import Path

__version__ = "0.1.0"


_ROOT = Path(__file__).resolve().parent


def load_tools() -> dict:
    """Return the validated tool-name → repo/package/smoke mapping."""
    path = _ROOT / "data" / "tools.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("tools.json must be a mapping")
    return data
