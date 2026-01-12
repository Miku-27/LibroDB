from flask import request
from flask_limiter.util import get_remote_address
from flask_jwt_extended.utils import decode_token
from flask_jwt_extended.exceptions import JWTExtendedException

def rate_limit_key():
    token = request.cookies.get("access_token_cookie")
    if not token:
        return get_remote_address()

    try:
        decoded = decode_token(token, allow_expired=True)
        user_id = decoded.get("sub")
        if user_id:
            return f"user:{user_id}"
    except JWTExtendedException:
        pass

    return f"ip:{get_remote_address()}"
