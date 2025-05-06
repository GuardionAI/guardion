from .sdk import guard_request
from agents import GuardrailFunctionOutput, RunContextWrapper, input_guardrail, Agent


@input_guardrail
async def guardion_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list
) -> GuardrailFunctionOutput:
    messages = [
        {"role": "user", "content": input if isinstance(input, str) else str(input)}
    ]

    request = guard_request(messages=messages, fail_fast=False)

    return GuardrailFunctionOutput(
        output_info=request, tripwire_triggered=request.get("flagged", False)
    )
