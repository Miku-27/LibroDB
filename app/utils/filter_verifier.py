
ALLOWED_FILTERS = {
    "googleId", "title", "authorName", "status", "collectionId", 
    "language", "pageCountLt", "pageCountMt", "pageCountEq",
    "publishedDate", "publisher", "isbn13", "isbn10","page","limit"
}

ALLOWED_FILTERS_DATATYPE = {
    "googleId": str,
    "title": str,
    "authorName": str,
    "status": str,
    "collectionId": int,
    "language": str,
    "pageCountLt": int,
    "pageCountMt": int,
    "pageCountEq": int,
    "publishedDate": str,
    "publisher": str,
    "isbn13": str,
    "isbn10": str,
    "page":int,
    "limit":int
}

def verify_filter(filter):
    cleaned_filter = {}
    try:
        for key,value in filter.items():
            if key not in ALLOWED_FILTERS:
                continue
            
            cleaned_filter[key] = ALLOWED_FILTERS_DATATYPE.get(key)(value)
        
            if key == "status" or key == "languange":
                cleaned_filter[key] = cleaned_filter[key].lower()
        return {
            "success":True,
            "data":cleaned_filter,
            "error":None
        }
    except (ValueError,TypeError):
        return {
            "success":False,
            "data":None,
            "error":f"Invalid value:{value} for the filter {key}"
        }