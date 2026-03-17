import os
from typing import Protocol

from openai import APIError, AuthenticationError, OpenAI

from app.utils.env import load_env_file


class ScriptPayload(Protocol):
    company_type: str
    manager_type: str


GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"


MODE_RULES = {
    "safe": {
        "tone": "Very polite, low-pressure, and indirect.",
        "constraints": [
            "Make the ask gently rather than forcing urgency.",
            "Keep the request open-ended and respectful.",
            "Avoid pressure or ultimatums.",
        ],
    },
    "balanced": {
        "tone": "Professional, assertive, and practical.",
        "constraints": [
            "State the ask clearly and confidently.",
            "Mention a handover or transition plan.",
            "Keep the tone respectful and businesslike.",
        ],
    },
    "aggressive": {
        "tone": "Direct, confident, and time-bound.",
        "constraints": [
            "Make a specific time-bound request.",
            "Sound confident without becoming rude.",
            "Use clear urgency and strong ownership.",
        ],
    },
}


def generate_negotiation_script(payload: ScriptPayload, score: int, mode: str) -> str:
    load_env_file()

    api_key = os.environ.get("GROQ_API_KEY", "").strip().replace('"', '').replace("'", "")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set in the backend environment.")
    print(api_key)
    
    client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
    prompt = build_script_prompt(payload, score, mode)

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except AuthenticationError as exc:
        raise RuntimeError("Groq rejected the API key. Check GROQ_API_KEY.") from exc
    except APIError as exc:
        raise RuntimeError(f"Groq request failed: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Script generation failed: {exc}") from exc

    message = response.choices[0].message.content if response.choices else None
    if not message:
        raise RuntimeError("Groq returned an empty script response.")
    return message.strip()


def build_script_prompt(payload: ScriptPayload, score: int, mode: str) -> str:
    rules = MODE_RULES.get(mode, MODE_RULES["balanced"])
    manager_instruction = (
        "Account for a supportive manager and keep the tone collaborative."
        if payload.manager_type == "supportive"
        else "Account for a toxic manager and keep the wording formal and careful."
        if payload.manager_type == "toxic"
        else "Account for a neutral manager and keep the wording practical."
    )

    constraints = "\n".join(f"- {item}" for item in rules["constraints"])

    return f"""
    You are helping a software engineer negotiate early release from a notice period.

    Context:
    - Company type: {payload.company_type}
    - Manager type: {payload.manager_type}
    - Negotiation strength score: {score}/100
    - Requested style: {mode}

    Tone instruction:
    - {rules['tone']}
    - {manager_instruction}

    Constraints:
    {constraints}
    - Write a single message that is realistic and ready to send.
    - Keep it to 5 to 7 lines.
    - Mention a real reason for leaving such as growth or a better opportunity.
    - Do not add bullet points, labels, or explanation.
    - Output only the message.
    """.strip()
