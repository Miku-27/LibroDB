# LibroDB API Documentation

## Project Overview

**Project Name:** LibroDB - Personal Book Library Management System  
**Description:** A Flask-based REST API for managing personal book libraries with collections, search functionality, and user authentication.  
**Base URL:** `http://localhost:5000/api`  
**Version:** 0.1.0  
**Authentication:** JWT tokens stored in HttpOnly cookies with CSRF protection  
**Global Rate Limit:** 200 requests per day (configurable)  

## Endpoint Summary

| Endpoint | Method | Auth Required | Rate Limit | Description |
|----------|--------|---------------|------------|-------------|
| `/auth/register` | POST | No | 5/minute | Register new user account |
| `/auth/login` | POST | No | 5/minute | User login |
| `/auth/logout` | POST | No | 5/minute | User logout |
| `/books` | GET | Yes | Global | Search books from Google Books API |
| `/library/books` | GET | Yes | Global | Get user's personal library |
| `/library/books/{bookId}` | POST | Yes | Global | Add book to user's library |
| `/library/books/{bookId}` | DELETE | Yes | Global | Remove book from user's library |
| `/library/books/{bookId}` | PATCH | Yes | Global | Update book status in library |
| `/collections/` | GET | Yes | Global | Get user's collections |
| `/collections/` | POST | Yes | Global | Create new collection |
| `/collections/{id}` | DELETE | Yes | Global | Delete collection |
| `/collections/{id}` | PATCH | Yes | Global | Rename collection |
| `/collections/{id}/book/{bookId}` | POST | Yes | Global | Add book to collection |
| `/collections/{id}/book/{bookId}` | DELETE | Yes | Global | Remove book from collection |

## Authentication Details

### JWT Token System
- **Storage:** HttpOnly cookies (secure, not accessible via JavaScript)
- **Token Name:** `access_token`
- **Expiration:** 60 minutes
- **CSRF Protection:** Enabled for POST, PUT, DELETE, PATCH requests
- **Cookie Settings:** 
  - `HttpOnly: true`
  - `SameSite: Lax`
  - `Secure: false` (development), `true` (production)

### Login Flow
1. Send credentials to `/auth/login`
2. Server validates and returns JWT in HttpOnly cookie
3. CSRF token is stored in a separate cookie and must be included by the client in a custom header for state-changing requests
4. Token automatically included in future requests

### Token Renewal
- No automatic renewal implemented
- Users must re-login after token expiration
- Expired tokens return 401 with redirect to login

## Rate Limiting

- **Global Default:** 200 requests per day per user/IP
- **Authentication Endpoints:** 5 requests per minute
- **Key Function:** User-based (if authenticated) or IP-based (if anonymous)
- **Headers:** Rate limit information included in response headers

## Endpoint Details

### Authentication Endpoints

#### Register User
```
POST /api/auth/register
```

**Description:** Create a new user account

**Authentication:** Not required  
**Rate Limit:** 5 requests per minute

**Request Body:**
```json
{
  "username": "john_doe",
  "usermail": "john@example.com",
  "password": "securePassword123"
}
```

**Parameters:**
- `username` (string, required): User's display name
- `usermail` (string, required): Valid email address
- `password` (string, required): User's password

**Success Response (201):**
```json
{
  "success": true,
  "msg": "Your account has been created successfully",
  "data": null
}
```

**Error Responses:**
```json
// 400 - Invalid email format
{
  "success": false,
  "msg": "The email address provided is not in a valid format",
  "data": null
}

// 409 - User already exists
{
  "success": false,
  "msg": "An account with this email address already exists",
  "data": null
}

// 415 - Invalid content type
{
  "success": false,
  "msg": "API expects data in json body",
  "data": null
}
```

#### Login User
```
POST /api/auth/login
```

**Description:** Authenticate user and set JWT cookie

**Authentication:** Not required  
**Rate Limit:** 5 requests per minute

**Request Body:**
```json
{
  "usermail": "john@example.com",
  "password": "securePassword123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "msg": "Successfully logged in",
  "data": null
}
```
*Note: JWT token is set as HttpOnly cookie*

**Error Responses:**
```json
// 401 - Invalid credentials
{
  "success": false,
  "msg": "The email or password you entered is incorrect",
  "data": null
}
```

#### Logout User
```
POST /api/auth/logout
```

**Description:** Clear JWT cookie and logout user

**Authentication:** Not required  
**Rate Limit:** 5 requests per minute

**Success Response (200):**
```json
{
  "success": true,
  "msg": "You have been logged out",
  "data": null
}
```

### Book Search Endpoints

#### Search Books
```
GET /api/books?query={search_term}&page={page}&limit={limit}
```

**Description:** Search books using Google Books API

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Query Parameters:**
- `query` (string, required): Search term for books
- `page` (integer, optional, default=1): Page number for pagination
- `limit` (integer, optional, default=9): Number of books per page

**Success Response (200):**
```json
{
  "success": true,
  "msg": "Data retrieved successfully",
  "data": [
    {
      "google_id": "abc123",
      "title": "The Great Gatsby",
      "author_name": "F. Scott Fitzgerald",
      "publisher": "Scribner",
      "published_date": "1925",
      "description": "A classic American novel...",
      "page_count": 180,
      "categories": "Fiction, Classics",
      "language": "en",
      "info_link": "https://books.google.com/books?id=abc123",
      "thumbnail": "https://books.google.com/books/content?id=abc123&printsec=frontcover&img=1&zoom=1",
      "isbn_13": "9780743273565",
      "isbn_10": "0743273567"
    }
  ]
}
```

**Error Responses:**
```json
// 400 - Invalid input
{
  "success": false,
  "msg": "Provided input is invalid , refer to docs",
  "data": null
}

// 502 - Third party API error
{
  "success": false,
  "msg": "Book with searched id doesnt exist",
  "data": null
}
```

### Library Management Endpoints

#### Get User's Library
```
GET /api/library/books?page={page}&limit={limit}&status={status}&title={title}...
```

**Description:** Retrieve user's personal book library with filtering and pagination

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Query Parameters (all optional):**
- `page` (integer, default=1): Page number
- `limit` (integer, default=9): Books per page
- `status` (string): Filter by reading status (`reading`, `completed`, `pending`)
- `title` (string): Filter by book title (partial match)
- `authorName` (string): Filter by author name (partial match)
- `language` (string): Filter by language
- `publisher` (string): Filter by publisher (partial match)
- `publishedDate` (string): Filter by publication date
- `isbn13` (string): Filter by ISBN-13
- `isbn10` (string): Filter by ISBN-10
- `pageCountLt` (integer): Books with page count less than value
- `pageCountMt` (integer): Books with page count more than value
- `pageCountEq` (integer): Books with exact page count
- `collectionId` (integer): Filter by collection ID

**Success Response (200):**
```json
{
  "success": true,
  "msg": "Book details retrieved successfully",
  "data": {
    "books": [
      {
        "id": "abc123",
        "title": "The Great Gatsby",
        "author_name": "F. Scott Fitzgerald",
        "thumbnail": "https://books.google.com/books/content?id=abc123&printsec=frontcover&img=1&zoom=1",
        "published_date": "1925",
        "categories": "Fiction, Classics",
        "language": "en",
        "status": "reading"
      }
    ],
    "page": 1,
    "per_page": 9,
    "total_books": 25,
    "total_pages": 3
  }
}
```

#### Add Book to Library
```
POST /api/library/books/{bookId}
```

**Description:** Add a book to user's personal library

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Path Parameters:**
- `bookId` (string, required): Google Books ID of the book

**Success Response (201):**
```json
{
  "success": true,
  "msg": "Book added to your library",
  "data": 123
}
```

**Error Responses:**
```json
// 409 - Book already exists
{
  "success": false,
  "msg": "This book is already present in your library",
  "data": null
}

// 502 - Book not found in Google Books
{
  "success": false,
  "msg": "Book with searched id doesnt exist",
  "data": null
}
```

#### Remove Book from Library
```
DELETE /api/library/books/{bookId}
```

**Description:** Remove a book from user's personal library

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Path Parameters:**
- `bookId` (string, required): Google Books ID of the book

**Success Response (200):**
```json
{
  "success": true,
  "msg": "Book removed from your library",
  "data": null
}
```

**Error Responses:**
```json
// 404 - Book not in library
{
  "success": false,
  "msg": "This book is not in your personal library",
  "data": null
}
```

#### Update Book Status
```
PATCH /api/library/books/{bookId}
```

**Description:** Update reading status of a book in user's library

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Path Parameters:**
- `bookId` (string, required): Google Books ID of the book

**Request Body:**
```json
{
  "new_status": "completed"
}
```

**Parameters:**
- `new_status` (string, required): New reading status (`Reading`, `Completed`, `Pending`)

**Success Response (200):**
```json
{
  "success": true,
  "msg": "Book details updated",
  "data": null
}
```

### Collection Management Endpoints

#### Get User Collections
```
GET /api/collections/
```

**Description:** Retrieve all collections belonging to the user

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Success Response (200):**
```json
{
  "success": true,
  "msg": "Data retrieved successfully",
  "data": [
    {
      "collection_id": 1,
      "collection_name": "Favorites"
    },
    {
      "collection_id": 2,
      "collection_name": "To Read"
    }
  ]
}
```

#### Create Collection
```
POST /api/collections/
```

**Description:** Create a new book collection

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Request Body:**
```json
{
  "collection_name": "Science Fiction"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "msg": "New collection created successfully",
  "data": null
}
```

**Error Responses:**
```json
// 400 - Invalid input
{
  "success": false,
  "msg": "Provided input is invalid , refer to docs",
  "data": null
}
```

#### Delete Collection
```
DELETE /api/collections/{collection_id}
```

**Description:** Delete a collection and all its book associations

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Path Parameters:**
- `collection_id` (integer, required): ID of the collection to delete

**Success Response (200):**
```json
{
  "success": true,
  "msg": "Collection deleted permanently",
  "data": null
}
```

**Error Responses:**
```json
// 404 - Collection not found
{
  "success": false,
  "msg": "The collection you requested does not exist",
  "data": null
}
```

#### Rename Collection
```
PATCH /api/collections/{collection_id}
```

**Description:** Update the name of an existing collection

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Path Parameters:**
- `collection_id` (integer, required): ID of the collection to rename

**Request Body:**
```json
{
  "Collection_name": "Updated Collection Name"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "msg": "Collection details updated",
  "data": null
}
```

#### Add Book to Collection
```
POST /api/collections/{collection_id}/book/{book_id}
```

**Description:** Add a book to a specific collection

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Path Parameters:**
- `collection_id` (integer, required): ID of the collection
- `book_id` (string, required): Google Books ID of the book

**Success Response (201):**
```json
{
  "success": true,
  "msg": "The book has been added to the collection",
  "data": null
}
```

**Error Responses:**
```json
// 404 - Book not in library
{
  "success": false,
  "msg": "This book is not in your personal library",
  "data": null
}

// 409 - Book already in collection
{
  "success": false,
  "msg": "This book is already present in this collection",
  "data": null
}
```

#### Remove Book from Collection
```
DELETE /api/collections/{collection_id}/book/{book_id}
```

**Description:** Remove a book from a specific collection

**Authentication:** Required (JWT cookie)  
**Rate Limit:** Global default

**Path Parameters:**
- `collection_id` (integer, required): ID of the collection
- `book_id` (string, required): Google Books ID of the book

**Success Response (200):**
```json
{
  "success": true,
  "msg": "Book successfully deleted from the collection",
  "data": null
}
```

## Error Codes

| HTTP Code | Meaning | Example Response |
|-----------|---------|------------------|
| 400 | Bad Request | `{"success": false, "msg": "Provided input is invalid , refer to docs", "data": null}` |
| 401 | Unauthorized | `{"success": false, "msg": "Authentication token missing or invalid", "data": null}` |
| 403 | Forbidden | `{"success": false, "msg": "You do not have permission to perform this action", "data": null}` |
| 404 | Not Found | `{"success": false, "msg": "The book you are looking for does not exist in our catalog", "data": null}` |
| 409 | Conflict | `{"success": false, "msg": "An account with this email address already exists", "data": null}` |
| 415 | Unsupported Media Type | `{"success": false, "msg": "API expects data in json body", "data": null}` |
| 429 | Too Many Requests | Rate limit exceeded (handled by Flask-Limiter) |
| 500 | Internal Server Error | `{"success": false, "msg": "Something went wrong on our end. Please try again later", "data": null}` |
| 502 | Bad Gateway | `{"success": false, "msg": "Book with searched id doesnt exist", "data": null}` |

## Security Features

### CSRF Protection
- Enabled for all state-changing operations (POST, PUT, DELETE, PATCH)
- Automatically handled when using cookies
- CSRF token validation occurs server-side

### Security Headers
- **Content Security Policy (CSP):** Configured to allow Google Books images and fonts
- **Frame Options:** DENY (prevents clickjacking)
- **Referrer Policy:** strict-origin-when-cross-origin
- **HTTPS Enforcement:** Enabled in production

### Rate Limiting
- **Per-User Limits:** When authenticated, limits apply per user
- **Per-IP Limits:** When anonymous, limits apply per IP address
- **Sensitive Endpoints:** Authentication endpoints have stricter limits (5/minute)

## Example Usage

### cURL Examples

**Register a new user:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "usermail": "john@example.com",
    "password": "securePassword123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "usermail": "john@example.com",
    "password": "securePassword123"
  }'
```

**Search books (authenticated):**
```bash
curl -X GET "http://localhost:5000/api/books?query=python&page=1&limit=5" \
  -b cookies.txt
```

**Add book to library:**
```bash
curl -X POST http://localhost:5000/api/library/books/abc123 \
  -b cookies.txt
```

**Get user's library with filters:**
```bash
curl -X GET "http://localhost:5000/api/library/books?status=reading&page=1&limit=10" \
  -b cookies.txt
```

### Python Requests Examples

```python
import requests

# Create session to handle cookies
session = requests.Session()

# Register user
register_data = {
    "username": "john_doe",
    "usermail": "john@example.com",
    "password": "securePassword123"
}
response = session.post("http://localhost:5000/api/auth/register", json=register_data)
print(response.json())

# Login (cookies automatically stored in session)
login_data = {
    "usermail": "john@example.com",
    "password": "securePassword123"
}
response = session.post("http://localhost:5000/api/auth/login", json=login_data)
print(response.json())

# Search books (authenticated)
params = {"query": "python programming", "page": 1, "limit": 5}
response = session.get("http://localhost:5000/api/books", params=params)
books = response.json()
print(books)

# Add first book to library
if books["success"] and books["data"]:
    book_id = books["data"][0]["google_id"]
    response = session.post(f"http://localhost:5000/api/library/books/{book_id}")
    print(response.json())

# Get user's library
response = session.get("http://localhost:5000/api/library/books")
library = response.json()
print(library)

# Create a collection
collection_data = {"collection_name": "Programming Books"}
response = session.post("http://localhost:5000/api/collections/", json=collection_data)
print(response.json())

# Logout
response = session.post("http://localhost:5000/api/auth/logout")
print(response.json())
```

## Notes

1. **Token Expiration:** JWT tokens expire after 60 minutes. Users need to re-login after expiration.

2. **CSRF Protection:** All state-changing requests require CSRF token validation when using cookie authentication.

3. **Book IDs:** All book operations use Google Books API IDs, not internal database IDs.

4. **Pagination:** Most list endpoints support pagination with `page` and `limit` parameters.

5. **Case Sensitivity:** Status and language filters are case-insensitive (automatically converted to lowercase).

6. **Collection Ownership:** Users can only access and modify their own collections and library books.

7. **Third-Party Dependencies:** Book search relies on Google Books API availability.

8. **Database Transactions:** All database operations are wrapped in transactions with proper rollback on errors.
