from backend.models.user import User, save_user
from typing import Dict
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from backend.helper.jwt import generate_jwt_token
import bcrypt
import uuid

async def signup_user(user: User) -> JSONResponse:
    try:
        if user.is_guest_user:
            return await signup_guest_user(user)
    
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = User(email=user.email, password=hashed_password)
        await save_user(new_user)
        response = JSONResponse(
            content={
                "message": "User signup successful",
                "isSuccess": True
            },
            status_code=201
        )

        response.set_cookie(key="jwt-token", value=generate_jwt_token({ 
            "email": user.email,
            "isGuestUser": user.is_guest_user
        }))

        return response
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )
    
async def signup_guest_user(user: User) -> JSONResponse:
    try:
        user.email = f"{str(uuid.uuid4())}@resumeplusplus.com"
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        await save_user(user)

        response = JSONResponse(
            content={
                "message": "User signup successful",
                "isSuccess": True
            },
            status_code=201
        )

        response.set_cookie(key="jwt-token", value=generate_jwt_token({ 
            "email": user.email,
            "isGuestUser": user.is_guest_user
        }))

        return response
    except Exception as exc:
        raise exc
    
def verify_user() -> JSONResponse:
    return JSONResponse(
        content={
            "isSuccess": True
        },
        status_code=200
    )