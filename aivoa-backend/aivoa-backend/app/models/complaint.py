import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    complaint_source = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)

    product_name = Column(String, nullable=True)
    product_strength_grade = Column(String, nullable=True)
    batch_lot_number = Column(String, nullable=True)
    manufacturing_date = Column(String, nullable=True)
    expiry_date = Column(String, nullable=True)
    quantity_affected = Column(String, nullable=True)

    complaint_type = Column(String, nullable=True)
    complaint_date = Column(String, nullable=True)
    complaint_description = Column(Text, nullable=True)

    initial_severity = Column(String, nullable=True)
    priority = Column(String, nullable=True)

    # AI-derived fields (bonus features land here too)
    completeness_score = Column(Integer, nullable=True)
    risk_classification = Column(String, nullable=True)
    duplicate_of = Column(UUID(as_uuid=True), nullable=True)

    status = Column(String, default="Pending Triage")
    created_at = Column(DateTime, default=datetime.utcnow)
