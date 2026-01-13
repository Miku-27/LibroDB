# LibroDB - Personal Library Management System
## Complete Project Documentation

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [What LibroDB Does](#what-librodb-does)
3. [How It Works](#how-it-works)
4. [Technology Stack](#technology-stack)
5. [Project Architecture](#project-architecture)
6. [Database Design](#database-design)
7. [Security Implementation](#security-implementation)
8. [API Design](#api-design)
9. [Frontend Implementation](#frontend-implementation)

---

## Project Overview

**LibroDB** is a full-stack personal library management system designed to help users organize, track, and manage their book collections. Built with a focus on clean architecture, security, and user experience, it provides a comprehensive solution for book enthusiasts who want to maintain digital catalogs of their reading materials.

### Key Objectives
- **Personal Library Management**: Create and maintain a digital catalog of books
- **Reading Progress Tracking**: Monitor reading status (Reading, Completed, Pending)
- **Collection Organization**: Group books into custom collections
- **Book Discovery**: Search and discover books through Google Books API integration
- **Secure User Management**: Robust authentication and authorization system

---
## What LibroDB Does

### Core Functionality

#### 1. User Management
- **User Registration**: Create accounts with email verification
- **Authentication**: Secure login/logout with JWT tokens
- **Password Management**: Change passwords and reset forgotten passwords
- **Session Management**: Automatic token expiration

#### 2. Book Search & Discovery
- **Global Search**: Search millions of books via Google Books API
- **Detailed Information**: Access comprehensive book metadata (title, author, publisher, ISBN, etc.)
- **Cover Images**: Display book thumbnails and covers
- **Pagination**: Navigate through search results efficiently

#### 3. Personal Library Management
- **Add Books**: Save books from search results to personal library
- **Remove Books**: Delete books from personal collection
- **Status Tracking**: Mark books as Reading, Completed, or Pending
- **Advanced Filtering**: Filter library by multiple criteria (status, author, language, page count, etc.)
- **Pagination**: Navigate through large personal libraries

#### 4. Collection Management
- **Create Collections**: Organize books into custom-named groups
- **Manage Collections**: Rename or delete collections
- **Book Assignment**: Add/remove books from collections
- **Collection Filtering**: View library books by specific collections

#### 5. Data Management
- **Persistent Storage**: All data stored in MySQL database
- **Data Integrity**: Foreign key constraints and transaction management
- **Backup Support**: Database migration system for schema changes

---

## How It Works

### System Flow


#### 2. Technical Flow
```
Frontend (Alpine.js) → API Layer (Flask) → Service Layer → Database (MySQL) → External APIs (Google Books)
```

### Request Processing
1. **Frontend**: User interacts with Alpine.js-powered interface
2. **Authentication**: JWT token validation for protected routes
3. **Rate Limiting**: Request throttling based on user/IP
4. **API Layer**: Flask routes handle HTTP requests
5. **Service Layer**: Business logic processing
6. **Database**: MySQL operations with transaction management
7. **External APIs**: Google Books integration for book data
8. **Response**: JSON responses back to frontend

---

## Technology Stack

### Backend Technologies

#### Core Framework
- **Flask (3.1.2)**: Lightweight Python web framework
  - *Purpose*: HTTP request handling, routing, and response management
  - *Why chosen*: Minimal overhead, explicit control, easy to understand

#### Database & ORM
- **MySQL**: Relational database management system
  - *Purpose*: Persistent data storage with ACID compliance
  - *Why chosen*: Mature, reliable, excellent for relational data
- **Flask-SQLAlchemy (3.1.1)**: Python SQL toolkit and ORM
  - *Purpose*: Database abstraction and object-relational mapping
  - *Why chosen*: Pythonic database operations, migration support
- **PyMySQL (1.1.2)**: Pure Python MySQL client
  - *Purpose*: MySQL database connectivity
  - *Why chosen*: Pure Python implementation, no external dependencies
- **Flask-Migrate (4.1.0)**: Database migration handling
  - *Purpose*: Version control for database schema changes
  - *Why chosen*: Alembic integration, seamless schema evolution

#### Authentication & Security
- **Flask-JWT-Extended (4.7.1)**: JWT token management
  - *Purpose*: Secure user authentication with JSON Web Tokens
  - *Why chosen*: HttpOnly cookie support, CSRF protection, token refresh
- **Flask-Talisman (1.1.0)**: Security headers and CSP
  - *Purpose*: HTTP security headers, Content Security Policy
  - *Why chosen*: Comprehensive security header management
- **Werkzeug**: Password hashing utilities
  - *Purpose*: Secure password storage with bcrypt
  - *Why chosen*: Built into Flask, industry-standard hashing

#### Rate Limiting & Performance
- **Flask-Limiter (4.1.1)**: Request rate limiting
  - *Purpose*: Prevent abuse and ensure fair resource usage
  - *Why chosen*: Flexible rate limiting strategies, Redis support
- **Redis (7.1.0)**: In-memory data store
  - *Purpose*: Rate limiting storage and caching
  - *Why chosen*: High performance, persistence options

#### External Integrations
- **Requests (2.32.5)**: HTTP library for API calls
  - *Purpose*: Google Books API integration
  - *Why chosen*: Simple, reliable HTTP client
- **Google Books API**: Book metadata and search
  - *Purpose*: Access to millions of book records
  - *Why chosen*: Comprehensive book database, free tier available

#### Configuration & Environment
- **Python-dotenv (1.2.1)**: Environment variable management
  - *Purpose*: Configuration management across environments
  - *Why chosen*: Simple .env file support, development/production separation

#### Server
- **Gunicorn (23.0.0)**: WSGI HTTP Server
  - *Purpose*: Production-ready Python web server
  - *Why chosen*: Robust, scalable, industry standard

### Frontend Technologies

#### Core Framework
- **Alpine.js**: Lightweight reactive framework
  - *Purpose*: Interactive UI components without build step
  - *Why chosen*: Minimal learning curve, no compilation required
- **Tailwind CSS**: Utility-first CSS framework
  - *Purpose*: Rapid UI development with consistent design
  - *Why chosen*: Utility classes, responsive design, maintainable styles

#### Static Assets
- **Custom CSS**: Additional styling for specific components
- **Custom JavaScript**: Page-specific functionality and API interactions
- **Default Images**: Fallback book covers and UI assets

### Development Tools

#### Package Management
- **Poetry**: Python dependency management
  - *Purpose*: Reproducible builds, virtual environment management
  - *Why chosen*: Modern Python packaging, lock file support

#### Database Tools
- **Alembic**: Database migration tool (via Flask-Migrate)
  - *Purpose*: Version-controlled schema changes
  - *Why chosen*: Automatic migration generation, rollback support

---

## Project Architecture

### Directory Structure
```
librodb/
├── app/                          # Main application package
│   ├── api/                      # API layer (REST endpoints)
│   │   ├── auth_api.py          # Authentication endpoints
│   │   ├── book_api.py          # Book search endpoints
│   │   ├── collection_api.py    # Collection management endpoints
│   │   ├── library_api.py       # Library management endpoints
│   │   └── __init__.py          # API blueprint registration
│   ├── pages/                    # Web page routes
│   │   ├── views.py             # HTML page rendering
│   │   └── __init__.py          # Pages blueprint
│   ├── services/                 # Business logic layer
│   │   ├── auth_services.py     # Authentication business logic
│   │   ├── collection_service.py # Collection operations
│   │   ├── email_service.py     # Email functionality
│   │   ├── google_api_services.py # Google Books integration
│   │   └── library_service.py   # Library operations
│   ├── static/                   # Frontend assets
│   │   ├── css/                 # Stylesheets
│   │   ├── js/                  # JavaScript files
│   │   └── covers/              # Book cover images
│   ├── templates/               # HTML templates
│   │   ├── partials/            # Reusable template components
│   │   └── *.html               # Page templates
│   ├── utils/                   # Utility functions
│   │   ├── codes.py             # Response codes and messages
│   │   ├── filter_verifier.py   # Input validation
│   │   ├── library_helper.py    # Library-specific utilities
│   │   ├── logger.py            # Logging configuration
│   │   └── ratelimit_helper.py  # Rate limiting utilities
│   ├── extensions.py            # Flask extension initialization
│   ├── models.py                # Database models
│   └── __init__.py              # Application factory
├── migrations/                   # Database migrations
├── config.py                    # Configuration classes
├── run.py                       # Application entry point
├── pyproject.toml               # Project dependencies
└── README.md                    # Project documentation
```

### Architectural Patterns

#### 1. Layered Architecture
- **Presentation Layer**: Templates and static files
- **API Layer**: REST endpoints and request handling
- **Service Layer**: Business logic and external integrations
- **Data Layer**: Database models and operations

#### 2. Blueprint Pattern
- **Modular Organization**: Separate blueprints for API and pages
- **Namespace Isolation**: Clear separation of concerns
- **Scalable Structure**: Easy to add new modules

#### 3. Factory Pattern
- **Application Factory**: `create_app()` function for flexible app creation
- **Configuration Management**: Environment-specific settings
- **Extension Initialization**: Centralized setup of Flask extensions

#### 4. Service Layer Pattern
- **Business Logic Separation**: Services handle complex operations
- **Reusability**: Services can be used by multiple API endpoints
- **Testability**: Isolated business logic for easier testing

---

## Database Design

### Entity Relationship Model

#### Core Entities

##### 1. User
```sql
- id (Primary Key)
- username (String, 80 chars)
- email (Unique, String, 120 chars)
- password_hash (String, 200 chars)
```

##### 2. Book
```sql
- id (Primary Key)
- google_id (Unique, String, 100 chars)
- title (String, 300 chars)
- author_name (String, 100 chars)
- publisher (String, 100 chars)
- published_date (String, 50 chars)
- description (Text)
- page_count (Integer)
- categories (String, 100 chars)
- language (String, 100 chars)
- info_link (String, 512 chars)
- thumbnail (String, 512 chars)
- isbn_13 (Unique, String, 13 chars)
- isbn_10 (Unique, String, 10 chars)
```

##### 3. UserBooks (Association Table)
```sql
- id (Primary Key)
- user_id (Foreign Key → User.id)
- book_id (Foreign Key → Book.id)
- status (Enum: reading, completed, pending)
- Unique Constraint: (user_id, book_id)
```

##### 4. UserCollection
```sql
- collection_id (Primary Key)
- user_id (Foreign Key → User.id)
- collection_name (String, 50 chars)
```

##### 5. CollectionBooks
```sql
- collection_id (Primary Key, Foreign Key → UserCollection.collection_id)
- user_book_id (Primary Key, Foreign Key → UserBooks.id)
```

##### 6. PasswordResetToken
```sql
- id (Primary Key)
- user_id (Foreign Key → User.id)
- reset_token (String, 255 chars)
- expires_at (DateTime)
- token_used (Boolean, default: False)
```

### Relationships

#### 1. User ↔ Books (Many-to-Many)
- **Through**: UserBooks association table
- **Additional Data**: Reading status per user-book relationship
- **Cascade**: Delete user removes all their book associations

#### 2. User ↔ Collections (One-to-Many)
- **Direct Relationship**: User owns multiple collections
- **Cascade**: Delete user removes all their collections

#### 3. Collections ↔ Books (Many-to-Many)
- **Through**: CollectionBooks association table
- **Constraint**: Books must be in user's library before adding to collections
- **Cascade**: Delete collection removes all book associations

### Database Features

#### 1. Data Integrity
- **Foreign Key Constraints**: Maintain referential integrity
- **Unique Constraints**: Prevent duplicate entries
- **Cascade Deletes**: Automatic cleanup of related records

#### 2. Performance Optimization
- **Connection Pooling**: Efficient database connection management
- **Query Optimization**: Efficient joins and filtering

#### 3. Migration Support
- **Version Control**: Track schema changes over time
- **Rollback Capability**: Revert problematic migrations
- **Environment Consistency**: Same schema across dev/prod

---

## Security Implementation

### Authentication & Authorization

#### 1. JWT Token System
- **Token Storage**: HttpOnly cookies (not accessible via JavaScript)
- **Token Expiration**: 60-minute lifetime with automatic cleanup
- **Token Validation**: Middleware validates tokens on protected routes

#### 2. Password Security
- **Hashing**: Werkzeug's bcrypt implementation
- **Verification**: Secure password comparison
- **Reset Mechanism**: Time-limited reset tokens

### Request Security

#### 1. CSRF Protection
- **Token Generation**: Automatic CSRF token creation
- **Cookie Integration**: CSRF tokens in separate cookies
- **Method Coverage**: POST, PUT, DELETE, PATCH requests

#### 2. Rate Limiting
- **Global Limits**: 200 requests per day per user/IP
- **Endpoint-Specific**: Stricter limits for sensitive operations
- **Authentication Endpoints**: 5 requests per minute
- **Password Operations**: 1-2 requests per minute
- **Storage**: Redis-backed for in-memory storage

### HTTP Security

#### 1. Security Headers (via Talisman)
- **Content Security Policy**: Restrict resource loading
- **Frame Options**: Prevent clickjacking (DENY)
- **Referrer Policy**: Control referrer information
- **HTTPS Enforcement**: Redirect HTTP to HTTPS in production

#### 2. Content Security Policy
```javascript
{
  "default-src": ["'self'"],
  "img-src": ["'self'", "books.google.com", "*.googleusercontent.com"],
  "style-src": ["'self'", "fonts.googleapis.com", "'unsafe-inline'"],
  "font-src": ["'self'", "fonts.gstatic.com"],
  "script-src": ["'self'", "'unsafe-eval'"]
}
```

### Data Protection

#### 1. Input Validation
- **Email Validation**: Regex pattern matching
- **Data Sanitization**: Strip and validate user inputs
- **Type Checking**: Ensure correct data types
- **Length Limits**: Prevent buffer overflow attacks

#### 2. SQL Injection Prevention
- **ORM Usage**: SQLAlchemy parameterized queries
- **No Raw SQL**: Avoid direct SQL string construction
- **Input Escaping**: Automatic parameter escaping

#### 3. Error Handling
- **Generic Messages**: Don't expose internal details
- **Logging**: Server-side error logging
- **Graceful Degradation**: User-friendly error responses

---

## API Design

### RESTful Principles

#### 1. Resource-Based URLs
- **Collections**: `/api/collections/`
- **Specific Resources**: `/api/collections/{id}`
- **Nested Resources**: `/api/collections/{id}/book/{bookId}`
- **Actions**: Represented by HTTP methods

#### 2. HTTP Methods
- **GET**: Retrieve data (idempotent)
- **POST**: Create new resources
- **PATCH**: Partial updates
- **DELETE**: Remove resources

#### 3. Status Codes
- **2xx**: Success responses (200, 201)
- **4xx**: Client errors (400, 401, 404, 409)
- **5xx**: Server errors (500, 502)

### Response Format

#### 1. Consistent Structure
```json
{
  "success": boolean,
  "msg": "Human-readable message",
  "data": object|array|null
}
```

#### 2. Error Handling
- **Standardized Codes**: Internal result codes mapped to HTTP status
- **User-Friendly Messages**: Clear, actionable error descriptions
- **No Sensitive Data**: Avoid exposing internal system details

#### 3. Pagination
```json
{
  "success": true,
  "msg": "Data retrieved successfully",
  "data": {
    "books": [...],
    "page": 1,
    "per_page": 9,
    "total_books": 25,
    "total_pages": 3
  }
}
```

### API Features

#### 1. Filtering & Search
- **Multiple Criteria**: Combine various filters
- **Partial Matching**: Title and author substring search
- **Range Queries**: Page count comparisons
- **Status Filtering**: Reading progress states

#### 2. Pagination
- **Page-Based**: Simple page/limit parameters
- **Configurable Limits**: Adjustable results per page
- **Total Counts**: Provide pagination metadata

#### 3. Validation
- **Input Sanitization**: Clean and validate all inputs
- **Type Checking**: Ensure correct parameter types
- **Required Fields**: Validate mandatory parameters

---

## Frontend Implementation

### Technology Choices

#### 1. Alpine.js
- **Reactive Components**: Data binding and event handling
- **No Build Step**: Direct browser execution
- **Minimal Learning Curve**: HTML-first approach
- **Small Footprint**: Lightweight framework

#### 2. Tailwind CSS
- **Utility Classes**: Rapid styling without custom CSS
- **Maintainable**: No CSS specificity issues

### Page-Specific Templates
- **Login/Register**: Authentication forms
- **Search**: Book discovery interface
- **Library**: Personal book management
- **Collections**: Organization tools
- **Book Details**: Individual book information

### JavaScript Architecture

#### 1. Page-Specific Scripts
- **Modular Approach**: Separate JS files per page
- **API Integration**: Fetch-based HTTP requests
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during operations

#### 2. Common Utilities
- **Base Functions**: Shared utility functions
- **API Helpers**: Common request patterns

## Development Setup

### Prerequisites
- Python 3.12+
- MySQL 8.0+
- Redis (for production rate limiting)
- Poetry (Python package manager)

### Local Development

#### 1. Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd librodb

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Copy environment template
cp env.example .env
```

#### 2. Configuration
```bash
# Edit .env file with your settings
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL_DEV=mysql+pymysql://user:password@localhost/librodb_dev
```

#### 3. Database Setup
```bash
# Initialize database
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

#### 4. Run Application
```bash
# Development server
python run.py

# Or with Flask CLI
flask run --host=0.0.0.0 --port=5000
```

