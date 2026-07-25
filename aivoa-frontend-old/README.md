# AIVOA — Complaint Intake Frontend

React + Redux Toolkit frontend for the AI-powered pharmaceutical complaint
intake/triage tool. Two-panel layout: complaint form (left) and AI assistant
panel (right) for document upload, text paste, extraction progress, and chat.

## Setup

```bash
npm install
npm run dev
```

Dev server runs on `http://localhost:5173` and proxies `/api/*` to
`http://localhost:8000` (the FastAPI backend).

## Structure

```
src/
  app/store.js                        Redux store
  features/complaint/                 Complaint form slice + component
  features/aiAssistant/               AI panel slice + component
  api/client.js                       Backend contract (single graph endpoint)
  styles/app.css
```

## Backend contract

- `POST /api/complaints/process` — multipart form with `file` or `text`.
  Runs the LangGraph agent end-to-end, returns the full resulting state
  (extracted fields, completeness, risk, etc.) as JSON.
- `POST /api/assistant/ask` — `{ question, context }` → `{ answer }` for the
  chat box.
- `POST /api/complaints` — save the (possibly hand-edited) form fields.
