import datetime
def now_iso():
    return datetime.datetime.utcnow().isoformat()
USERS = {
    "victim.demo@example.com": {"userId": "V-2001", "password": "demo123", "role": "victim", "displayName": "Demo Victim", "preferredLanguage": "en", "consentStatus": "granted"},
    "counsellor.demo@example.com": {"userId": "C-3001", "password": "demo123", "role": "counsellor", "displayName": "Demo Counsellor", "preferredLanguage": "en"},
    "investigator.demo@example.com": {"userId": "INV-004", "password": "demo123", "role": "investigator", "displayName": "Demo Investigator", "preferredLanguage": "en"},
    "admin.demo@example.com": {"userId": "A-9001", "password": "demo123", "role": "admin", "displayName": "Demo Admin", "preferredLanguage": "en"}
}
CASE_STAGES = ["Registered", "Under Investigation", "Evidence Review", "Court Proceedings", "Closed"]
RISK_SEED = {
    "CL-1001": "LOW", "CL-1002": "MODERATE", "CL-1003": "HIGH", "CL-1004": "LOW", "CL-1005": "CRITICAL",
    "CL-1006": "MODERATE", "CL-1007": "HIGH", "CL-1008": "LOW", "CL-1009": "MODERATE", "CL-1010": "HIGH"
}
LEVEL_SCORE = {"LOW": 18, "MODERATE": 40, "HIGH": 68, "CRITICAL": 88}
def build_cases():
    cases = {}
    for i, (case_id, level) in enumerate(RISK_SEED.items(), start=1):
        score = LEVEL_SCORE[level]
        cases[case_id] = {
            "caseId": case_id,
            "victimId": f"V-{2000+i}",
            "assignedInvestigatorId": "INV-004",
            "assignedCounsellorId": "C-3001",
            "caseStage": CASE_STAGES[min(i % len(CASE_STAGES), len(CASE_STAGES)-1)],
            "status": "Under Investigation" if level != "CRITICAL" else "Under Investigation - Priority",
            "location": "Fictional District " + str(i),
            "incidentCategory": "Demo Category " + str((i % 4) + 1),
            "firReference": f"FIR-{1000+i}",
            "investigationStatus": "In Progress",
            "courtStatus": "Pending",
            "compensationStatus": "Under Review",
            "createdAt": now_iso(),
            "updatedAt": now_iso(),
            "latestScore": score,
            "latestRiskLevel": level,
            "trend": "Stable"
        }
    return cases
CASES = build_cases()
def build_timeline():
    timeline = {}
    base_events = [
        ("05 Jan 2026", "Complaint registered"),
        ("07 Jan 2026", "FIR registered"),
        ("10 Jan 2026", "Investigation started"),
        ("15 Jan 2026", "Victim statement recorded"),
        ("18 Jan 2026", "Evidence uploaded"),
        ("02 Feb 2026", "Witness statement recorded"),
        ("15 Feb 2026", "Threat reported"),
        ("20 Feb 2026", "Wellbeing check-in completed"),
        ("25 Feb 2026", "Risk level increased"),
        ("01 Mar 2026", "Counsellor intervention"),
        ("10 Mar 2026", "Investigation update")
    ]
    for case_id in CASES:
        timeline[case_id] = [{"date": d, "event": e} for d, e in base_events]
    return timeline
TIMELINE = build_timeline()
EVIDENCE = {
    case_id: [
        {"evidenceId": f"EV-{idx}01", "type": "Document", "description": "Case-related document", "uploadedBy": "INV-004", "uploadedAt": now_iso(), "status": "Verified", "caseId": case_id},
        {"evidenceId": f"EV-{idx}02", "type": "Statement", "description": "Recorded statement transcript", "uploadedBy": "INV-004", "uploadedAt": now_iso(), "status": "Verified", "caseId": case_id}
    ] for idx, case_id in enumerate(CASES, start=1)
}
CHECKINS = {case_id: [] for case_id in CASES}
RISK_HISTORY = {case_id: [LEVEL_SCORE[RISK_SEED[case_id]] - 15, LEVEL_SCORE[RISK_SEED[case_id]] - 8, LEVEL_SCORE[RISK_SEED[case_id]]] for case_id in CASES}
ALERTS = {}
alert_counter = 1
for case_id, level in RISK_SEED.items():
    if level in ("HIGH", "CRITICAL"):
        ALERTS[f"AL-{alert_counter:03d}"] = {
            "alertId": f"AL-{alert_counter:03d}",
            "caseId": case_id,
            "severity": "URGENT" if level == "CRITICAL" else "HIGH",
            "reason": "Significant increase in distress indicators.",
            "signals": ["Stress increased", "Poor sleep", "Safety concern", "Worsening trend"],
            "status": "pending",
            "assignedTo": "C-3001",
            "createdAt": now_iso(),
            "reviewedAt": None
        }
        alert_counter += 1
INTERVENTIONS = {case_id: [] for case_id in CASES}
INVESTIGATION_UPDATES = {case_id: [] for case_id in CASES}
AUDIT_LOGS = []
