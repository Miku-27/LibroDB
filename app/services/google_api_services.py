import requests
from requests.exceptions import HTTPError
from app.utils.codes import Result_codes
import logging

logger = logging.getLogger(__name__)

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books(query,page=1,max_results=5,by_volume=False,):


    offset = (page-1)*max_results

    params = {
        "q": query,
        "maxResults": max_results,
        "startIndex":offset
    }

    try:
        if by_volume:
            response = requests.get(GOOGLE_BOOKS_API_URL+"/"+query)
        else:
            response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        
        response.raise_for_status() 

        data = [response.json()] if by_volume else response.json().get("items",[])

        books = []
        for item in data:
            volume_info = item.get("volumeInfo", {})
            books.append({
                "google_id": item.get("id"),
                "title": volume_info.get("title"),
                "author_name" : ", ".join(volume_info.get("authors", [])),
                "publisher": volume_info.get("publisher"),
                "published_date": volume_info.get("publishedDate"),
                "description": volume_info.get("description"),
                "page_count": volume_info.get("pageCount"),
                "categories" : ", ".join(volume_info.get("categories", []))[:100],
                "language": volume_info.get("language"),
                "info_link": volume_info.get("infoLink"),
                "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
                "isbn_13": None,
                "isbn_10": None
            })

            for identifier in volume_info.get("industryIdentifiers", []):
                if identifier["type"] == "ISBN_13":
                    books[-1]["isbn_13"] = identifier["identifier"]
                if identifier["type"] == "ISBN_10":
                    books[-1]["isbn_10"] = identifier["identifier"]


        return {
            "success": True,
            "status_code": Result_codes.DATA_FETCHED,
            "data": books
        }

    except HTTPError as e:
        status_code = e.response.status_code
        logger.exception("Error trying to fetch book from googlebooks api")

        return {
            "success": False,
            "status_code": Result_codes.BOOK_NOT_FOUND if status_code == 404 else Result_codes.THIRD_PARTY_ERROR,
            "data": None
        }

    except Exception as e:
        logger.exception("Error trying to fetch book from googlebooks api")
        return {
            "success": False,
            "status_code": Result_codes.INTERNAL_SERVER_ERROR,
            "data": None
        }
