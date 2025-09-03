from fastapi import APIRouter, HTTPException, status
from backend.models.user import User
from backend.api.controllers.login import signup_user

router = APIRouter(prefix='/login')

@router.post("/signup")
async def test(user: User):
    if not user.is_guest_user and (not user.email or not user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Not a guest user. Email or password is missing"
        )
    return await signup_user(user)



