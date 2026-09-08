from app.data import demo_data
import datetime
def add_evidence(case_id: str, evidence_type: str, description: str, uploaded_by: str):
    existing = demo_data.EVIDENCE.get(case_id, [])
    evidence_id = f"EV-{len(existing)+1:03d}"
    item = {
        "evidenceId": evidence_id, "type": evidence_type, "description": description,
        "uploadedBy": uploaded_by, "uploadedAt": datetime.datetime.utcnow().isoformat(),
        "status": "Pending Verification", "caseId": case_id
    }
    existing.append(item)
    demo_data.EVIDENCE[case_id] = existing
    return item
def get_evidence(case_id: str):
    return demo_data.EVIDENCE.get(case_id, [])
