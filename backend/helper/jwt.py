from typing import Dict
from backend.config.settings import get_settings
import jwt

def generate_jwt_token(payload: Dict) -> str:
    return jwt.encode(payload, get_settings().jwt_key, algorithm="HS256")

def decode_jwt_token(token: str) -> Dict:
    return jwt.decode(token, get_settings().jwt_key, algorithms=["HS256"])