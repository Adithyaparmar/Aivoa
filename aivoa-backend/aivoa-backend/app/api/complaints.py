from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.db import get_db
from app.core.config import settings
from app.models.complaint import Complaint
from app.services.document_parser import extract_text
from app.agent.graph import complaint_graph
from app.schemas.complaint import ComplaintFields, ProcessComplaintResponse

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


@router.post("")
def save_complaint(fields: ComplaintFields, db: Session = Depends(get_db)):
    """Persist the (possibly hand-edited) form fields."""
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
        initial_severity=fields.initialSeverity,
        priority=fields.priority,
        status="Saved",
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": str(record.id), "status": record.status}
