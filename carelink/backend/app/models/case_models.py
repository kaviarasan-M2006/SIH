from pydantic import BaseModel
from typing import Optional
class InvestigationUpdateRequest(BaseModel):
    status: str
    description: str
    nextAction: str
class InterventionRequest(BaseModel):
    type: str
    action: str
    followUpDate: Optional[str] = None
    notes: Optional[str] = None
class EvidenceMetaRequest(BaseModel):
    type: str
    description: str
