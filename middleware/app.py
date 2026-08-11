from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from idea_machine import relay_idea

app = FastAPI(title="CHIMERA Idea Machine Middleware", version="0.1.0")


class RelayRequest(BaseModel):
    idea: str = Field(min_length=1)
    sequence: list[str] | None = None


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "chimera-idea-machine"}


@app.post("/relay")
async def relay(request: RelayRequest):
    try:
        return await relay_idea(request.idea, request.sequence)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
