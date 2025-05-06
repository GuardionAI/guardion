import os
import httpx
from pyexpat.errors import messages

from typing import List, Union
from langchain.schema import BaseMessage, PromptValue
from langchain_core.language_models import BaseLanguageModel
from .sdk import guard_request, GuardionError


ROLE_MAPPING = {
    "system": "system",
    "ai": "system",
    "user": "user",
    "human": "user",
    "assistant": "assistant",
}


def format_input(prompt: Union[str, List[BaseMessage], PromptValue]) -> dict:
    if isinstance(prompt, str):
        return prompt

    if isinstance(prompt, PromptValue):
        prompt = prompt.to_messages()

    if not isinstance(prompt, list):
        raise GuardionError(f"Invalid prompt type: {type(prompt)} for prompt: {prompt}")

    messages = []

    for message in prompt:
        if not isinstance(message, BaseMessage):
            raise GuardionError(
                f"Invalid message type: {type(message)} for message: {message}"
            )

        messages.append(
            {
                "role": ROLE_MAPPING.get(message.type, message.type),
                "content": message.content,
            }
        )

    return messages


class InvalidGuardionRequest(Exception):
    pass


def get_api_key(api_key: str = None):
    return api_key or os.getenv("GUARDIONAI_API_KEY", "sk-guardion-api-key")


def get_guarded_llm(base_llm_model: BaseLanguageModel, api_key: str = None):
    class GuardedLangChain(base_llm_model):
        def _llm_type(self) -> str:
            return "guardionai_" + super()._llm_type

        def _generate(self, messages: List[BaseMessage]) -> str:
            guard_request(api_key=get_api_key(api_key), messages=format_input(messages))
            return super()._generate(messages)

    return GuardedLangChain


def get_guarded_chat_llm(base_llm_model: BaseLanguageModel, api_key: str = None):
    class GuardedChatLangChain(base_llm_model):
        def _llm_type(self) -> str:
            return "guardionai_" + super()._llm_type

        def _generate(self, messages: List[BaseMessage], *args, **kwargs) -> str:
            guard_request(api_key=get_api_key(api_key), messages=format_input(messages))
            return super()._generate(messages, *args, **kwargs)

    return GuardedChatLangChain
