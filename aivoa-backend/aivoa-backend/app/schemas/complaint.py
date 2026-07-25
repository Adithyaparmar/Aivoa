from typing import Optional
from pydantic import BaseModel


class ComplaintFields(BaseModel):
    complaintSource: Optional[str] = None
    customerName: Optional[str] = None
    productName: Optional[str] = None
    productStrengthGrade: Optional[str] = None
    batchLotNumber: Optional[str] = None
    manufacturingDate: Optional[str] = None
    expiryDate: Optional[str] = None
    quantityAffected: Optional[str] = None
    complaintType: Optional[str] = None
    complaintDate: Optional[str] = None
    complaintDescription: Optional[str] = None
    initialSeverity: Optional[str] = None
    priority: Optional[str] = None


class ProcessComplaintResponse(BaseModel):
    fields: ComplaintFields
    completeness: dict
    risk: dict
    duplicate_check: Optional[dict] = None
    root_cause_suggestion: Optional[str] = None
    capa_suggestion: Optional[str] = None
    summary: Optional[str] = None


class AnalysisPayload(BaseModel):
    completeness: Optional[dict] = None
    risk: Optional[dict] = None
    duplicate_check: Optional[dict] = None
    root_cause_suggestion: Optional[str] = None
    capa_suggestion: Optional[str] = None
    summary: Optional[str] = None


class SaveComplaintRequest(BaseModel):
    fields: ComplaintFields
    analysis: Optional[AnalysisPayload] = None


class AssistantAskRequest(BaseModel):
    question: str
    context: Optional[dict] = None


class AssistantAskResponse(BaseModel):
    answer: str
