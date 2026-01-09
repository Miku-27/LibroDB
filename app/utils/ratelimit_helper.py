from flask_jwt_extended import get_jwt_identity,verify_jwt_in_request
from flask_limiter.util import get_remote_address

def rate_limit_key():
    if verify_jwt_in_request(optional=True):
        return get_jwt_identity()
    return get_remote_address()