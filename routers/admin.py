from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])

# 🔐 Admin credentials (change here anytime)
ADMIN_EMAIL = "admin@aura.com"
ADMIN_PASSWORD = "adminaura123"

# 📦 Request schema
class LoginRequest(BaseModel):
    email: str
    password: str

# 🚀 Login API
@router.post("/login")
def admin_login(data: LoginRequest):
    if data.email == ADMIN_EMAIL and data.password == ADMIN_PASSWORD:
        return {
            "success": True,
            "message": "Login successful"
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )