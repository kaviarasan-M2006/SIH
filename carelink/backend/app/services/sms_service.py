def send_checkin_reminder(user_id: str) -> dict:
    return {"status": "SIMULATED", "message": f"[SIMULATED SMS] Check-in reminder sent to {user_id}."}
def send_alert_notification(staff_id: str, case_id: str) -> dict:
    return {"status": "SIMULATED", "message": f"[SIMULATED SMS] Alert notification for case {case_id} sent to {staff_id}."}
