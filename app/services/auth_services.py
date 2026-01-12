from app.models import User,PasswordResetToken
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.utils.codes  import Result_codes
from app.services.email_service import EmailService
import secrets
from datetime import datetime, timezone,timedelta
import os
import logging

logger = logging.getLogger(__name__)

def register_user(username,usermail,password):

    try:
        existing_user = User.query.filter_by(email = usermail).first()
        if existing_user:
            return {
                "success": False,
                "status_code": Result_codes.USER_ALREADY_EXISTS,
                "data": None
            }

        new_user = User(username=username,email=usermail)
        new_user.set_hashed_password(password)
        db.session.add(new_user)
        db.session.commit()
        return {
                "success": True,
                "status_code": Result_codes.USER_REGISTERED,
                "data": None
            }
    except Exception as e:
        db.session.rollback()
        logger.exception("Database error during user registering")
        return {
                "success": False,
                "status_code": Result_codes.INTERNAL_SERVER_ERROR,
                "data": None
            }


def check_login(usermail,password):
    
    try:
        existing_user = User.query.filter_by(email = usermail).first()
    
        if existing_user and existing_user.check_hashed_password(password):
            return {
                "success": True,
                "status_code": Result_codes.LOGIN_SUCCESS,
                "data": existing_user.id
            }
        else:
            return {
                "success": False,
                "status_code": Result_codes.INVALID_CREDENTIALS,
                "data": None
            }
        
    except Exception as e:
        logger.exception("Database error during login check")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }

def intialize_password_reset_request(email):
    try:
        user_id = db.session.query(User.id).filter(User.email == email).scalar()
        if not user_id:
            return {
            "success": True,
            "status_code": Result_codes.EMAIL_NOT_SENT,
            "data": None
        }
        
        generated_reset_token = secrets.token_urlsafe(32)
        now = datetime.now(timezone.utc)
        db.session.query(PasswordResetToken).filter((PasswordResetToken.token_used == True) | (PasswordResetToken.expires_at < now)).delete()
        db.session.flush()
        new_token = PasswordResetToken(
            user_id = user_id,
            expires_at = now + timedelta(minutes=15),
            reset_token = generated_reset_token,
        ) 
        db.session.add(new_token)
        db.session.commit()

        website_url = os.getenv("WEBSITE_URL")
        email_client = EmailService()
        subject = "Password Reset Request"
        body = f"Hello, click here to reset your password: {website_url}/change-password?token={generated_reset_token}"
        
        email_client.send_email_async(
            to=email,
            subject=subject,
            body=body
        )

        return {
            "success": True,
            "status_code": Result_codes.EMAIL_SENT,
            "data": None
        }
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception("Database error during adding reset token")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }
    
def intialize_password_reset(reset_token,new_password):
    try:
        now = datetime.now(timezone.utc)
        token_valid_row = db.session.query(PasswordResetToken).filter(
            PasswordResetToken.reset_token==reset_token,
            PasswordResetToken.expires_at > now,
            PasswordResetToken.token_used == False
        ).first()

        if not token_valid_row:
            return {
                "success": False,
                "status_code": Result_codes.PASSWORD_RESET_FAILED,
                "data": None
            }
        
        user = db.session.query(User).filter(User.id == token_valid_row.user_id).first()
        user.set_hashed_password(new_password)
        token_valid_row.token_used = True
        db.session.commit()
        return {
            "success": True,
            "status_code": Result_codes.PASSWORD_RESET_SUCCESS,
            "data": None
        }
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception("Database error during Trying to reset password")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }   

def change_password_service(user_id,old_password,new_password):
    try:
        user = db.session.query(User).filter(User.id==user_id , ).first()
        if not user:
            return {
                "success": False,
                "status_code": Result_codes.USER_NOT_FOUND,
                "data":None
            }
        password_match = user.check_hashed_password(old_password)
        if not password_match:
            return {
                "success": False,
                "status_code": Result_codes.INVALID_CREDENTIALS,
                "data": None
            }   
        
        user.set_hashed_password(new_password)

        db.session.commit()
        return {
            "success":True,
            "status_code": Result_codes.PASSWORD_RESET_SUCCESS,
            "data": None
        }   
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception("Database error during Trying to reset password")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }   