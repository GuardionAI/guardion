import asyncio
from agents import Agent, Runner, InputGuardrailTripwireTriggered
from guardionsdk.openai_agents import guardion_guardrail


agent = Agent(
    name="Secure AI Assistant",
    instructions="You are a helpful and safe assistant.",
    input_guardrails=[guardion_guardrail],
)


async def main():
    try:
        user_prompt = "How can I hack a website?"
        result = await Runner.run(agent, user_prompt)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("❌ Input flagged by GuardionAI!")


asyncio.run(main())
