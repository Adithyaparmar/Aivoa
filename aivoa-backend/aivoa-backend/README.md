# AIVOA — Complaint Intake Backend

FastAPI + LangGraph backend. One agent graph runs the whole pipeline:
extract fields → check completeness → classify risk → detect duplicates →
recommend root cause → recommend CAPA → summarize.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate       # .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env            # fill in GROQ_API_KEY and DATABASE_URL
uvicorn app.main:app --reload --port 8000
```

Docs at `http://localhost:8000/docs`.

## Structure

```
app/
  main.py                  FastAPI app, CORS, router registration
  core/config.py           Settings (env vars)
  core/db.py                SQLAlchemy engine/session
  models/complaint.py       Complaint table
  schemas/complaint.py      Pydantic request/response models
  agent/state.py            Shared LangGraph state (TypedDict)
  agent/nodes.py            One function per graph node
  agent/graph.py            Graph wiring — core path + bonus branches
  services/groq_client.py   Single place that calls Groq
  services/document_parser.py   PDF/DOCX/TXT → plain text
  api/complaints.py         POST /complaints/process, POST /complaints
  api/assistant.py          POST /assistant/ask (chat box)
```

## Endpoint contract (matches the frontend)

- `POST /api/complaints/process` — multipart `file` or form `text` →
  runs the full graph → returns `{ fields, completeness, risk,
  duplicate_check, root_cause_suggestion, capa_suggestion, summary }`.
- `POST /api/assistant/ask` — `{ question, context }` → `{ answer }`.
- `POST /api/complaints` — persists the (possibly hand-edited) fields.

## Notes

- Uses `gemma2-9b-it` for structured extraction (JSON mode) and
  `llama-3.3-70b-versatile` for free-text reasoning (root cause, CAPA,
  summary, chat) — matches the assignment's mandatory model + fallback.
- Duplicate detection compares against the last 50 saved complaint
  descriptions in Postgres — swap for a real vector/similarity search if
  you want it more robust.
- OCR/production-grade parsing intentionally skipped — the assignment
  brief says this isn't required. `document_parser.py` does plain text
  extraction only.
