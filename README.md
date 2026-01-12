# LibroDB - Personal Library Management System

**LibroDB** is a clean, opinionated personal book library management system. Built as a focused engineering project, it emphasizes backend clarity, structured data modeling, and a "UI without complexity" philosophy.

The system allows users to search the global Google Books catalog, maintain a personal digital library, track reading progress, and organize books into custom collections.

---

## 🚀 Project Philosophy

This project was built to explore the end-to-end development of a secure web system without relying on heavy frameworks that obscure underlying logic.

* **Clarity over Scale:** Focused on clean structure and easy-to-reason-about data models.
* **Intentional Simplicity:** A minimal UI using Alpine.js and Tailwind CSS designed to support, not overshadow, the backend.
* **Security First:** Implementation of JWT-based authentication via HttpOnly cookies and robust CSRF protection.

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python) for request/response handling.
* **Database:** Managed MySQL (Aiven) with SSL/TLS connections and version-controlled migrations.
* **Frontend:** Alpine.js for reactive UI (no build step required) and Tailwind CSS for maintainable styling.
* **Authentication:** JWT tokens stored in HttpOnly cookies.
* **Integrations:** Google Books API for external book data.

---

## ✨ Key Features

* **Structured Library Model:** A schema-driven approach to manage book relationships and user data.
* **Search & Filtering:** Robust search functionality allowing filters by title, author, status, language, and page counts.
* **Collection Management:** Create, rename, and organize books into custom-named collections.
* **Reading Status Tracking:** Track your progress through categories like `Reading`, `Completed`, and `Pending`.
* **Security & Rate Limiting:**
* **Global Rate Limit:** 200 requests/day.
* **Auth Rate Limit:** 5 requests/minute for sensitive endpoints.
* **CSRF Protection:** Enabled for all state-changing operations (POST, PATCH, DELETE).



---

## 📖 API Overview

The API is versioned at `v0.1.0` and follows RESTful principles.

### Authentication Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Create a new user account |
| `POST` | `/api/auth/login` | Authenticate and receive JWT cookie |
| `POST` | `/api/auth/logout` | Clear session cookies |

### Library & Collection Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/books` | Search Google Books API |
| `GET` | `/api/library/books` | View your filtered personal library |
| `POST` | `/api/library/books/{id}` | Add a book to your library |
| `PATCH` | `/api/library/books/{id}` | Update reading status |
| `POST` | `/api/collections/` | Create a new collection |
| `POST` | `/api/collections/{id}/book/{id}` | Add library book to collection |

---

## 🛠️ Getting Started

### Prerequisites

* Python 3.x
* MySQL Instance
* Google Books API access (optional for certain features)

### Quick Start (Python Requests)

```python
import requests

session = requests.Session()

# Login
login_data = {"usermail": "user@example.com", "password": "yourpassword"}
session.post("http://localhost:5000/api/auth/login", json=login_data)

# Search for a book
params = {"query": "The Great Gatsby"}
response = session.get("http://localhost:5000/api/books", params=params)
print(response.json())

```

---

## 🛡️ Security Implementation

To prevent common vulnerabilities, LibroDB implements:

1. **HttpOnly/Secure Cookies:** Prevents JavaScript-based token theft.
2. **CSRF Tokens:** Required in custom headers for all state-changing requests.
3. **Security Headers:** Configured Content Security Policy (CSP), Frame Options (DENY), and Referrer Policy.

---

## 🚧 Known Issues & Roadmap
- **Password Reset:** Currently disabled in production due to Render's outbound SMTP 
  limitations on the Free Tier.
- **Planned Fix:** Migrating from `smtplib` to a REST API-based provider (SendGrid/Resend) 
  to bypass port restrictions.

  ---
## 📝 Notes

* **Token Expiration:** JWTs expire every 60 minutes.
* **Case Sensitivity:** Status and language filters are automatically normalized to lowercase.
* **Database:** All operations use transactions with automatic rollback on failure.

---

## ⚖️ Disclaimer & Data Usage
This project is a personal portfolio piece built for educational and engineering demonstration purposes. 
- **Non-Commercial:** This application is not a commercial product. It is not used to generate revenue, nor is the data accessed through the API sold or distributed to third parties.
- **Data Source:** Book metadata (titles, authors, descriptions) is fetched via the [Google Books API](https://developers.google.com/books).
- **Attribution:** All book information and cover images are property of their respective owners and Google Books.
