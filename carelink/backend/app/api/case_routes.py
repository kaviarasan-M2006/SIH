from fastapi import APIRouter, Depends, HTTPException
from app.utils.security import get_current_user
from app.database.repositories import get_case, is_authorized_for_case, find_case_by_victim
from app.data import demo_data
from app.models.case_models import InvestigationUpdateRequest
from app.utils.logger import log_action
import datetime
router = APIRouter(prefix="/api/cases", tags=["cases"])
@router.get("")
def list_cases(user=Depends(get_current_user)):
    role = user["role"]
    uid = user["userId"]
    result = []
    for case_id, case in demo_data.CASES.items():
        if role == "admin" or (role == "investigator" and case["assignedInvestigatorId"] == uid) or (role == "counsellor" and case["assignedCounsellorId"] == uid) or (role == "victim" and case["victimId"] == uid):
            result.append(case)
    return result
@router.get("/{case_id}")
def case_detail(case_id: str, user=Depends(get_current_user)):
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    log_action(user["userId"], "CASE_VIEWED", case_id)
    return case
@router.get("/{case_id}/timeline")
def case_timeline(case_id: str, user=Depends(get_current_user)):
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    return demo_data.TIMELINE.get(case_id, [])
@router.get("/{case_id}/investigation")
def investigation_updates(case_id: str, user=Depends(get_current_user)):
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    if user["role"] == "victim":
        raise HTTPException(status_code=403, detail="Victims cannot access investigation records")
    return demo_data.INVESTIGATION_UPDATES.get(case_id, [])
@router.post("/{case_id}/investigation")
def add_investigation_update(case_id: str, payload: InvestigationUpdateRequest, user=Depends(get_current_user)):
    if user["role"] not in ("investigator", "admin"):
        raise HTTPException(status_code=403, detail="Only investigators can add updates")
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    entry = {
        "date": datetime.datetime.utcnow().strftime("%d/%m/%Y"),
        "status": payload.status, "description": payload.description,
        "nextAction": payload.nextAction, "updatedBy": user["userId"]
    }
    demo_data.INVESTIGATION_UPDATES.setdefault(case_id, []).append(entry)
    demo_data.CASES[case_id]["investigationStatus"] = payload.status
    demo_data.CASES[case_id]["updatedAt"] = datetime.datetime.utcnow().isoformat()
    log_action(user["userId"], "CASE_UPDATED", case_id)
    return entry
@router.get("/{case_id}/audit")
def audit_log(case_id: str, user=Depends(get_current_user)):
    if user["role"] not in ("admin", "investigator"):
        raise HTTPException(status_code=403, detail="Not authorized")
    return [a for a in demo_data.AUDIT_LOGS if a.get("details") == case_id or case_id in str(a.get("details", ""))]
@router.get("/mine/victim")
def my_case(user=Depends(get_current_user)):
    if user["role"] != "victim":
        raise HTTPException(status_code=403, detail="Only victims can access this endpoint")
    case_id = find_case_by_victim(user["userId"])
    if not case_id:
        return {"caseId": None, "message": "No case linked to this demo account yet"}
    return demo_data.CASES[case_id]
