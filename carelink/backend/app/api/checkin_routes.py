from fastapi import APIRouter, Depends, HTTPException
from app.models.checkin_models import CheckinRequest
from app.utils.security import get_current_user
from app.database.repositories import is_authorized_for_case
from app.data import demo_data
from app.ai.sentiment_service import analyze_text
from app.ai.threat_detector import detect_threat_escalation
from app.ai.risk_engine import calculate_risk
from app.services.alert_service import create_alert
from app.utils.logger import log_action
import datetime
router = APIRouter(prefix="/api/checkins", tags=["checkins"])
@router.post("")
def submit_checkin(payload: CheckinRequest, user=Depends(get_current_user)):
    if not is_authorized_for_case(user["userId"], user["role"], payload.caseId):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    checkin_record = payload.dict()
    checkin_record["createdAt"] = datetime.datetime.utcnow().isoformat()
    demo_data.CHECKINS.setdefault(payload.caseId, []).append(checkin_record)
    sentiment = analyze_text(payload.optionalMessage or "")
    threat_check = detect_threat_escalation(payload.optionalMessage or "")
    history = demo_data.RISK_HISTORY.get(payload.caseId, [])
    previous_score = history[-1] if history else 0
    risk_input = checkin_record.copy()
    risk_input["hasThreatHistory"] = threat_check["escalation_detected"]
    result = calculate_risk(risk_input, previous_score, history, sentiment, consecutive_missed=0)
    demo_data.RISK_HISTORY.setdefault(payload.caseId, []).append(result["score"])
    demo_data.CASES[payload.caseId]["latestScore"] = result["score"]
    demo_data.CASES[payload.caseId]["latestRiskLevel"] = result["riskLevel"]
    demo_data.CASES[payload.caseId]["trend"] = result["trend"]
    log_action(user["userId"], "CHECKIN_SUBMITTED", payload.caseId)
    log_action(user["userId"], "RISK_CALCULATED", payload.caseId)
    if result["riskLevel"] in ("HIGH", "CRITICAL"):
        severity = "URGENT" if result["riskLevel"] == "CRITICAL" else "HIGH"
        alert = create_alert(payload.caseId, severity, "Significant increase in distress indicators.", result["indicators"], demo_data.CASES[payload.caseId]["assignedCounsellorId"])
        log_action(user["userId"], "ALERT_CREATED", payload.caseId)
    return {"checkin": checkin_record, "risk": result, "sentiment": sentiment}
@router.get("/{case_id}")
def get_checkins(case_id: str, user=Depends(get_current_user)):
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    return demo_data.CHECKINS.get(case_id, [])
