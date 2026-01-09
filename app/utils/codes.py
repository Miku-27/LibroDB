from flask import jsonify
from enum import Enum


class Result_codes:
    """
    Unified result codes for the entire application.
    Used by the Service Layer to communicate with the API Layer.
    """
    # --- Auth Codes ---
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    USER_REGISTERED = "USER_REGISTERED"
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGOUT_SUCCESS = "LOGOUT_SUCCESS"

    # --- Book Codes ---
    BOOK_NOT_FOUND = "BOOK_NOT_FOUND"
    BOOK_NOT_IN_LIBRARY = "BOOK_NOT_IN_LIBRARY"
    BOOK_ADDED = "BOOK_ADDED"
    BOOK_REMOVED = "BOOK_REMOVED"
    BOOK_UPDATED = "BOOK_UPDATED"
    BOOK_FETCHED = "BOOK_FETCHED"
    BOOK_ALREADY_EXISTS = "BOOK_ALREADY_EXISTS"
    
    # --- Collection Codes ---
    COLLECTION_NOT_FOUND = "COLLECTION_NOT_FOUND"
    COLLECTION_CREATED = "COLLECTION_CREATED"
    COLLECTION_DELETED = "COLLECTION_DELETED"
    COLLECTION_UPDATED = "COLLECTION_UPDATED"
    
    # --- Collection-Book Relationship Codes ---
    BOOK_ALREADY_IN_COLLECTION = "BOOK_ALREADY_IN_COLLECTION"
    BOOK_NOT_IN_COLLECTION = "BOOK_NOT_IN_COLLECTION"
    BOOK_ADDED_TO_COLLECTION = "BOOK_ADDED_TO_COLLECTION"
    BOOK_REMOVED_FROM_COLLECTION = "BOOK_REMOVED_FROM_COLLECTION"
    
    # --- System & General Codes ---
    PERMISSION_DENIED = "PERMISSION_DENIED"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    DATA_FETCHED = "DATA_FETCHED"
    JSON_REQUIRED = "JSON_REQUIRED"
    INVALID_EMAIL = "INVALID_EMAIL"
    INVALID_INPUT = "INVALID_INPUT"
    THIRD_PARTY_ERROR = "THIRD_PARTY_ERROR"
    EMAIL_SENT="EMAIL_SENT"
    EMAIL_NOT_SENT="EMAIL_NOT_SENT"
    PASSWORD_RESET_SUCCESS = "PASSWORD_RESET_SUCCESS"   
    PASSWORD_RESET_FAILED = "PASSWORD_RESET_FAILED"   


# Mapping Codes to HTTP Codes
RESP_HTTP_CODE = {
    # 200s: Success
    Result_codes.USER_REGISTERED: 201,
    Result_codes.LOGIN_SUCCESS: 200,
    Result_codes.LOGOUT_SUCCESS: 200,
    Result_codes.BOOK_ADDED: 201,
    Result_codes.BOOK_REMOVED: 200,
    Result_codes.BOOK_UPDATED: 200,
    Result_codes.BOOK_FETCHED: 200,
    Result_codes.COLLECTION_CREATED: 201,
    Result_codes.COLLECTION_DELETED: 200,
    Result_codes.COLLECTION_UPDATED: 200,
    Result_codes.BOOK_ADDED_TO_COLLECTION: 201,
    Result_codes.DATA_FETCHED: 200,
    Result_codes.BOOK_REMOVED_FROM_COLLECTION:200, #intentioanlly done to get body in frontend
    Result_codes.EMAIL_SENT:200,
    Result_codes.EMAIL_NOT_SENT:200,
    Result_codes.PASSWORD_RESET_SUCCESS : 200,   

    # 400s: Client Errors
    Result_codes.PASSWORD_RESET_FAILED : 400,
    Result_codes.BOOK_NOT_FOUND: 404,
    Result_codes.INVALID_EMAIL: 400,
    Result_codes.BOOK_NOT_IN_LIBRARY: 404,
    Result_codes.BOOK_NOT_IN_COLLECTION: 404,
    Result_codes.COLLECTION_NOT_FOUND: 404,
    Result_codes.INVALID_CREDENTIALS: 401,
    Result_codes.PERMISSION_DENIED: 403,
    Result_codes.USER_ALREADY_EXISTS: 409,
    Result_codes.BOOK_ALREADY_IN_COLLECTION: 409,
    Result_codes.BOOK_ALREADY_EXISTS:409,
    Result_codes.JSON_REQUIRED:415,
    Result_codes.INVALID_INPUT: 400,
    
    # 500s: Server Errors
    Result_codes.INTERNAL_SERVER_ERROR: 500,
    Result_codes.THIRD_PARTY_ERROR:502,

}


# Mapping Codes to Messages
RESP_MESSAGES = {
    # Auth Messages
    Result_codes.USER_REGISTERED: "Your account has been created successfully",
    Result_codes.LOGIN_SUCCESS: "Successfully logged in",
    Result_codes.LOGOUT_SUCCESS: "You have been logged out",
    Result_codes.USER_ALREADY_EXISTS: "An account with this email address already exists",
    Result_codes.INVALID_CREDENTIALS: "The email or password you entered is incorrect",
    
    # Book Messages
    Result_codes.BOOK_ADDED: "Book added to your library",
    Result_codes.BOOK_REMOVED: "Book removed from your library",
    Result_codes.BOOK_UPDATED: "Book details updated",
    Result_codes.BOOK_FETCHED: "Book details retrieved successfully",
    Result_codes.BOOK_NOT_FOUND: "The book you are looking for does not exist in our catalog",
    Result_codes.BOOK_NOT_IN_LIBRARY: "This book is not in your personal library",
    Result_codes.BOOK_ALREADY_EXISTS: "This book is already present in your library",

    # Collection Messages
    Result_codes.COLLECTION_CREATED: "New collection created successfully",
    Result_codes.COLLECTION_DELETED: "Collection deleted permanently",
    Result_codes.COLLECTION_UPDATED: "Collection details updated",
    Result_codes.COLLECTION_NOT_FOUND: "The collection you requested does not exist",
    
    # Collection Action Messages
    Result_codes.BOOK_ADDED_TO_COLLECTION: "The book has been added to the collection",
    Result_codes.BOOK_ALREADY_IN_COLLECTION: "This book is already present in this collection",
    Result_codes.BOOK_NOT_IN_COLLECTION: "This book could not be found in this collection",
    Result_codes.BOOK_REMOVED_FROM_COLLECTION : "Book successfully deleted from the collection",
    
    # General Messages
    Result_codes.DATA_FETCHED: "Data retrieved successfully",
    Result_codes.PERMISSION_DENIED: "You do not have permission to perform this action",
    Result_codes.INTERNAL_SERVER_ERROR: "Something went wrong on our end. Please try again later",
    Result_codes.JSON_REQUIRED: "API expects data in json body",
    Result_codes.INVALID_EMAIL: "The email address provided is not in a valid format",
    Result_codes.INVALID_INPUT: "Provided input is invalid , refer to docs",
    Result_codes.THIRD_PARTY_ERROR : "Book with searched id doesnt exist", # for now using this defination
    Result_codes.EMAIL_SENT:"If an account is associated with this email, you will receive a reset link shortly.",
    Result_codes.EMAIL_NOT_SENT:"If an account is associated with this email, you will receive a reset link shortly.",
    Result_codes.PASSWORD_RESET_FAILED:"Failed to reset password please try again with new request",
    Result_codes.PASSWORD_RESET_SUCCESS:"Password was succesfully updated"
}

def finalize_to_Flask_response(service_layer_response=None,success=None,data=None,code=None,cstm_msg=None):

    if service_layer_response:
        success = service_layer_response.get("success")
        status_code = service_layer_response.get("status_code")
        data = service_layer_response.get("data")
        msg = RESP_MESSAGES.get(status_code)
        http_code = RESP_HTTP_CODE.get(status_code)
    else:
        msg = cstm_msg if cstm_msg else RESP_MESSAGES.get(code)
        http_code = RESP_HTTP_CODE.get(code)
    
    response = jsonify({
        "success": success,
        "msg": msg,
        "data": data
    })
    response.status_code = http_code
    return response