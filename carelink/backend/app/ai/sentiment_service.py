from typing import Dict
NEGATIVE_WORDS = ["sad", "hopeless", "worthless", "alone", "tired", "exhausted", "cry", "crying", "bad", "worse", "difficult", "hurt", "pain"]
FEAR_WORDS = ["scared", "afraid", "fear", "frightened", "terrified", "nervous", "anxious", "worried"]
STRESS_WORDS = ["stressed", "overwhelmed", "pressure", "anxious", "tension", "burden"]
THREAT_WORDS = ["threat", "threatened", "warned", "follow", "following", "watching", "harm", "hurt me", "kill", "attack"]
HELP_WORDS = ["help", "support", "need someone", "talk to someone", "counsellor", "assist"]
def normalize(count: int, cap: int = 3) -> float:
    return round(min(count, cap) / cap, 2)
def analyze_text(text: str) -> Dict:
    if not text:
        return {"negative_sentiment": 0.0, "fear_signal": 0.0, "stress_signal": 0.0, "threat_signal": 0.0, "help_signal": 0.0}
    lowered = text.lower()
    neg_count = sum(1 for w in NEGATIVE_WORDS if w in lowered)
    fear_count = sum(1 for w in FEAR_WORDS if w in lowered)
    stress_count = sum(1 for w in STRESS_WORDS if w in lowered)
    threat_count = sum(1 for w in THREAT_WORDS if w in lowered)
    help_count = sum(1 for w in HELP_WORDS if w in lowered)
    return {
        "negative_sentiment": normalize(neg_count),
        "fear_signal": normalize(fear_count),
        "stress_signal": normalize(stress_count),
        "threat_signal": normalize(threat_count),
        "help_signal": normalize(help_count),
        "disclaimer": "Sentiment analysis is only one signal and cannot determine mental health status."
    }
