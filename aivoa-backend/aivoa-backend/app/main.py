from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app import models  # noqa: F401 — registers all models with Base
from app.api import complaints, assistant

app = FastAPI(title="AIVOA Complaint Intake API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(complaints.router, prefix="/api")
app.include_router(assistant.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
