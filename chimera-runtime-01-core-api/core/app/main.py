import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# The repository currently keeps providers in a sibling runtime module.
PROVIDERS_ROOT = Path(__file__).resolve().parents[5] / "chimera-runtime-02-providers-storage"
if str(PROVIDERS_ROOT) not in sys.path:
    sys.path.insert(0, str(PROVIDERS_ROOT))

from providers import OpenAIProvider

app = FastAPI(title="CHIMERA Runtime")


class GenerateRequest(BaseModel):
    prompt: str
    model: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(request: GenerateRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")

    try:
        provider = OpenAIProvider(model=request.model)
        return {"provider": "openai", "model": provider.model, "output": provider.generate(request.prompt)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI provider error: {exc}") from exc
