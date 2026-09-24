# 📚 Course Management API (`02-course-api-pydantic`)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic_v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Security](https://img.shields.io/badge/Security-API_Key-green?style=for-the-badge&logo=springsecurity)](https://fastapi.tiangolo.com/tutorial/security/)

A robust, production-grade Course Management REST API backend built with **FastAPI** and **Pydantic v2**. This project adheres to standard modular REST architecture, enforcing strict schema validation, custom header-based API Key authentication, rolling window IP rate limiting, and dynamic query filtering.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Security & Authentication](#-security--authentication)
- [Rate Limiting Middleware](#-rate-limiting-middleware)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [Running the Server](#running-the-server)
  - [Public Tunneling (ngrok)](#public-tunneling-ngrok)
- [Data Schemas & Pydantic Validation](#-data-schemas--pydantic-validation)
- [API Endpoints & Usage](#-api-endpoints--usage)
- [Interactive Documentation](#-interactive-documentation)

---

## ✨ Features

- **Modular Project Layout:** Decoupled codebase (`app/main.py`, `app/models.py`, `app/database.py`, `app/security.py`).
- **Header-Based Authentication:** Protected mutating routes using native `APIKeyHeader(name="X-API-Key")`.
- **Client IP Rate Limiting:** Custom middleware tracking client request frequency (10 requests / 60-second window per IP).
- **Comprehensive Schema Enforcement:** Pydantic models with field boundary rules (`min_length`, `max_length`, `gt`, `ge`, `le`).
- **Partial Entity Updates:** Safe `PATCH` updates using `.model_dump(exclude_unset=True)`.
- **Dynamic Filter Operations:** Filter catalog by category, price bounds (`min_price`, `max_price`), and active publishing status.

---

## 📁 Project Structure

```text
02-course-api-pydantic/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI instance, route definitions & rate-limiting logic
│   ├── models.py        # Pydantic schemas (CourseCreate, CourseUpdate, CourseResponse)
│   ├── database.py      # In-memory data store & request tracking dictionary
│   └── security.py      # Native APIKeyHeader dependency & authentication logic
│
├── .gitignore
├── requirements.txt     # Framework & server dependencies
└── README.md            # Comprehensive project documentation
```

---

## 🔒 Security & Authentication

The API implements native header-based authentication via `APIKeyHeader(name="X-API-Key")` integrated directly with Swagger UI.

- **Header Name:** `X-API-Key`
- **Secret Key:** `test123`
- **Protected Routes:** State-mutating endpoints (`POST`, `PUT`, `PATCH`, `DELETE`).
- **Behavior:** Unauthenticated requests or invalid keys return HTTP `403 Forbidden`:
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```

---

## 🛡️ Rate Limiting Middleware

To safeguard the server from denial-of-service or brute-force requests, read endpoints inspect incoming request client metadata (`request.client.host`):

| Policy Metric | Rule |
| :--- | :--- |
| **Max Allowed Requests** | 10 requests |
| **Time Window** | 60 seconds rolling window per client IP |
| **Exceeded Status** | HTTP `429 Too Many Requests` |
| **Error Response** | `{"detail": "Rate limit exceeded. Try again later."}` |

---

## 🚀 Getting Started

### Prerequisites

Ensure Python 3.10+ is installed on your system.

### Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd 02-course-api-pydantic
   ```

2. **Create and activate a virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

Launch the development server using Uvicorn with auto-reload:

```bash
uvicorn app.main:app --reload
```

Access point URLs:
- **Base URL:** `http://127.0.0.1:8000`
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Public Tunneling (ngrok)

To expose your local development server to external clients:

```bash
ngrok http 8000
```

---

## 📋 Data Schemas & Pydantic Validation

| Model | Field | Type | Validation Rules | Description |
| :--- | :--- | :--- | :--- | :--- |
| **CourseCreate** | `title` | `str` | `min_length=3`, `max_length=100` | Course title |
| | `description` | `str` | `min_length=10`, `max_length=500` | Detailed syllabus |
| | `price` | `float` | `gt=0` | Price must be positive |
| | `duration` | `str` | `min_length=2` | Estimated duration (e.g. '8 weeks') |
| | `instructor` | `str` | `min_length=2` | Instructor full name |
| | `category` | `str` | `min_length=2` | Subject category (e.g. 'python') |
| | `rating` | `float` | `ge=0.0`, `le=5.0` | Rating out of 5.0 |
| | `active` | `bool` | Default: `True` | Publishing status |
| **CourseUpdate** | All fields | `Optional` | Same validation rules, default `None` | Partial payload model for `PATCH` |
| **CourseResponse** | `id` | `int` | Auto-incremented identifier | Primary key included in responses |

---

## 📡 API Endpoints & Usage

### 1. Public Root Check (`GET /`)

```bash
curl -X GET "http://127.0.0.1:8000/"
```

---

### 2. Create Course (`POST /courses`)

- **Header Required:** `X-API-Key: test123`
- **Status Code:** `201 Created`

```bash
curl -X POST "http://127.0.0.1:8000/courses" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{
    "title": "Mastering FastAPI & Pydantic",
    "description": "Comprehensive guide to building modern REST APIs using Python.",
    "price": 999.00,
    "duration": "10 weeks",
    "instructor": "Pavan Majji",
    "category": "python",
    "rating": 4.8,
    "active": true
  }'
```

---

### 3. List & Filter Courses (`GET /courses`)

- **Filter by Category:**
  ```bash
  curl -X GET "http://127.0.0.1:8000/courses?category=python"
  ```
- **Filter by Price Bounds:**
  ```bash
  curl -X GET "http://127.0.0.1:8000/courses?min_price=500&max_price=5000"
  ```
- **Filter by Active Status:**
  ```bash
  curl -X GET "http://127.0.0.1:8000/courses?active=true"
  ```
- **Combined Multi-Filter Query:**
  ```bash
  curl -X GET "http://127.0.0.1:8000/courses?category=python&min_price=500&max_price=5000&active=true"
  ```

---

### 4. Get Course By ID (`GET /courses/{course_id}`)

```bash
curl -X GET "http://127.0.0.1:8000/courses/1"
```

---

### 5. Idempotent Full Replacement (`PUT /courses/{course_id}`)

```bash
curl -X PUT "http://127.0.0.1:8000/courses/1" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{
    "title": "Advanced Python & FastAPI Architecture",
    "description": "Deep dive into production-grade microservices and design patterns.",
    "price": 1499.00,
    "duration": "12 weeks",
    "instructor": "Pavan Majji",
    "category": "python",
    "rating": 4.9,
    "active": true
  }'
```

---

### 6. Partial Field Update (`PATCH /courses/{course_id}`)

```bash
curl -X PATCH "http://127.0.0.1:8000/courses/1" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{
    "price": 799.00,
    "rating": 5.0
  }'
```

---

### 7. Delete Course (`DELETE /courses/{course_id}`)

```bash
curl -X DELETE "http://127.0.0.1:8000/courses/1" \
  -H "X-API-Key: test123"
```

---

## 📖 Interactive Documentation

- **Swagger UI:** Access `http://127.0.0.1:8000/docs` to test endpoints interactively (click **Authorize** and enter `test123` for API Key).
- **ReDoc:** Access `http://127.0.0.1:8000/redoc` for OpenAPI schema specifications.

---

## 📜 License

This project is created for educational and practical assessment purposes.