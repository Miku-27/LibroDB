from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import request, redirect, url_for
from flask_limiter import Limiter
from app.utils.ratelimit_helper import rate_limit_key
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


rate_limiter = Limiter(
    key_func=rate_limit_key, 
)

@jwt.unauthorized_loader
def custom_unauthorized(reason):
    if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
        return {
            "success": False,
            "msg": "Authentication token missing or invalid",
            "data":None
        }, 401
    else:
        return redirect(url_for("pages.view.login"))


@jwt.expired_token_loader
def custom_expired(jwt_header, jwt_payload):
    if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
        return {
        "success": False,
        "msg": "Your session has expired. Please log in again.",
        "data": None
        }, 401
    else:
        return redirect(url_for("pages.view.login"))