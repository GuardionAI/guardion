import os
import httpx

from typing import List
from .exceptions import GuardionError, InjectionDetectedError


def process_guard_response(response: dict):
    """
    Function that processes the response and extract the relevant information,
    given a certain policy that is defined in the Guardion Customer Panel.
    """
    if response.get("detail") == "Invalid credentials":
        raise GuardionError("Invalid credentials")

    if not response.get("flagged", False):
        return

    breakdown = response.get("breakdown", [])
    for detail in breakdown:
        for result in detail.get("result", []):
            if result["label"].lower() == "injection":
                score = str(round(result["score"] * 100))
                raise InjectionDetectedError(
                    f"There is a chance of {score}% that the request is an injection attempt."
                )

    return response


def guard_request(
    messages: List[dict],
    api_key: str = os.getenv("GUARDIONAI_API_KEY"),
    override_enabled_policies: List[str] = None,
    override_response: str = None,
    breakdown_all: bool = False,
    fail_fast: bool = True,
):
    """
    Function that sends the request to the Guardion API and processes the response.
    It will raise an InjectionDetectedError if the request is flagged as an injection attempt.
    It will raise a GuardionError if the request fails from an auth or server error.
    :params:
        messages: List[dict]: The messages to send to the Guardion API.
        api_key: str: The API key to use to send the request.
        override_enabled_policies: List[str]: Optional - The policies to use to override the default ones.
        override_response: str: Optional - The response to override the default one.
        breakdown_all: bool: Optional - Whether to breakdown the response.
        fail_fast: bool: Optional - Whether to fail fast.
    """
    response = httpx.post(
        "https://api.guardion.ai/v1/guard",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "session": None,
            "messages": messages,
            "override_enabled_policies": override_enabled_policies,
            "override_response": override_response,
            "breakdown_all": breakdown_all,
            "fail_fast": fail_fast,
            "application": "guardionsdk",
        },
    )
    breakpoint()
    try:
        return process_guard_response(response.json())
    except Exception as e:
        if not fail_fast:
            return response.json()
        raise e
