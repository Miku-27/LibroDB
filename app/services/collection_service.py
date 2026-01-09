from app.extensions import db
from app.models import UserCollection,CollectionBooks,UserBooks,Book
from app.utils.codes import Result_codes
import logging

logger = logging.getLogger(__name__)


def get_user_collection_metadata_service(user_id):
    
    try:
        collection_data = [{"collection_id":collection_id,"collection_name":collection_name}
         for(collection_id,collection_name)
         in db.session.query(UserCollection.collection_id,UserCollection.collection_name).filter_by(user_id=user_id)
        ]

        return {
            "success": True,
            "status_code": Result_codes.DATA_FETCHED,
            "data": collection_data
        }
    except Exception as e:
        logger.exception("Database error during fetching collection data")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }
        

def create_new_collection_service(collection_name,user_id):
    try:
        newCollection = UserCollection(
            user_id=user_id,
            collection_name=collection_name
        )

        db.session.add(newCollection)
        db.session.commit()
        return {
            "success": True,
            "status_code": Result_codes.COLLECTION_CREATED,
            "data": None
        }
    
    except Exception as e:
        db.session.rollback()
        logger.exception("Database error during collection creation")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }
    
def add_book_to_collection_service(collection_id, book_google_id, user_id):
    try:
        book_id = db.session.query(Book.id).filter(Book.google_id == book_google_id).scalar()
        
        if book_id is None:
            return {
                "success": False,
                "status_code": Result_codes.BOOK_NOT_IN_LIBRARY,
                "data": None
            }
       
        user_book_id = db.session.query(UserBooks.id).filter_by(
            user_id=user_id, book_id=book_id
        ).scalar()

        if not user_book_id:
            new_user_book = UserBooks(user_id=user_id, book_id=book_id)
            db.session.add(new_user_book)
            db.session.flush()
            user_book_id = new_user_book.id

        exists = db.session.query(CollectionBooks).filter_by(
            collection_id=collection_id,
            user_book_id=user_book_id
        ).first()

        if exists:
            return {
                "success": False,
                "status_code": Result_codes.BOOK_ALREADY_IN_COLLECTION,
                "data": None
            }

        db.session.execute(
            CollectionBooks.__table__.insert().values(
                collection_id=collection_id,
                user_book_id=user_book_id
            )
        )

        db.session.commit()

        return {
            "success": True,
            "status_code": Result_codes.BOOK_ADDED_TO_COLLECTION,
            "data": None
        }

    except Exception as e:
        db.session.rollback()
        logger.exception("Database error during adding a book to collection")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }


def remove_book_from_collection_service(collection_id, book_google_id, user_id):
    try:
        
        book_id = db.session.query(Book.id).filter(Book.google_id == book_google_id).scalar()
        
        if book_id is None:
            return {
                "success": False,
                "status_code": Result_codes.BOOK_NOT_IN_LIBRARY,
                "data": None
            }
        
        user_book_id = db.session.query(UserBooks.id).filter_by(
            user_id=user_id,
            book_id=book_id
        ).scalar() 

        if not user_book_id:
            return {
                "success": False,
                "status_code": Result_codes.BOOK_NOT_IN_COLLECTION,
                "data": None
            }

        entry_id = db.session.query(CollectionBooks.collection_id).filter_by(
            collection_id=collection_id,
            user_book_id=user_book_id
        ).scalar()

        if not entry_id:
            return {
                "success": False,
                "status_code": Result_codes.BOOK_NOT_IN_COLLECTION,
                "data": None
            }
        
        db.session.query(CollectionBooks).filter_by(
            collection_id=collection_id,
            user_book_id=user_book_id
        ).delete()

        db.session.commit()
        return {
            "success": True,
            "status_code": Result_codes.BOOK_REMOVED_FROM_COLLECTION,
            "data": None
        }

    except Exception as e:
        db.session.rollback()
        logger.exception("Database error while removing a book from collection")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }


def delete_collection_service(collection_id,user_id):

    try:
        collection = UserCollection.query.filter_by(collection_id=collection_id,user_id = user_id).first()

        if not collection:
            return {
            "success": False,
            "status_code": Result_codes.COLLECTION_NOT_FOUND,
            "data": None
        }

        db.session.delete(collection)
        db.session.commit()

        return {
            "success": True,
            "status_code": Result_codes.COLLECTION_DELETED,
            "data": None
        }
    except Exception as e:
        db.session.rollback()
        logger.exception("Database error while trying to delete a collection")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }
    
def rename_collection_service(user_id,collection_id,new_collection_name):

    try:
        collection = UserCollection.query.filter(collection_id=collection_id,user_id=user_id).first()

        if collection:
            collection.collection_name = new_collection_name
            db.session.commit()

            return {
            "success": True,
            "status_code": Result_codes.COLLECTION_UPDATED,
            "data": collection
            }
        else:
            return {
            "success": False,
            "status_code": Result_codes.COLLECTION_NOT_FOUND,
            "data": None
            }
        
    except Exception as e:
        db.session.rollback()
        logger.exception("Database error while trying to rename a collection")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }
    