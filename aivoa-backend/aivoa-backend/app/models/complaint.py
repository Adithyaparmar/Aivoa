import uuid
import enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.db import Base


class SeverityLevel(str, enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"


class ComplaintStatus(str, enum.Enum):
    pending_triage = "Pending Triage"
    saved = "Saved"
    under_review = "Under Review"
    closed = "Closed"


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Origin & customer
    complaint_source = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)

    # Product & batch identification
    product_name = Column(String, nullable=True, index=True)
    product_strength_grade = Column(String, nullable=True)
    batch_lot_number = Column(String, nullable=True, index=True)
    manufacturing_date = Column(String, nullable=True)
    expiry_date = Column(String, nullable=True)
    quantity_affected = Column(String, nullable=True)

    # Complaint details
    complaint_type = Column(String, nullable=True)
    complaint_date = Column(String, nullable=True)
    complaint_description = Column(Text, nullable=True)

    # Initial assessment
    initial_severity = Column(Enum(SeverityLevel, name="severity_level"), nullable=True)
    priority = Column(String, nullable=True)

    status = Column(
        Enum(ComplaintStatus, name="complaint_status"),
        default=ComplaintStatus.pending_triage,
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    analyses = relationship(
        "ComplaintAnalysis",
        back_populates="complaint",
        cascade="all, delete-orphan",
        foreign_keys="ComplaintAnalysis.complaint_id",
    )

    __table_args__ = (
        Index("ix_complaints_product_batch", "product_name", "batch_lot_number"),
    )
