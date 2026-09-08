from pydantic import BaseModel
class AlertReviewRequest(BaseModel):
    status: str
    notes: str = ""
