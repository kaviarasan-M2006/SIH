from app.data import demo_data
import datetime
def create_alert(case_id: str, severity: str, reason: str, signals: list, assigned_to: str = None):
    alert_id = f"AL-{len(demo_data.ALERTS)+1:03d}"
    alert = {
        "alertId": alert_id, "caseId": case_id, "severity": severity, "reason": reason,
        "signals": signals, "status": "pending", "assignedTo": assigned_to,
        "createdAt": datetime.datetime.utcnow().isoformat(), "reviewedAt": None
    }
    demo_data.ALERTS[alert_id] = alert
    return alert
def review_alert(alert_id: str, status: str, notes: str = ""):
    alert = demo_data.ALERTS.get(alert_id)
    if not alert:
        return None
    alert["status"] = status
    alert["reviewedAt"] = datetime.datetime.utcnow().isoformat()
    alert["reviewNotes"] = notes
    return alert
def get_alerts_for_case(case_id: str):
    return [a for a in demo_data.ALERTS.values() if a["caseId"] == case_id]
