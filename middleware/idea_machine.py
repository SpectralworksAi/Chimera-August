from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass(frozen=True)
class Flavor:
    name: str
    instruction: str
    model: str


DEFAULT_SEQUENCE = ["skeptic", "strategist", "builder"]

FLAVORS: dict[str, Flavor] = {
    "skeptic": Flavor(
        "Skeptic",
        "Attack the idea constructively. Identify unsupported assumptions, failure modes, contradictions, and the strongest objection. Do not redesign it yet.",
        os.getenv("GROQ_SKEPTIC_MODEL", "llama-3.3-70b-versatile"),
    ),
    "strategist": Flavor(
        "Strategist",
        "Turn the surviving idea into a practical strategy. Define target user, value, constraints, leverage points, and a plausible route to execution.",
        os.getenv("GROQ_STRATEGIST_MODEL", "llama-3.3-70b-versatile"),
    ),
    "builder": Flavor(
        "Builder",
        "Convert the current idea and prior analysis into a concrete implementation concept. Produce specific next steps, interfaces, artifacts, or experiments.",
        os.getenv("GROQ_BUILDER_MODEL", "llama-3.3-70b-versatile"),
    ),
}


class GroqClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is required")
        self.base_url = base_url or os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

    async def complete(self, *, model: str, system: str, user: str) -> str:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.7,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        return data["choices"][0]["message"]["content"]


async def relay_idea(
    idea: str,
    sequence: list[str] | None = None,
    client: GroqClient | None = None,
) -> dict[str, Any]:
    """Run a deliberate multi-step idea relay while preserving lineage."""
    if not idea.strip():
        raise ValueError("idea must not be empty")

    selected = sequence or DEFAULT_SEQUENCE
    unknown = [name for name in selected if name not in FLAVORS]
    if unknown:
        raise ValueError(f"unknown flavors: {', '.join(unknown)}")

    client = client or GroqClient()
    original_idea = idea.strip()
    current = original_idea
    history: list[dict[str, Any]] = []

    for index, flavor_name in enumerate(selected, start=1):
        flavor = FLAVORS[flavor_name]
        prompt = f"""Original idea:\n{original_idea}\n\nCurrent relay state:\n{current}\n\nYour role:\n{flavor.instruction}\n\nPrevious relay steps:\n{history}\n\nReturn only the substantive transformed analysis/output. Do not describe yourself as an AI persona."""
        output = await client.complete(
            model=flavor.model,
            system="You are one stage in a disciplined idea-development relay. Preserve useful information, challenge weak reasoning, and make the transformation substantive rather than cosmetic.",
            user=prompt,
        )
        history.append(
            {
                "step": index,
                "flavor": flavor.name,
                "model": flavor.model,
                "input": current,
                "output": output,
            }
        )
        current = output

    return {
        "original_idea": original_idea,
        "body": current,
        "sequence": selected,
        "history": history,
    }
