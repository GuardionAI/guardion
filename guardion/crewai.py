from .sdk import guard_request
from typing import Tuple, Any
from crewai import TaskOutput


def guardrail(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate and parse JSON output."""
    messages = [{"role": "system", "content": result.raw}]
    request = guard_request(messages=messages, fail_fast=False)
    if request.get("flagged", False):
        return (True, None)
    else:
        return (False, "Content contains Prompt Injection")
