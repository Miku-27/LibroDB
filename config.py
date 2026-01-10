import os
from datetime import timedelta

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "200 per day")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_TOKEN_NAME = "access_token"

    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_METHODS = ["POST", "PUT", "DELETE", "PATCH"]
    JWT_CSRF_CHECK_FORM = False
    JWT_COOKIE_SECURE = False

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    TALISMAN_ENABLED = True
    TALISMAN_FORCED_HTTPS = False
    TALISMAN_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    TALISMAN_FRAME_OPTIONS = "DENY"

    TALISMAN_CSP = {
        "default-src": ["'self'"],
        "img-src": [
            "'self'", 
            "books.google.com", 
            "*.googleusercontent.com"
        ],

        "style-src": [
            "'self'", 
            "fonts.googleapis.com"
        ],
        "font-src": [
            "'self'", 
            "fonts.gstatic.com"
        ],
    }

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    JWT_COOKIE_SECURE = False
    TALISMAN_ENABLED = False
    TALISMAN_FORCED_HTTPS = False
    

class ProductionConfig(BaseConfig):
    DEBUG = False
    JWT_COOKIE_SECURE = True
    TALISMAN_ENABLED = True
    TALISMAN_FORCED_HTTPS = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "connect_args": {
            "ssl": {
                "ca": "/etc/ssl/certs/ca-certificates.crt" 
            }
        }
    }