from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.collection_service import (
    create_new_collection_service,
    add_book_to_collection_service,
    remove_book_from_collection_service,
    delete_collection_service,
    rename_collection_service,
    get_user_collection_metadata_service
)
from app.utils.codes import finalize_to_Flask_response,Result_codes

collection_api = Blueprint("collection_api", __name__, url_prefix="/collections")



@collection_api.route("/", methods=["GET"])
@jwt_required()
def get_collection_route():
    user_id = get_jwt_identity()
    result = get_user_collection_metadata_service(user_id)
    return finalize_to_Flask_response(result)

@collection_api.route("/", methods=["POST"])
@jwt_required()
def new_collection_route():

    if not request.is_json:
        return finalize_to_Flask_response(None,False,None,Result_codes.JSON_REQUIRED)
    
    data = request.get_json()
    collection_name = data.get("collection_name", "").strip()
    if not collection_name:
        return finalize_to_Flask_response(None,False,None,Result_codes.INVALID_INPUT)
    
    user_id = get_jwt_identity()
    
    result = create_new_collection_service(collection_name, user_id)
    return finalize_to_Flask_response(result)

@collection_api.route("/<int:collection_id>/book/<string:book_id>", methods=["POST"])
@jwt_required()
def add_book_to_collection_route(collection_id,book_id):
    
    user_id = get_jwt_identity()
    result = add_book_to_collection_service(collection_id,book_id,user_id)
    
    return finalize_to_Flask_response(result)


@collection_api.route("/<int:collection_id>/book/<string:book_id>", methods=["DELETE"])
@jwt_required()
def remove_book_from_collection_route(collection_id,book_id):
    
    user_id = get_jwt_identity()
    result = remove_book_from_collection_service(collection_id,book_id,user_id)
    print(result)
    return finalize_to_Flask_response(result)


@collection_api.route("/<int:collection_id>", methods=["DELETE"])
@jwt_required()
def remove_collection_route(collection_id):
    
    user_id = get_jwt_identity()
    result = delete_collection_service(collection_id,user_id)
    return finalize_to_Flask_response(result)

@collection_api.route("/<int:collection_id>", methods=["PATCH"])
@jwt_required()
def rename_collection_route(collection_id):
    
    if not request.is_json:
        return finalize_to_Flask_response(None,False,None,Result_codes.JSON_REQUIRED)
    data = request.get_json()
    
    new_collection_name = data.get("Collection_name", "").strip()
    if not new_collection_name:
        return finalize_to_Flask_response(None,False,None,Result_codes.INVALID_INPUT)
    user_id = get_jwt_identity()

    result = rename_collection_service(user_id,collection_id,new_collection_name)

    return finalize_to_Flask_response(result)