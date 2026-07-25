from fastapi import APIRouter

from app.schemas.complaint import AssistantAskRequest, AssistantAskResponse
from app.services.groq_client import call_text

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/ask", response_model=AssistantAskResponse)
def ask_assistant(payload: AssistantAskRequest):
    system = (
        "You are a helpful assistant embedded in a pharmaceutical complaint "
        "intake tool. Answer questions about the complaint currently on "
        "screen, using the provided context. Be concise."
    )
    prompt = f"Question: {payload.question}\n\nComplaint context: {payload.context or {}}"
    answer = call_text(prompt=prompt, system=system)
    return AssistantAskResponse(answer=answer)
