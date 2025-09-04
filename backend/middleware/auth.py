from functools import wraps
from typing import Callable

from fastapi import HTTPException, Request
from backend.helper.jwt import decode_jwt_token


def auth_required(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
        if request is None:
            request = kwargs.get("request")

        token = request.headers.get("Authorization")

        try:
            encrypted_token = token.split(" ")[1]   
            request.state.user = decode_jwt_token(encrypted_token)
        except Exception as exc:
            print(str(exc))
            raise HTTPException(status_code=401, detail="Unauthorized")

        return await func(*args, **kwargs)
    return wrapper

