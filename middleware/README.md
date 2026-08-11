# CHIMERA Middleware v0.1

A small, provider-independent continuity middleware layer.

## What it does

- accepts a normal chat request
- loads explicit local state
- builds a bounded context envelope
- sends the request to a provider adapter
- records the interaction and semantic delta
- exports/imports portable PION state

## First provider

Groq via its OpenAI-compatible Chat Completions API. The provider is isolated behind `Provider` so another model provider can be added without changing the runtime.

## Run

```powershell
cd middleware
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GROQ_API_KEY="your-key"
uvicorn app:app --reload
```

Then call `POST /chat` with:

```json
{"message":"Hello", "session_id":"demo"}
```

State is stored locally under `middleware/data/` and can be exported with `GET /pion/export`.

The API key is never stored in PION state.
