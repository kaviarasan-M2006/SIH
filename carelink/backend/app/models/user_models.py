from pydantic import BaseModel
class LoginRequest(BaseModel):
    email: str
    password: str
    role: str
class LoginResponse(BaseModel):
    token: str
    userId: str
    role: str
    displayName: str
    preferredLanguage: str
