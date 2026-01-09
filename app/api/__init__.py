from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")

from app.api.auth_api import auth_api
from app.api.library_api import library_api
from app.api.collection_api import collection_api
from app.api.book_api import books_api

api_bp.register_blueprint(auth_api)
api_bp.register_blueprint(library_api)
api_bp.register_blueprint(collection_api)
api_bp.register_blueprint(books_api)