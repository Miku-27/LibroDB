def book_object_to_dict(book_obj):
    books_dict = {
        "google_id": book_obj.google_id, 
        "title": book_obj.title,
        "author_name":book_obj.author_name,
        "publisher": book_obj.publisher,
        "published_date":book_obj.published_date,
        "description": book_obj.description,
        "page_count": book_obj.page_count,
        "categories": book_obj.categories,
        "language": book_obj.language,
        "info_link": book_obj.info_link,
        "thumbnail": book_obj.thumbnail,
        "isbn_13": book_obj.isbn_13,
        "isbn_10": book_obj.isbn_10,
    }
    return books_dict
