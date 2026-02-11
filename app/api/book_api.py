from flask import Blueprint, request,current_app
from flask_jwt_extended import jwt_required

from app.services.google_api_services import search_books
from app.utils.codes import Result_codes,finalize_to_Flask_response

books_api = Blueprint("books_api", __name__,url_prefix="/books")

@books_api.route("")
@jwt_required()
def search_books_globally():

    query = request.args.get("query", "").strip()
    books_per_page = request.args.get("limit", 9)
    page_number = request.args.get("page", 1)

    try:
        books_per_page = int(books_per_page)
        page_number = int(page_number)
    except ValueError:
        return finalize_to_Flask_response(None,False,None,Result_codes.INVALID_INPUT)
    
    if not query:
        return finalize_to_Flask_response(None,False,None,Result_codes.INVALID_INPUT)
    api_key=current_app.config["GOOGLE_API_KEY"]
    result = search_books(api_key,query,page_number,books_per_page)
    
    return finalize_to_Flask_response(result)
