# Care-Link AI

AI-Powered Dynamic Mental Health Monitoring, Distress Risk Prediction & Case Management System for Victims and Witnesses of Atrocities.

## 1. Problem Statement

Victims and witnesses of serious crimes often disengage from the justice process due to unmonitored psychological distress, fear, and lack of coordinated support between investigation, legal, and counselling teams.

## 2. Existing Solution Gaps

Chatbots, sentiment analysis, case management tools, and counselling services already exist, but operate in silos and are not linked to a single case record accessible to authorized roles.

## 3. Proposed Solution

A single, role-based web platform that connects case registration, investigation, evidence, wellbeing check-ins, AI-based distress indicators, alerts, and human intervention into one unified case timeline.

## 4. Innovation

Integration of existing techniques (NLP sentiment signals, rule-based risk scoring, case management) into one case-linked, explainable, human-in-the-loop system rather than a new detection algorithm.

## 5. Features

- Role-based single application (Victim, Counsellor, Investigator, Administrator)
- Unified case dashboard with tabs: Overview, Case Details, Investigation, Evidence, Wellbeing, AI Risk, Alerts, Interventions, Timeline, Audit Log
- Periodic wellbeing check-ins (English and Tamil)
- Transparent, explainable distress risk scoring (non-clinical, non-diagnostic)
- Non-response monitoring with human-review escalation
- Internal alert system with severity levels
- Intervention and follow-up recording
- Investigation update logging
- Evidence metadata management (non-public storage)
- Simulated SMS/IVRS service interfaces
- Full audit logging of key actions

## 6. Architecture

React (Vite) frontend calls a FastAPI backend over REST. The backend uses an in-memory demo data layer for this prototype (structured to mirror Firebase Firestore collections) and issues JWT session tokens after login. Firebase Authentication/Firestore/Storage integration points are stubbed and ready to be wired in for production use.

## 7. Technology Stack

Frontend: React, Vite, JavaScript, Recharts
Backend: Python, FastAPI, Pydantic, Uvicorn, PyJWT
AI/ML: NumPy, Pandas, Scikit-learn, Joblib (transparent rule-based engine now; ML-ready structure)
Database (production target): Firebase Firestore
Auth (production target): Firebase Authentication
Storage (production target): Firebase Storage

## 8. Database Structure (Firestore Collections)

users, cases, checkins, risk_scores, alerts, evidence, statements, investigation_updates, legal_updates, compensation, interventions, audit_logs, notifications

Field structures for `users`, `cases`, `checkins`, `risk_scores`, `evidence`, and `alerts` are documented in the original specification and mirrored in `backend/app/data/demo_data.py`.

## 9. Security

- JWT-based session tokens, no plaintext password storage in production (Firebase Authentication)
- Server-side authorization checks on every case-scoped endpoint (`is_authorized_for_case`)
- Role-restricted access to investigation, evidence, and audit data
- No public evidence URLs
- Firestore security rules should deny-by-default; never use `allow read, write: if true;`

## 10. AI Methodology

The risk engine (`backend/app/ai/risk_engine.py`) computes a 0-100 distress score from mood, sleep, stress, safety concern, support request, sentiment/threat text signals, score trend, and missed check-in history. Thresholds (LOW/MODERATE/HIGH/CRITICAL) are explicitly labelled as experimental, non-clinical prototype thresholds. The system never outputs a diagnosis; it only recommends human review.

## 11. Installation

Requires Python 3.10+ and Node.js 18+.

## 12. Firebase Setup (Production Path)

1. Create a Firebase project.
2. Enable Authentication, Firestore, and Storage.
3. Download a service account key and set `FIREBASE_CREDENTIALS_PATH` in `backend/.env`.
4. Replace the in-memory demo data layer with Firestore reads/writes in `backend/app/database/`.

## 13. Backend Setup

```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 14. Frontend Setup

```
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `http://localhost:8000` (see `frontend/src/services/api.js`).

## 15. Demo Credentials

All demo accounts use password `demo123`.

- Victim: victim.demo@example.com
- Counsellor: counsellor.demo@example.com
- Investigator: investigator.demo@example.com
- Administrator: admin.demo@example.com

## 16. Testing

Suggested test coverage (add under `backend/tests/`):

- Risk engine: low/moderate/high/critical classification, improving/stable/worsening trend, non-response penalty
- Authorization: victim accessing another case, counsellor accessing unassigned case, investigator accessing unauthorized case
- API: valid/invalid check-in submission, risk calculation, alert creation, case lookup

## 17. Limitations

- In-memory data resets on server restart (Firestore integration required for persistence)
- Sentiment analysis is keyword-based for transparency, not a trained NLP model
- No real SMS/IVRS integration; interfaces are simulated
- Not validated for clinical or legal decision-making

## 18. Future Scope

- Replace in-memory store with Firestore
- Integrate a trained, explainable ML model behind the same risk engine interface
- Real SMS/IVRS provider integration
- Expand language support beyond English and Tamil
- Fine-grained, field-level permission rules in Firestore Security Rules

## Important Notice

This is an academic prototype. Do not enter real victim, medical, legal, or personally identifiable information. The AI components are decision-support and early-warning tools only; they do not diagnose mental illness and do not determine guilt, innocence, credibility, legal outcomes, or evidence authenticity. Human professionals remain responsible for all such decisions.
