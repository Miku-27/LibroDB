from app.extensions import db
from app.services.google_api_services import search_books
from app.utils.library_helper import book_object_to_dict
from app.models import Book,UserBooks,CollectionBooks
from sqlalchemy import exists
from math import ceil
from app.utils.codes import Result_codes
import logging

logger = logging.getLogger(__name__)

def add_to_library(book_google_id,user_id):

    try:
        book = Book.query.filter_by(google_id=book_google_id).first()

        if not book:
            result = search_books(query=book_google_id,by_volume=True)
            if result.get("success"):
                book_data=result.get("data")[0]

                book = Book(
                    google_id=book_data.get("google_id") or None,
                    title=book_data.get("title") or None,
                    publisher=book_data.get("publisher") or None,
                    published_date=book_data.get("published_date") or None,
                    description=book_data.get("description") or None,
                    page_count=book_data.get("page_count") or None,
                    language=book_data.get("language") or None,
                    author_name=book_data.get("authors") or None,
                    categories=book_data.get("categories") or None,
                    isbn_13=book_data.get("isbn_13") or None, 
                    isbn_10=book_data.get("isbn_10") or None,
                    thumbnail=book_data.get("thumbnail") or None,
                    info_link=book_data.get("info_link") or None,
                )

                db.session.add(book)
                db.session.flush()
                
            elif result.get('status_code') == Result_codes.THIRD_PARTY_ERROR:
                return {
                "success": False,
                "status_code": Result_codes.THIRD_PARTY_ERROR,
                "data": None
                }
            else:
                raise Exception


        user_has_book = db.session.query(
            exists().where(
                UserBooks.user_id == user_id
            ).where(
                UserBooks.book_id == book.id
            )
            ).scalar()

        if not user_has_book:
            new_association = UserBooks(user_id=user_id,book_id=book.id)
            db.session.add(new_association)
            db.session.commit()
            return {
            "success": True,
            "status_code": Result_codes.BOOK_ADDED,
            "data": book.id
            }
        
        else:
            return {
            "success": False,
            "status_code": Result_codes.BOOK_ALREADY_EXISTS,
            "data": None
            }
    
    except Exception as e:
        db.session.rollback()
        logger.exception("Database error while trying to add book to user library")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }

# map used by pagination logic
FILTER_MAP = {
    "googleId":lambda q, v: q.filter(Book.google_id == v ),
    "title": lambda q, v: q.filter(Book.title.ilike(f"%{v}%")),
    "authorName": lambda q, v: q.filter(Book.author_name.ilike(f"%{v}%")),
    "status":lambda q, v: q.filter(UserBooks.status == v),
    "language": lambda q, v: q.filter(Book.language == v),
    "publisher": lambda q, v: q.filter(Book.publisher.ilike(f"%{v}%")),
    "publishedDate":lambda q, v: q.filter(Book.title.ilike(f"%{v}%")),
    "isbn13": lambda q, v: q.filter(Book.isbn_13 == v),
    "isbn10": lambda q, v: q.filter(Book.isbn_10 == v),
    "pageCountLt": lambda q, v: q.filter(Book.page_count < v),
    "pageCountMt": lambda q, v: q.filter(Book.page_count > v),
    "pageCountEq": lambda q, v: q.filter(Book.page_count == v),

    "collectionId":lambda q, v: q.join(CollectionBooks, CollectionBooks.user_book_id == UserBooks.id).filter(CollectionBooks.collection_id == v),
}


def get_user_books(user_id,filters={"page":1,"limit":9}):

    page_number = filters.pop("page", 1)
    books_per_page = filters.pop("limit", 9)
    offset = (page_number - 1) * books_per_page

    try:
        stmt = db.session.query(
                Book.google_id,
                Book.title,
                Book.author_name,
                Book.thumbnail,
                Book.published_date,
                Book.categories,
                Book.language,
                UserBooks.status
            ).join(UserBooks, UserBooks.book_id == Book.id).filter(UserBooks.user_id == user_id)
        
        for key,value in filters.items():
            lambda_obj = FILTER_MAP.get(key)
            if lambda_obj:
                stmt = lambda_obj(stmt,value)

        stmt = stmt.order_by(UserBooks.id.desc())

        total_books = stmt.count()
        books = [
                    {
                        "id": book_id,
                        "title": title,
                        "author_name": author,
                        "thumbnail": thumb,
                        "published_date": published_date,
                        "categories": categories,
                        "language": language,
                        "status": status
                    }
                    for (
                        book_id,
                        title,
                        author,
                        thumb,
                        published_date,
                        categories,
                        language,
                        status
                        ) 
                    in stmt.limit(books_per_page).offset(offset)
        ]     

        total_pages = ceil(total_books/books_per_page)
        book_data =  {
            "books": books,       
            "page": page_number,             
            "per_page": books_per_page, 
            "total_books": total_books,               
            "total_pages": total_pages  
        }
    
        return {
            "success": True,
            "status_code": Result_codes.BOOK_FETCHED,
            "data": book_data
        }
    
    except Exception as e:
        logger.exception("Database error while trying to fetch user's books")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }

def remove_from_userlib(book_google_id,user_id): 
    try:
        book_id = db.session.query(Book.id).filter(Book.google_id == book_google_id).scalar()
        
        if book_id is None:
            return {
                "success": False,
                "status_code": Result_codes.BOOK_NOT_IN_LIBRARY,
                "data": None
            }
        
        exists = (
            db.session.query(UserBooks)
            .filter_by(user_id=user_id, book_id=book_id)
            .first()
        )

        if exists is None:
            return {
                "success": False,
                "status_code": Result_codes.BOOK_NOT_IN_LIBRARY,
                "data": None
            }
        

        db.session.delete(exists)
        db.session.commit()
        return {
            "success": True,
            "status_code": Result_codes.BOOK_REMOVED,
            "data": None
        }
    
    except Exception as e:
        db.session.rollback()
        logger.exception("Database error while trying to remove book from user's library")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }
    
def get_book_info_service(book_google_id,user_id): 

    try:
        book = db.session.query(Book).filter(Book.google_id == book_google_id).first()
        user_book_id = None
        if book:
            user_book_id = db.session.query(UserBooks.id).filter(
                UserBooks.book_id == book.id, 
                UserBooks.user_id == user_id
            ).scalar()
            book = book_object_to_dict(book)
    
        else:
            response = search_books(book_google_id,by_volume=True)
            if not response.get("success"):
                return{
                    "success": False,
                    "status_code": response.get("status_code"),
                    "data": None
                }
            book = response.get("data")[0]
            
        data = {
            "book_existence" : True if user_book_id else False,
            "book":book
        }   
        return {
            "success": True,
            "status_code": Result_codes.DATA_FETCHED,
            "data": data
        }
    
    except Exception as e:
        logger.exception("Database error retrive book from Database")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }


def change_book_status(book_google_id,user_id,new_status): 

    try:
        book_id = db.session.query(Book.id).filter(Book.google_id == book_google_id).scalar()
        if not book_id:
            return {
                "success": False,
                "status_code": Result_codes.BOOK_NOT_IN_LIBRARY,
                "data": None
            }
        
        user_book_id = db.session.query(UserBooks).filter(
            UserBooks.book_id == book_id,
            UserBooks.user_id == user_id
        ).first() 

        if not user_book_id:
            return {
                "success": False,
                "status_code": Result_codes.BOOK_NOT_IN_LIBRARY,
                "data": None
            }
        
        user_book_id.status = new_status
        db.session.commit()

        return {
                "success": True,
                "status_code": Result_codes.BOOK_UPDATED,
                "data": None
        }

    except Exception as e:
        db.session.rollback()
        logger.exception("Database error while changing book status")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }      