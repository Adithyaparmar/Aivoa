import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.db import Base


class ComplaintAnalysis(Base):
    """AI-derived output from a graph run. Kept separate from Complaint so
    the raw intake data stays untouched and a complaint can be re-analyzed
    without overwriting history."""

    __tablename__ = "complaint_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(
        UUID(as_uuid=True), ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False, index=True
    )

    completeness_score = Column(Integer, nullable=True)
    missing_fields = Column(JSON, nullable=True)  # list[str]

    risk_level = Column(String, nullable=True)
    risk_rationale = Column(Text, nullable=True)

    is_duplicate = Column(Integer, nullable=True)  # 0/1 — kept simple, avoids Boolean dialect quirks
    duplicate_of = Column(UUID(as_uuid=True), ForeignKey("complaints.id"), nullable=True)

    root_cause_suggestion = Column(Text, nullable=True)
    capa_suggestion = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    complaint = relationship(
        "Complaint", back_populates="analyses", foreign_keys=[complaint_id]
    )
