from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.utils.security import get_current_user
router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])
class ChatRequest(BaseModel):
    message: str
    language: str = "en"
RESPONSES = {
    "en": {
        "greeting": "Hello, I am the Care-Link Support Assistant. How are you feeling today?",
        "wellbeing_check": "Would you like to complete a wellbeing check-in now?",
        "stress": "I understand things may feel stressful. Would you like to talk to a counsellor?",
        "fear": "I'm sorry you're feeling afraid. Do you feel unsafe right now?",
        "threat_report": "Thank you for sharing this. A member of the support team will be notified for human review.",
        "need_counsellor": "I can connect you with a counsellor. Would you like me to request a callback?",
        "need_support": "You are not alone. I can help you request support from the team.",
        "legal_support": "Legal support information is available. An investigator or legal aid contact can guide you.",
        "emergency_help": "If you are in immediate danger, please contact local emergency services right away.",
        "privacy": "Your information is protected and only shared with authorized personnel on your case.",
        "consent": "You may review or update your consent preferences anytime in Privacy & Consent.",
        "general_support": "I'm here to help. Could you tell me a little more?"
    },
    "ta": {
        "greeting": "வணக்கம், நான் கேர்-லிங்க் ஆதரவு உதவியாளர். இன்று நீங்கள் எப்படி உணர்கிறீர்கள்?",
        "wellbeing_check": "இப்போது ஒரு நல்வாழ்வு சரிபார்ப்பை பூர்த்தி செய்ய விரும்புகிறீர்களா?",
        "stress": "விஷயங்கள் மன அழுத்தமாக உணரப்படலாம் என்பதை புரிந்துகொள்கிறேன். ஆலோசகருடன் பேச விரும்புகிறீர்களா?",
        "fear": "நீங்கள் பயமாக உணர்வது வருந்தத்தக்கது. இப்போது பாதுகாப்பற்றதாக உணர்கிறீர்களா?",
        "threat_report": "இதைப் பகிர்ந்தமைக்கு நன்றி. மனித மறுஆய்வுக்காக ஆதரவு குழுவினருக்கு தெரிவிக்கப்படும்.",
        "need_counsellor": "நான் உங்களை ஒரு ஆலோசகருடன் இணைக்க முடியும். திரும்ப அழைப்பு கோர வேண்டுமா?",
        "need_support": "நீங்கள் தனியாக இல்லை. குழுவிடமிருந்து ஆதரவு கோர உதவ முடியும்.",
        "legal_support": "சட்ட உதவி தகவல் கிடைக்கிறது. புலனாய்வாளர் அல்லது சட்ட உதவி தொடர்பு உங்களுக்கு வழிகாட்ட முடியும்.",
        "emergency_help": "நீங்கள் உடனடி ஆபத்தில் இருந்தால், உடனடியாக உள்ளூர் அவசர சேவைகளை தொடர்பு கொள்ளவும்.",
        "privacy": "உங்கள் தகவல் பாதுகாக்கப்படுகிறது மற்றும் அங்கீகரிக்கப்பட்ட பணியாளர்களுடன் மட்டுமே பகிரப்படுகிறது.",
        "consent": "உங்கள் ஒப்புதல் விருப்பங்களை எப்போது வேண்டுமானாலும் தனியுரிமை மற்றும் ஒப்புதலில் மதிப்பாய்வு செய்யலாம்.",
        "general_support": "நான் உதவ இங்கு இருக்கிறேன். இன்னும் கொஞ்சம் சொல்ல முடியுமா?"
    }
}
KEYWORDS = {
    "greeting": ["hi", "hello", "vanakkam"],
    "stress": ["stress", "stressed", "pressure"],
    "fear": ["afraid", "scared", "fear"],
    "threat_report": ["threat", "threatened", "following me", "watching me"],
    "need_counsellor": ["counsellor", "talk to someone", "speak to counsellor"],
    "need_support": ["support", "help me", "need help"],
    "legal_support": ["legal", "court", "fir", "lawyer"],
    "emergency_help": ["emergency", "danger", "unsafe now"],
    "privacy": ["privacy", "data protection"],
    "consent": ["consent"]
}
def detect_intent(message: str) -> str:
    lowered = message.lower()
    for intent, words in KEYWORDS.items():
        if any(w in lowered for w in words):
            return intent
    return "general_support"
@router.post("/message")
def chat_message(payload: ChatRequest, user=Depends(get_current_user)):
    intent = detect_intent(payload.message)
    lang = payload.language if payload.language in RESPONSES else "en"
    reply = RESPONSES[lang].get(intent, RESPONSES[lang]["general_support"])
    return {"intent": intent, "reply": reply}
