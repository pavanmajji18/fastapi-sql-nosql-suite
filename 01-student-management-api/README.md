# 🎓 Student Management REST API (`01-student-management-api`)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic_v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

A high-performance, production-ready RESTful API built with **FastAPI** and **Pydantic v2**. This service implements complete CRUD (Create, Read, Update, Delete) operations for managing student records using an in-memory data store, illustrating standard HTTP verbs, status codes, query filtering, and schema validation.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [Running the Server](#running-the-server)
- [API Specification](#-api-specification)
  - [Endpoints Overview](#endpoints-overview)
  - [Data Schemas](#data-schemas)
  - [Sample Requests & Responses](#sample-requests--responses)
- [HTTP Status Codes Reference](#-http-status-codes-reference)
- [Interactive Documentation](#-interactive-documentation)

---

## ✨ Features

- **Standard REST Architecture:** Fully compliant HTTP method semantics (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
- **Strict Data Validation:** Pydantic v2 models enforce string length constraints, valid email formats (`EmailStr`), GPA ranges, and age bounds.
- **Differentiated Resource Updates:**
  - `PUT /students/{id}` performs an idempotent, full entity replacement.
  - `PATCH /students/{id}` executes partial updates via `.model_dump(exclude_unset=True)`.
- **Dynamic Query Filtering:** Search students dynamically by `major` and `min_gpa`.
- **Robust Error Handling:** Explicit HTTP status codes (`201 Created`, `204 No Content`, `400 Bad Request`, `404 Not Found`, `422 Unprocessable Entity`).
- **Interactive OpenAPI Documentation:** Auto-generated Swagger UI and ReDoc endpoints.

---

## 🛠 Architecture & Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Modern, fast web framework for building APIs |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) | Data parsing, type enforcement, and validation (with `email-validator`) |
| **ASGI Web Server** | [Uvicorn](https://www.uvicorn.org/) | Lightning-fast ASGI server |
| **Data Store** | In-Memory Dictionary (`Dict[int, dict]`) | Lightweight in-memory persistence layer |

---

## 📁 Project Structure

```text
01-student-management-api/
│
├── main.py              # Application entrypoint, schemas, and routing
├── requirements.txt     # Python dependencies
└── README.md            # Comprehensive project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed on your system.

### Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd 01-student-management-api
   ```

2. **Create a virtual environment:**
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

Start the development server with live reload:

```bash
uvicorn main:app --reload
```

> [!TIP]
> If `uvicorn` is not recognized in your terminal path, invoke it using Python module syntax:
> ```bash
> python -m uvicorn main:app --reload
> ```

Access point URLs:
- **Base URL:** `http://127.0.0.1:8000`
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## 📡 API Specification

### Endpoints Overview

| Method | Route | Description | Success Status |
| :--- | :--- | :--- | :--- |
| `POST` | `/students` | Register a new student | `201 Created` |
| `GET` | `/students` | Retrieve all students (filterable by `major`, `min_gpa`) | `200 OK` |
| `GET` | `/students/{id}` | Retrieve a student by ID | `200 OK` |
| `PUT` | `/students/{id}` | Replace student details entirely | `200 OK` |
| `PATCH` | `/students/{id}` | Partially update student fields | `200 OK` |
| `DELETE` | `/students/{id}` | Delete a student record | `204 No Content` |

---

### Data Schemas

#### 1. Student Payload (`StudentCreate`)

| Field | Type | Constraints | Example |
| :--- | :--- | :--- | :--- |
| `name` | `string` | Length: 2 – 50 characters | `"Pavan Majji"` |
| `email` | `string` | Valid RFC email syntax | `"pavan.majji@example.com"` |
| `age` | `integer` | Value between 5 and 99 (`gt=4, lt=100`) | `24` |
| `major` | `string` | Length: 2 – 50 characters | `"Computer Science"` |
| `gpa` | `float` | Value between 0.0 and 4.0 | `3.85` |

#### 2. Student Response (`StudentResponse`)

Includes all fields from `StudentCreate` plus:
- `id`: Unique auto-incrementing integer identifier.

---

### Sample Requests & Responses

#### 1. Create Student (`POST /students`)

```bash
curl -X POST "http://127.0.0.1:8000/students" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Pavan Majji",
       "email": "pavan.majji@example.com",
       "age": 24,
       "major": "Computer Science",
       "gpa": 3.85
     }'
```

**Response (`201 Created`):**
```json
{
  "id": 1,
  "name": "Pavan Majji",
  "email": "pavan.majji@example.com",
  "age": 24,
  "major": "Computer Science",
  "gpa": 3.85
}
```

---

#### 2. List Students with Filters (`GET /students`)

Retrieve students enrolled in `Computer Science` with a GPA of at least `3.5`:

```bash
curl -X GET "http://127.0.0.1:8000/students?major=Computer%20Science&min_gpa=3.5"
```

**Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "name": "Pavan Majji",
    "email": "pavan.majji@example.com",
    "age": 24,
    "major": "Computer Science",
    "gpa": 3.85
  }
]
```

---

#### 3. Partial Update (`PATCH /students/{id}`)

Update only the student's GPA without passing the rest of the object:

```bash
curl -X PATCH "http://127.0.0.1:8000/students/1" \
     -H "Content-Type: application/json" \
     -d '{
       "gpa": 3.95
     }'
```

**Response (`200 OK`):**
```json
{
  "id": 1,
  "name": "Pavan Majji",
  "email": "pavan.majji@example.com",
  "age": 24,
  "major": "Computer Science",
  "gpa": 3.95
}
```

---

#### 4. Delete Student (`DELETE /students/{id}`)

```bash
curl -X DELETE "http://127.0.0.1:8000/students/1"
```

**Response (`204 No Content`):**
*(Empty response body)*

---

## 🚦 HTTP Status Codes Reference

- **`200 OK`**: Resource successfully retrieved or modified.
- **`201 Created`**: New student record successfully created.
- **`204 No Content`**: Student successfully deleted; body omitted.
- **`400 Bad Request`**: Duplicate email address or empty update payload.
- **`404 Not Found`**: The requested student `id` does not exist.
- **`422 Unprocessable Entity`**: Payload failed schema validation (e.g., invalid email, GPA > 4.0, age < 5).

---

## 📖 Interactive Documentation

- **Swagger UI:** Access `http://127.0.0.1:8000/docs` to test endpoints interactively directly from your browser.
- **ReDoc:** Access `http://127.0.0.1:8000/redoc` for schema specifications.

---

## 📜 License

This project is created for educational and practical assessment purposes.
