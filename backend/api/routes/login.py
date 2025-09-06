from fastapi import APIRouter, HTTPException, status, Request
from backend.models.user import User
from backend.api.controllers.login import signup_user, verify_user
from backend.middleware.auth import auth_required

router = APIRouter(prefix='/auth')

@router.post("/signup")
async def signup(user: User):
    if not user.is_guest_user or (not user.email or not user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Not a guest user. Email or password is missing"
        )
    return await signup_user(user)

@router.get("/verify")
@auth_required
async def test(request: Request):
    return verify_user()
