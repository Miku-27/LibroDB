# LibroDB API Documentation

## Overview

**LibroDB** is a personal library management system that provides a RESTful API for managing book collections, user authentication, and library operations. The API allows users to search for books using the Google Books API, maintain personal libraries, track reading progress, and organize books into custom collections.

### Key Features
- **User Authentication**: JWT-based authentication with HttpOnly cookies
- **Book Search**: Integration with Google Books API for global book search
- **Personal Library**: Add, remove, and manage books in your personal library
- **Reading Status Tracking**: Track books as Reading, Completed, or Pending
- **Collections**: Create and manage custom book collections
- **Security**: CSRF protection, rate limiting, and secure headers

### Base Information
- **Base URL**: `Domain/api`
- **Version**: 0.1.0
- **Authentication**: JWT tokens stored in HttpOnly cookies
- **Content Type**: `application/json`
- **Rate Limiting**: 200 requests per day (global), 5 requests per minute (auth endpoints)

---

## Authentication

All API endpoints except authentication routes require a valid JWT token. The token is automatically stored in an HttpOnly cookie upon successful login and included in subsequent requests.

### Security Features
- **JWT Tokens**: 60-minute expiration, stored in HttpOnly cookies
- **CSRF Protection**: Required for POST, PUT, DELETE, PATCH requests
- **Rate Limiting**: Per-user (authenticated) or per-IP (anonymous)
- **Secure Headers**: CSP, Frame Options, Referrer Policy

---

## API Endpoints by Group

## Authentication API (`/api/auth`)

### Register User
```http
POST /api/auth/user
```

Create a new user account.

**Rate Limit**: 5 requests per minute

**Request Body**:
```json
{
  "username": "john_doe",
  "usermail": "john@example.com",
  "password": "securePassword123"
}
```

**Success Response (201)**:
```json
{
  "success": true,
  "msg": "Your account has been created successfully",
  "data": null
}
```

**Error Responses**:
- `400`: Invalid email format
- `409`: User already exists
- `415`: Invalid content type (not JSON)

---

### Login User
```http
POST /api/auth/token
```

Authenticate user and receive JWT cookie.

**Rate Limit**: 5 requests per minute

**Request Body**:
```json
{
  "usermail": "john@example.com",
  "password": "securePassword123"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "Successfully logged in",
  "data": null
}
```
*JWT token is automatically set as HttpOnly cookie*

**Error Responses**:
- `401`: Invalid credentials
- `415`: Invalid content type

---

### Logout User
```http
DELETE /api/auth/token
```

Clear JWT cookie and logout user.

**Rate Limit**: 5 requests per minute

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "You have been logged out",
  "data": null
}
```

---

### Change Password
```http
PATCH /api/auth/user
```

Change user password (requires authentication).

**Rate Limit**: 2 requests per minute

**Request Body**:
```json
{
  "oldPassword": "currentPassword",
  "newPassword": "newSecurePassword"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "Password was successfully updated",
  "data": null
}
```

---

### Password Reset Request
```http
POST /api/auth/password-reset
```

Request password reset email.

**Rate Limit**: 1 request per minute

**Request Body**:
```json
{
  "usermail": "john@example.com"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "If an account is associated with this email, you will receive a reset link shortly.",
  "data": null
}
```

---

### Password Reset
```http
PATCH /api/auth/password-reset
```

Reset password using reset token.

**Rate Limit**: 1 request per minute

**Request Body**:
```json
{
  "resetToken": "reset_token_here",
  "newPassword": "newSecurePassword"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "Password was successfully updated",
  "data": null
}
```

---

## Book Search API (`/api/books`)

### Search Books Globally
```http
GET /api/books?query={search_term}&page={page}&limit={limit}
```

Search books using Google Books API.

**Authentication**: Required  
**Rate Limit**: Global default (200/day)

**Query Parameters**:
- `query` (string, required): Search term for books
- `page` (integer, optional, default=1): Page number for pagination
- `limit` (integer, optional, default=9): Number of books per page

**Success Response (200)**:
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

**Error Responses**:
- `400`: Invalid input parameters
- `502`: Google Books API error

---

## Library Management API (`/api/library`)

### Get User's Library
```http
GET /api/library/books?page={page}&limit={limit}&status={status}&title={title}...
```

Retrieve user's personal book library with filtering and pagination.

**Authentication**: Required  
**Rate Limit**: Global default

**Query Parameters** (all optional):
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

**Success Response (200)**:
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

---

### Add Book to Library
```http
POST /api/library/books/{bookId}
```

Add a book to user's personal library.

**Authentication**: Required  
**Rate Limit**: Global default

**Path Parameters**:
- `bookId` (string, required): Google Books ID of the book

**Success Response (201)**:
```json
{
  "success": true,
  "msg": "Book added to your library",
  "data": 123
}
```

**Error Responses**:
- `409`: Book already exists in library
- `502`: Book not found in Google Books

---

### Remove Book from Library
```http
DELETE /api/library/books/{bookId}
```

Remove a book from user's personal library.

**Authentication**: Required  
**Rate Limit**: Global default

**Path Parameters**:
- `bookId` (string, required): Google Books ID of the book

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "Book removed from your library",
  "data": null
}
```

**Error Responses**:
- `404`: Book not in library

---

### Update Book Status
```http
PATCH /api/library/books/{bookId}
```

Update reading status of a book in user's library.

**Authentication**: Required  
**Rate Limit**: Global default

**Path Parameters**:
- `bookId` (string, required): Google Books ID of the book

**Request Body**:
```json
{
  "new_status": "completed"
}
```

**Parameters**:
- `new_status` (string, required): New reading status (`Reading`, `Completed`, `Pending`)

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "Book details updated",
  "data": null
}
```

**Error Responses**:
- `400`: Invalid status value
- `404`: Book not in library

---

## Collection Management API (`/api/collections`)

### Get User Collections
```http
GET /api/collections/
```

Retrieve all collections belonging to the user.

**Authentication**: Required  
**Rate Limit**: Global default

**Success Response (200)**:
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

---

### Create Collection
```http
POST /api/collections/
```

Create a new book collection.

**Authentication**: Required  
**Rate Limit**: Global default

**Request Body**:
```json
{
  "collection_name": "Science Fiction"
}
```

**Success Response (201)**:
```json
{
  "success": true,
  "msg": "New collection created successfully",
  "data": null
}
```

**Error Responses**:
- `400`: Invalid input (empty collection name)
- `415`: Invalid content type

---

### Delete Collection
```http
DELETE /api/collections/{collection_id}
```

Delete a collection and all its book associations.

**Authentication**: Required  
**Rate Limit**: Global default

**Path Parameters**:
- `collection_id` (integer, required): ID of the collection to delete

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "Collection deleted permanently",
  "data": null
}
```

**Error Responses**:
- `404`: Collection not found

---

### Rename Collection
```http
PATCH /api/collections/{collection_id}
```

Update the name of an existing collection.

**Authentication**: Required  
**Rate Limit**: Global default

**Path Parameters**:
- `collection_id` (integer, required): ID of the collection to rename

**Request Body**:
```json
{
  "Collection_name": "Updated Collection Name"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "Collection details updated",
  "data": null
}
```

**Error Responses**:
- `400`: Invalid input (empty collection name)
- `404`: Collection not found

---

### Add Book to Collection
```http
POST /api/collections/{collection_id}/book/{book_id}
```

Add a book to a specific collection.

**Authentication**: Required  
**Rate Limit**: Global default

**Path Parameters**:
- `collection_id` (integer, required): ID of the collection
- `book_id` (string, required): Google Books ID of the book

**Success Response (201)**:
```json
{
  "success": true,
  "msg": "The book has been added to the collection",
  "data": null
}
```

**Error Responses**:
- `404`: Book not in library or collection not found
- `409`: Book already in collection

---

### Remove Book from Collection
```http
DELETE /api/collections/{collection_id}/book/{book_id}
```

Remove a book from a specific collection.

**Authentication**: Required  
**Rate Limit**: Global default

**Path Parameters**:
- `collection_id` (integer, required): ID of the collection
- `book_id` (string, required): Google Books ID of the book

**Success Response (200)**:
```json
{
  "success": true,
  "msg": "Book successfully deleted from the collection",
  "data": null
}
```

**Error Responses**:
- `404`: Book not in collection or collection not found

---

## Error Codes Reference

| HTTP Code | Meaning | Common Causes |
|-----------|---------|---------------|
| 400 | Bad Request | Invalid input parameters, missing required fields |
| 401 | Unauthorized | Invalid credentials, expired token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist (book, collection, user) |
| 409 | Conflict | Resource already exists (duplicate book, user) |
| 415 | Unsupported Media Type | Request not in JSON format |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 502 | Bad Gateway | Third-party API error (Google Books) |

---

## Response Format

All API responses follow a consistent format:

```json
{
  "success": boolean,
  "msg": "Human-readable message",
  "data": object|array|null
}
```

- `success`: Indicates if the request was successful
- `msg`: Human-readable message describing the result
- `data`: Response data (varies by endpoint, null for operations without return data)

---

## Rate Limiting

- **Global Default**: 200 requests per day per user/IP
- **Authentication Endpoints**: 5 requests per minute
- **Password Change**: 2 requests per minute  
- **Password Reset**: 1 request per minute
- **Key Function**: User-based (authenticated) or IP-based (anonymous)

Rate limit information is included in response headers.

---

## Notes

1. **Token Expiration**: JWT tokens expire after 60 minutes. Re-login required after expiration.

2. **CSRF Protection**: Automatically handled when using cookies. Custom headers required for state-changing operations.

3. **Book IDs**: All book operations use Google Books API IDs, not internal database IDs.

4. **Case Sensitivity**: Status and language filters are case-insensitive.

5. **Collection Ownership**: Users can only access their own collections and library books.

6. **Database Transactions**: All operations use transactions with automatic rollback on errors.

7. **Third-Party Dependencies**: Book search functionality depends on Google Books API availability.
