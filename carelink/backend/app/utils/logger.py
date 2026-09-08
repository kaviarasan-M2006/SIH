import datetime
from app.data import demo_data
def log_action(actor_id: str, action: str, details: str = ""):
    entry = {"actorId": actor_id, "action": action, "details": details, "timestamp": datetime.datetime.utcnow().isoformat()}
    demo_data.AUDIT_LOGS.append(entry)
    return entry
