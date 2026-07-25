import json
from groq import Groq

from app.core.config import settings

_client = Groq(api_key=settings.groq_api_key)


def call_json(prompt: str, system: str, model: str | None = None) -> dict:
    """Call Groq and force a JSON object back. Every LangGraph node that
    needs structured output goes through this one function."""
    response = _client.chat.completions.create(
        model=model or settings.groq_extraction_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"_raw": content, "_parse_error": True}


def call_text(prompt: str, system: str, model: str | None = None) -> str:
    """Plain text completion — used for chat and free-text summaries."""
    response = _client.chat.completions.create(
        model=model or settings.groq_reasoning_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
