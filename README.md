# Guardion - AI Firewall SDK

Guardion is a **lightning-fast, context-aware AI Firewall SDK**, built to protect LLM-based systems from prompt injection and misuse. Seamlessly integrates with leading agent frameworks.

In the background, Guardion uses a robust **Prompt Defense System** developed by the GuardionAI research team. Our production-grade detection engine, [ModernGuard](https://docs.guardion.ai/modern-guard), continuously evaluates threats using a multilayered architecture of classifiers, heuristics, and decoding pipelines.

✅ **Tested and proven in production by major financial institutions.**  

## 🔬 Benchmarks

### Detection Performance
Multilingual prompt injection evaluation for finance and e-commerce domains.

| Model                                                  | Overall F1-Score |
|--------------------------------------------------------|------------------|
| **guardion/Modern-Guard-v1**                           | **0.9718**       |
| Lakera Guard                                            | 0.8600           |
| protectai/deberta-v3-base-prompt-injection-v2          | 0.6008           |
| deepset/deberta-v3-base-injection                      | 0.5725           |
| meta-llama/Prompt-Guard-2-86M                           | 0.4555           |
| jackhhao/jailbreak-classifier                          | 0.5000           |

**Notes**
> Tested on a multilingual, multi-attack dataset of 50K prompts with 40+ attack classes in 8 languages.

> Evaluation data was built using real-world red team data from partners and the latest jailbreak and attack methods, including: encoding, prompt injection, jailbreaking, exfiltration & leakage, evasion & obfuscation, code and command injection, hard negatives (safe content), regular documents (safe content), regular chats (safe content), and more. [See more details here](https://docs.guardion.ai/modern-guard).

## Features

✅ Plug-and-play SDK for popular agent and LLM frameworks

🛡️ Real-time prompt inspection

🔍 Customizable detectors and security policies

🚀 Optimized for low latency and high throughput

## How to use?

First, get an API Key at [GuardionAI Console](https://guardion.ai).

And store at the env var `GUARDIONAI_API_KEY`.

```bash
export GUARDIONAI_API_KEY=your-api-key
```

### OpenAI Agents SDK

You need to install our SDK using our openai-agents extras with the following command:

```bash
pip install guardion[openai_agents]
```

```python
from agents import Agent, Runner, InputGuardrailTripwireTriggered
from guardionsdk.openai_agents import guardion_guardrail

agent = Agent(
    name="Secure AI Assistant",
    instructions="You are a helpful and safe assistant.",
    input_guardrails=[guardion_guardrail],
)
```

And use it as shown in the file `examples/openai_agents.sdk`.

### LangChain

We support Chat and simple LLM models from LangChain, in order to use it, you need to install our langchain extra.

```bash
pip install guardion[langchain]
```
```python
from langchain_openai import ChatOpenAI
from guardionsdk.langchain import get_guarded_chat_llm
from guardionsdk.exceptions import InjectionDetectedError

GuardionOpenAI = get_guarded_chat_llm(
    ChatOpenAI
)
llm_guardion = GuardionOpenAI(model="gpt-4o-mini")
```

And in order to use it, just checkout our `examples/langhchain.py` file.
