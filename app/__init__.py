import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db,jwt,rate_limiter,migrate
from app.api import api_bp
from app.pages import pages_bp
from app.utils.logger import attach_app_logger
from flask_talisman import Talisman



def create_app():
    app = Flask(__name__)

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # PROJECT_ROOT = os.path.dirname(BASE_DIR)
    # load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    load_dotenv('.env')
    env = os.getenv("LIBRO_ENV", "development")

    from config import DevelopmentConfig,ProductionConfig
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    if app.config.get('TALISMAN_ENABLED'):
        Talisman(
            app,
            content_security_policy=app.config.get("TALISMAN_CSP"),
            force_https=app.config.get("TALISMAN_FORCE_HTTPS"),
            referrer_policy=app.config.get("TALISMAN_REFERRER_POLICY"),
            frame_options = app.config.get("TALISMAN_FRAME_OPTIONS")
        )


    attach_app_logger()

    db.init_app(app)
    jwt.init_app(app)
    rate_limiter.init_app(app)
    migrate.init_app(app,db)
    
    app.register_blueprint(api_bp)
    app.register_blueprint(pages_bp)

    return app