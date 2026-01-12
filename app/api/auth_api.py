from flask import Blueprint,request
from flask_jwt_extended import create_access_token, set_access_cookies,unset_jwt_cookies, jwt_required,get_jwt_identity
import re

from app.services.auth_services import register_user,check_login,intialize_password_reset_request,intialize_password_reset,change_password_service
from app.utils.codes import finalize_to_Flask_response,Result_codes
from app.extensions import rate_limiter

auth_api = Blueprint('auth',__name__ , url_prefix='/auth')

@auth_api.route("/user" , methods=["POST"])
@rate_limiter.limit("5 per minute")
def register():
    
    if not request.is_json:
        return finalize_to_Flask_response(None,False,None,Result_codes.JSON_REQUIRED)

    data = request.get_json()
    username = data.get("username", "").strip()
    usermail = data.get("usermail", "").lower().strip()
    password = data.get("password", "").strip()

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex,usermail):
        return finalize_to_Flask_response(None,False,None,Result_codes.INVALID_EMAIL)
    
    response = register_user(username,usermail,password)
    return finalize_to_Flask_response(response)

@auth_api.route("/user" , methods=["PATCH"])
@rate_limiter.limit("2 per minute")
@jwt_required()
def change_password_route():
    
    if not request.is_json:
        return finalize_to_Flask_response(None,False,None,Result_codes.JSON_REQUIRED)

    data = request.get_json()
    old_password = data.get("oldPassword", "").strip()
    new_password = data.get("newPassword", "").strip()
    user_id = get_jwt_identity()
    response = change_password_service(user_id,old_password,new_password)
    return finalize_to_Flask_response(response)



@auth_api.route("/token", methods=["POST"])
@rate_limiter.limit("5 per minute")
def login():
    
    if not request.is_json:
        return finalize_to_Flask_response(None,False,None,Result_codes.JSON_REQUIRED)

    data = request.get_json()
    usermail = data.get("usermail", "").lower().strip()
    password = data.get("password", "").strip()

    result = check_login(usermail,password)
    
    if not result.get("success"):
        return finalize_to_Flask_response(result)
    else:
        user_id = result.get("data")
        access_token = create_access_token(identity=str(user_id))

        response = finalize_to_Flask_response(result)
        set_access_cookies(response,access_token)

        return response
    
@auth_api.route("/token", methods=["DELETE"])
@rate_limiter.limit("5 per minute")
def logout():
    response = finalize_to_Flask_response(None,True,None,Result_codes.LOGOUT_SUCCESS)
    unset_jwt_cookies(response)
    return response

@auth_api.route("/password-reset", methods=["PATCH"])
@rate_limiter.limit("1 per minute")
def password_reset_route():

    if not request.is_json:
        return finalize_to_Flask_response(None,False,None,Result_codes.JSON_REQUIRED)

    data = request.get_json()
    new_password = data.get("newPassword","").strip()
    resetToken = data.get("resetToken","").strip()
    if not new_password:
        return finalize_to_Flask_response(None,False,None,Result_codes.INVALID_EMAIL)
    
    result = intialize_password_reset(resetToken,new_password)
    return finalize_to_Flask_response(result)

@auth_api.route("/password-reset", methods=["POST"])
@rate_limiter.limit("1 per minute")
def password_reset_request_route():
    
    if not request.is_json:
        return finalize_to_Flask_response(None,False,None,Result_codes.JSON_REQUIRED)

    data = request.get_json()
    usermail = data.get("usermail", "").lower().strip()
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex,usermail):
        return finalize_to_Flask_response(None,False,None,Result_codes.INVALID_EMAIL)
    
    result = intialize_password_reset_request(usermail)
    return finalize_to_Flask_response(result)