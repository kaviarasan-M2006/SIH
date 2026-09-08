def trigger_ivrs_call(user_id: str) -> dict:
    return {"status": "SIMULATED", "message": f"[SIMULATED IVRS] Automated wellbeing call queued for {user_id}."}
