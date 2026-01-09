from flask import Blueprint

pages_bp = Blueprint("pages", __name__)

from app.pages.views import view

pages_bp.register_blueprint(view)
