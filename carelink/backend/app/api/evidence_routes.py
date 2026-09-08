from fastapi import APIRouter, Depends, HTTPException
from app.utils.security import get_current_user
from app.database.repositories import is_authorized_for_case
from app.models.case_models import EvidenceMetaRequest
from app.services.evidence_service import add_evidence, get_evidence
from app.utils.logger import log_action
router = APIRouter(prefix="/api/evidence", tags=["evidence"])
@router.get("/{case_id}")
def list_evidence(case_id: str, user=Depends(get_current_user)):
    if user["role"] == "victim":
        raise HTTPException(status_code=403, detail="Victims cannot access evidence records")
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    log_action(user["userId"], "EVIDENCE_VIEWED", case_id)
    return get_evidence(case_id)
@router.post("/{case_id}")
def upload_evidence(case_id: str, payload: EvidenceMetaRequest, user=Depends(get_current_user)):
    if user["role"] not in ("investigator", "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to upload evidence")
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    item = add_evidence(case_id, payload.type, payload.description, user["userId"])
    log_action(user["userId"], "EVIDENCE_UPLOADED", case_id)
    return item
