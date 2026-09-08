from fastapi import APIRouter, HTTPException
from app.models.user_models import LoginRequest, LoginResponse
from app.data import demo_data
from app.utils.security import create_token
from app.utils.logger import log_action
router = APIRouter(prefix="/api/auth", tags=["auth"])
@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    user = demo_data.USERS.get(payload.email)
    if not user or user["password"] != payload.password or user["role"] != payload.role:
        raise HTTPException(status_code=401, detail="Invalid credentials or role mismatch")
    token = create_token(user["userId"], user["role"])
    log_action(user["userId"], "LOGIN", f"role={user['role']}")
    return LoginResponse(token=token, userId=user["userId"], role=user["role"], displayName=user["displayName"], preferredLanguage=user.get("preferredLanguage", "en"))
