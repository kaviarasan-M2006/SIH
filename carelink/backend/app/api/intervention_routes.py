from fastapi import APIRouter, Depends, HTTPException
from app.utils.security import get_current_user
from app.database.repositories import is_authorized_for_case
from app.models.case_models import InterventionRequest
from app.data import demo_data
from app.utils.logger import log_action
import datetime
router = APIRouter(prefix="/api/interventions", tags=["interventions"])
@router.get("/{case_id}")
def list_interventions(case_id: str, user=Depends(get_current_user)):
    if user["role"] == "victim":
        raise HTTPException(status_code=403, detail="Not authorized")
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    return demo_data.INTERVENTIONS.get(case_id, [])
@router.post("/{case_id}")
def add_intervention(case_id: str, payload: InterventionRequest, user=Depends(get_current_user)):
    if user["role"] not in ("counsellor", "admin"):
        raise HTTPException(status_code=403, detail="Only counsellors can record interventions")
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    entry = {
        "type": payload.type, "date": datetime.datetime.utcnow().strftime("%d/%m/%Y"),
        "staffId": user["userId"], "action": payload.action, "followUpDate": payload.followUpDate,
        "status": "Scheduled" if payload.followUpDate else "Completed", "notes": payload.notes or ""
    }
    demo_data.INTERVENTIONS.setdefault(case_id, []).append(entry)
    log_action(user["userId"], "INTERVENTION_CREATED", case_id)
    return entry
