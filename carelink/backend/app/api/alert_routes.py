from fastapi import APIRouter, Depends, HTTPException
from app.utils.security import get_current_user
from app.database.repositories import is_authorized_for_case
from app.models.risk_models import AlertReviewRequest
from app.services.alert_service import get_alerts_for_case, review_alert
from app.data import demo_data
from app.utils.logger import log_action
router = APIRouter(prefix="/api/alerts", tags=["alerts"])
@router.get("")
def list_all_alerts(user=Depends(get_current_user)):
    if user["role"] not in ("counsellor", "investigator", "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")
    alerts = list(demo_data.ALERTS.values())
    if user["role"] == "counsellor":
        alerts = [a for a in alerts if a["assignedTo"] == user["userId"]]
    return alerts
@router.get("/{case_id}")
def alerts_for_case(case_id: str, user=Depends(get_current_user)):
    if not is_authorized_for_case(user["userId"], user["role"], case_id):
        raise HTTPException(status_code=403, detail="Not authorized for this case")
    return get_alerts_for_case(case_id)
@router.post("/{alert_id}/review")
def review_alert_route(alert_id: str, payload: AlertReviewRequest, user=Depends(get_current_user)):
    if user["role"] not in ("counsellor", "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to review alerts")
    alert = review_alert(alert_id, payload.status, payload.notes)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    log_action(user["userId"], "ALERT_REVIEWED", alert_id)
    return alert
