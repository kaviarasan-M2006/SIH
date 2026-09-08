from fastapi import APIRouter, Depends, HTTPException
from app.utils.security import get_current_user
from app.database.repositories import is_authorized_for_case
from app.data import demo_data
router = APIRouter(prefix="/api/risk", tags=["risk"])
@router.get("/{case_id}")
def get_risk_summary(case_id: str, user=Depends(get_current_user)):
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    case = demo_data.CASES.get(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    history = demo_data.RISK_HISTORY.get(case_id, [])
    return {
        "caseId": case_id, "score": case["latestScore"], "riskLevel": case["latestRiskLevel"],
        "trend": case["trend"], "history": history,
        "disclaimer": "Experimental non-clinical prototype thresholds. AI does not diagnose mental illness."
    }
@router.get("/{case_id}/trend")
def get_trend(case_id: str, user=Depends(get_current_user)):
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    history = demo_data.RISK_HISTORY.get(case_id, [])
    labeled = [{"week": f"Week {i+1}", "score": score} for i, score in enumerate(history)]
    return {"caseId": case_id, "points": labeled, "trend": demo_data.CASES[case_id]["trend"]}
