from app.data import demo_data
def get_case(case_id: str):
    return demo_data.CASES.get(case_id)
def is_authorized_for_case(user_id: str, role: str, case_id: str) -> bool:
    case = get_case(case_id)
    if not case:
        return False
    if role == "admin":
        return True
    if role == "investigator":
        return case["assignedInvestigatorId"] == user_id
    if role == "counsellor":
        return case["assignedCounsellorId"] == user_id
    if role == "victim":
        return case["victimId"] == user_id
    return False
def find_case_by_victim(victim_id: str):
    for case_id, case in demo_data.CASES.items():
        if case["victimId"] == victim_id:
            return case_id
    return None
