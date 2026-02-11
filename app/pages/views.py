from flask import Blueprint, request, render_template, redirect,current_app
from flask_jwt_extended import jwt_required, get_jwt_identity,verify_jwt_in_request

from app.services.library_service import get_user_books,get_book_info_service
from app.services.collection_service import get_user_collection_metadata_service
view = Blueprint("view", __name__)

@view.route("/library")
@jwt_required()
def library_route():

    user_id = get_jwt_identity() 
    library_result = get_user_books(user_id)
    collection_result = get_user_collection_metadata_service(user_id)
    user_data = {"book_data":library_result.get("data"),"collection_data":collection_result.get("data")}

    return render_template("library.html", data=user_data)

@view.route("/book/<string:book_id>")
@jwt_required()
def book_detail_route(book_id):

    user_id = get_jwt_identity() 
    api_key=current_app.config["GOOGLE_API_KEY"]
    book_result = get_book_info_service(api_key,book_id,user_id)
    return render_template("book-detail.html",book = book_result.get("data").get("book"),book_existence = book_result.get("data").get("book_existence"))

@view.route("/")
@view.route("/index")
def index_route():
    return render_template("index.html")

@view.route("/forgot-password")
def forgot_password_route():
    return render_template("request-forgot-password.html")


@view.route("/search-book")
@jwt_required()
def search_book_route():
    return render_template("search-book.html")

@view.route("/login")
def login_route():
    return render_template("login.html")

@view.route("/register")
def register_route():
    return render_template("register.html")

@view.route("/change-password")
@jwt_required
def change_password_route():
    return render_template("change-password.html")


