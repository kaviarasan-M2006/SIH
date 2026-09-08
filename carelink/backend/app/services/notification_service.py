from app.data import demo_data
def notify_counsellor(case_id: str, message: str):
    return {"caseId": case_id, "message": message, "status": "SIMULATED_NOTIFICATION_SENT"}
