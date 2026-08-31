from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

from .models.vesicle import Vesicle

app = FastAPI(title="CHIMERA Runtime")


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1)
    vesicle: Vesicle


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(request: GenerateRequest):
    """Generate from a validated CHIMERA/PION state, not from a raw prompt alone."""
    try:
        pion = request.vesicle.validated_pion()
    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "invalid_pion_state",
                "message": "The Vesicle payload is not a valid CPS/1.0 PION packet.",
                "validation": exc.errors(),
            },
        ) from exc

    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    client = OpenAI()

    validated_state = pion.model_dump_json(exclude_none=True)
    instructions = (
        "You are the model provider inside CHIMERA. "
        "The PION packet below has already passed CHIMERA validation. "
        "Use it as authoritative execution context for this request. "
        "Do not silently rewrite, commit, or invent CHIMERA state. "
        "If the user request conflicts with validated state, identify the conflict."
    )
    model_input = (
        "VALIDATED_CHIMERA_PION_STATE:\n"
        f"{validated_state}\n\n"
        "USER_REQUEST:\n"
        f"{request.prompt.strip()}"
    )

    try:
        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=model_input,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail="OpenAI generation failed") from exc

    return {
        "vesicle_id": request.vesicle.id,
        "protocol": pion.protocol,
        "model": model,
        "output": response.output_text,
        "validated_pion": pion.model_dump(mode="json"),
    }
