import os
import sys
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# The repository currently keeps providers in a sibling runtime module.
REPO_ROOT = Path(__file__).resolve().parents[3]
PROVIDERS_ROOT = REPO_ROOT / "chimera-runtime-02-providers-storage"
if str(PROVIDERS_ROOT) not in sys.path:
    sys.path.insert(0, str(PROVIDERS_ROOT))

from providers import OpenAIProvider
from models.vesicle import Vesicle

app = FastAPI(title="CHIMERA Runtime")


class GenerateRequest(BaseModel):
    prompt: str
    vesicle: Vesicle
    model: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(request: GenerateRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")

    # Pydantic has already validated the Vesicle at the API boundary.
    # Only the canonical validated representation is passed downstream.
    state = request.vesicle.validated_state()
    model_input = (
        "CHIMERA VALIDATED STATE (PION/Vesicle):\n"
        + json.dumps(state, sort_keys=True, separators=(",", ":"))
        + "\n\nUSER REQUEST:\n"
        + request.prompt
    )

    try:
        provider = OpenAIProvider(model=request.model)
        return {
            "provider": "openai",
            "model": provider.model,
            "vesicle_id": request.vesicle.id,
            "output": provider.generate(model_input),
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI provider error: {exc}") from exc
