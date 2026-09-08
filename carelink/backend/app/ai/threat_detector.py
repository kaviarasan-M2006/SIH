from typing import Dict
CRITICAL_PHRASES = ["going to hurt", "going to kill", "coming after", "found my house", "know where i live"]
def detect_threat_escalation(text: str) -> Dict:
    if not text:
        return {"escalation_detected": False, "matched_phrases": []}
    lowered = text.lower()
    matched = [p for p in CRITICAL_PHRASES if p in lowered]
    return {"escalation_detected": len(matched) > 0, "matched_phrases": matched}
