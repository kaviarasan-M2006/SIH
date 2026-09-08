from typing import List, Dict
MOOD_MAP = {"very_good": 0, "good": 1, "okay": 3, "difficult": 6, "very_difficult": 9}
SLEEP_MAP = {"normal": 0, "slightly_disturbed": 2, "frequently_disturbed": 5, "very_difficult": 8}
SAFETY_MAP = {"no": 0, "not_sure": 5, "yes": 12}
SUPPORT_MAP = {"no": 0, "maybe": 1, "yes": 2}
def classify(score: float) -> str:
    if score <= 24: return "LOW"
    if score <= 49: return "MODERATE"
    if score <= 74: return "HIGH"
    return "CRITICAL"
def missed_checkin_penalty(consecutive_missed: int) -> float:
    if consecutive_missed <= 0: return 0
    if consecutive_missed == 1: return 2
    if consecutive_missed == 2: return 6
    return 12
def calculate_risk(checkin: Dict, previous_score: float, history_scores: List[float], sentiment_signals: Dict, consecutive_missed: int = 0) -> Dict:
    indicators = []
    mood_val = MOOD_MAP.get(checkin.get("mood", "okay"), 3)
    sleep_val = SLEEP_MAP.get(checkin.get("sleep", "normal"), 0)
    stress_val = min(max(checkin.get("stressLevel", 0), 0), 10)
    safety_val = SAFETY_MAP.get(checkin.get("safetyConcern", "no"), 0)
    support_val = SUPPORT_MAP.get(checkin.get("supportRequested", "no"), 0)
    base = (mood_val * 2.2) + (sleep_val * 2.0) + (stress_val * 2.5) + safety_val + (support_val * 1.5)
    fear = sentiment_signals.get("fear_signal", 0) * 10
    threat = sentiment_signals.get("threat_signal", 0) * 14
    negative = sentiment_signals.get("negative_sentiment", 0) * 8
    help_signal = sentiment_signals.get("help_signal", 0) * 6
    signal_component = fear + threat + negative + help_signal
    trend_component = 0
    if history_scores:
        avg_recent = sum(history_scores[-3:]) / len(history_scores[-3:])
        if avg_recent > previous_score:
            trend_component = min((avg_recent - previous_score) * 0.5, 10)
    missed_component = missed_checkin_penalty(consecutive_missed)
    if consecutive_missed >= 3 and checkin.get("hasThreatHistory"):
        missed_component += 8
    raw_score = base + signal_component + trend_component + missed_component
    smoothed = (raw_score * 0.7) + (previous_score * 0.3)
    final_score = round(min(max(smoothed, 0), 100), 1)
    if stress_val >= 7: indicators.append("Stress level reported high")
    if sleep_val >= 5: indicators.append("Sleep significantly disturbed")
    if safety_val >= 12: indicators.append("User reported feeling unsafe")
    if safety_val == 5: indicators.append("User uncertain about safety")
    if threat > 0: indicators.append("Threat-related language detected in message")
    if fear > 0: indicators.append("Fear-related signals detected")
    if trend_component > 0: indicators.append("Distress indicators increased over recent check-ins")
    if consecutive_missed >= 2: indicators.append("Multiple consecutive missed check-ins")
    if not indicators: indicators.append("No significant elevated indicators this cycle")
    trend_label = "Stable"
    if history_scores:
        if final_score > previous_score + 5: trend_label = "Worsening"
        elif final_score < previous_score - 5: trend_label = "Improving"
    return {
        "score": final_score,
        "riskLevel": classify(final_score),
        "indicators": indicators,
        "trend": trend_label,
        "modelVersion": "prototype-v1-transparent",
        "disclaimer": "Experimental non-clinical prototype thresholds. AI does not diagnose mental illness.",
        "recommendedAction": "Human counsellor/case-worker review recommended." if classify(final_score) in ("HIGH", "CRITICAL") else "Continue routine monitoring."
    }
