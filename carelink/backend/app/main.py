from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth_routes, case_routes, checkin_routes, chatbot_routes, risk_routes, evidence_routes, alert_routes, intervention_routes
app = FastAPI(title="Care-Link AI Prototype API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_routes.router)
app.include_router(case_routes.router)
app.include_router(checkin_routes.router)
app.include_router(chatbot_routes.router)
app.include_router(risk_routes.router)
app.include_router(evidence_routes.router)
app.include_router(alert_routes.router)
app.include_router(intervention_routes.router)
@app.get("/")
def root():
    return {"status": "Care-Link AI backend running", "notice": "This is an academic prototype. Do not enter real victim, medical, legal, or personally identifiable information."}
@app.get("/api/health")
def health():
    return {"status": "ok"}
