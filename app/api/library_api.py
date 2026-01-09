from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.library_service import add_to_library,get_user_books,remove_from_userlib,change_book_status
from app.utils.codes import finalize_to_Flask_response,Result_codes
from app.utils.filter_verifier import verify_filter

library_api = Blueprint("library_api", __name__, url_prefix="/library")

@library_api.route("/books")
@jwt_required()
def userBooks_route():
    user_id = get_jwt_identity()

    all_filters = request.args.to_dict()
    
    result = verify_filter(all_filters)
    if not result.get("success"):
        return finalize_to_Flask_response(None,False,None,Result_codes.INVALID_INPUT,result.get("error"))

    cleaned_filter = result.get("data")

    result = get_user_books(user_id,cleaned_filter)
    return finalize_to_Flask_response(result)

@library_api.route("/books/<string:bookId>" , methods=["POST"])
@jwt_required()
def savebook_route(bookId):
    user_id = get_jwt_identity()
    
    result = add_to_library(bookId,user_id)
    return finalize_to_Flask_response(result)

@library_api.route("/books/<string:bookId>", methods=['DELETE'])
@jwt_required()
def removebook_route(bookId):
    
    user_id = get_jwt_identity()
    result = remove_from_userlib(bookId,user_id)

    return finalize_to_Flask_response(result)

@library_api.route("/books/<string:bookId>", methods=['PATCH'])
@jwt_required()
def change_status_route(bookId):

    if not request.is_json:
        return finalize_to_Flask_response(None,False,None,Result_codes.JSON_REQUIRED)

    data = request.get_json()
    new_status = data.get("new_status",None)
    if not new_status or new_status not in ['Reading','Completed','Pending']:
        return finalize_to_Flask_response(None,False,None,Result_codes.INVALID_INPUT)
    
    user_id = get_jwt_identity()
    result = change_book_status(bookId,user_id,new_status)
    print(result)

    return finalize_to_Flask_response(result)
