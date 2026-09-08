from pydantic import BaseModel
from typing import Optional
class CheckinRequest(BaseModel):
    caseId: str
    mood: str
    sleep: str
    stressLevel: int
    safetyConcern: str
    supportRequested: str
    optionalMessage: Optional[str] = ""
