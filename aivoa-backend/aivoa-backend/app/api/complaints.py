from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.db import get_db
from app.core.config import settings
from app.models.complaint import Complaint, SeverityLevel, ComplaintStatus
from app.models.analysis import ComplaintAnalysis
from app.services.document_parser import extract_text
from app.agent.graph import complaint_graph
from app.schemas.complaint import ComplaintFields, ProcessComplaintResponse, SaveComplaintRequest

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.post("/process", response_model=ProcessComplaintResponse)
async def process_complaint(
    file: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    """Single contract point with the frontend: takes a file OR raw text,
    runs the full LangGraph agent, returns the complete resulting state."""
    if not file and not text:
        raise HTTPException(400, "Provide either a file or text")

    if file:
        content = await file.read()
        if len(content) > settings.max_upload_mb * 1024 * 1024:
            raise HTTPException(400, f"File exceeds {settings.max_upload_mb}MB limit")
        raw_text = extract_text(file.filename, content)
    else:
        raw_text = text

    # Pull recent complaint descriptions for the duplicate-detection node
    existing = db.execute(
        select(Complaint.complaint_description).limit(50)
    ).scalars().all()

    result = complaint_graph.invoke({
        "raw_text": raw_text,
        "existing_complaints": [c for c in existing if c],
    })

    return ProcessComplaintResponse(
        fields=ComplaintFields(**result.get("fields", {})),
        completeness=result.get("completeness", {}),
        risk=result.get("risk", {}),
        duplicate_check=result.get("duplicate_check"),
        root_cause_suggestion=result.get("root_cause_suggestion"),
        capa_suggestion=result.get("capa_suggestion"),
        summary=result.get("summary"),
    )


def _to_severity(value: str | None) -> SeverityLevel | None:
    if not value:
        return None
    try:
        return SeverityLevel(value)
    except ValueError:
        return None  # AI/user gave something outside the enum — drop rather than crash


@router.post("")
def save_complaint(payload: SaveComplaintRequest, db: Session = Depends(get_db)):
    """Persist the (possibly hand-edited) form fields, plus the AI analysis
    that produced them, if the frontend sends one along."""
    fields = payload.fields

    record = Complaint(
        complaint_source=fields.complaintSource,
        customer_name=fields.customerName,
        product_name=fields.productName,
        product_strength_grade=fields.productStrengthGrade,
        batch_lot_number=fields.batchLotNumber,
        manufacturing_date=fields.manufacturingDate or None,
        expiry_date=fields.expiryDate or None,
        quantity_affected=fields.quantityAffected,
        complaint_type=fields.complaintType,
        complaint_date=fields.complaintDate or None,
        complaint_description=fields.complaintDescription,
        initial_severity=_to_severity(fields.initialSeverity),
        priority=fields.priority,
        status=ComplaintStatus.saved,
    )
    db.add(record)
    db.flush()  # get record.id before commit, so the analysis row can reference it

    if payload.analysis:
        a = payload.analysis
        analysis_record = ComplaintAnalysis(
            complaint_id=record.id,
            completeness_score=(a.completeness or {}).get("score"),
            missing_fields=(a.completeness or {}).get("missing_fields"),
            risk_level=(a.risk or {}).get("level"),
            risk_rationale=(a.risk or {}).get("rationale"),
            is_duplicate=int(bool((a.duplicate_check or {}).get("is_duplicate"))),
            root_cause_suggestion=a.root_cause_suggestion,
            capa_suggestion=a.capa_suggestion,
            summary=a.summary,
        )
        db.add(analysis_record)

    db.commit()
    db.refresh(record)
    return {"id": str(record.id), "status": record.status.value}
