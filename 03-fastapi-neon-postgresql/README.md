# 🐘 FastAPI + Neon Serverless PostgreSQL API (`03-fastapi-neon-postgresql`)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Neon DB](https://img.shields.io/badge/Neon_PostgreSQL-00E599?style=for-the-badge&logo=postgresql&logoColor=black)](https://neon.tech/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)

A production-grade RESTful API built with **FastAPI**, **SQLAlchemy** (raw SQL execution via `text()`), and **Neon Serverless PostgreSQL**. This project demonstrates multi-table relational persistence, raw SQL parametrized queries, transactional integrity, foreign key enrollments, and analytical SQL aggregations.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema & ER Diagram](#-database-schema--er-diagram)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [Database Provisioning](#database-provisioning)
  - [Running the Server](#running-the-server)
- [API Specification & Endpoints](#-api-specification--endpoints)
- [Sample Requests & Responses](#-sample-requests--responses)
- [SQL Analytics Spotlight](#-sql-analytics-spotlight)
- [Interactive Documentation](#-interactive-documentation)

---

## 📌 Overview

This service manages a relational domain model for **Students**, **Courses**, and **Enrollments**. Unlike high-level ORM patterns, this project highlights parameterized raw SQL queries using SQLAlchemy's `text()` interface combined with FastAPI's dependency injection (`Depends(get_db)`) to achieve maximum query execution speed and full SQL control over serverless PostgreSQL connections.

> [!NOTE]
> Neon PostgreSQL provides serverless branching, auto-scaling, and connection pooling out-of-the-box, making it ideal for cloud microservices.

---

## ✨ Key Features

- **Direct Raw SQL Execution:** Safe parameterized execution using `db.execute(text(...))` to prevent SQL injection.
- **Relational Integrity:** Foreign Key constraints linking `student` and `courses` through an associative `enrollment` table.
- **Transactional Safety:** Automatic rollbacks (`db.rollback()`) on execution errors and explicit explicit transactional commits (`db.commit()`).
- **Partial Entity Updates:** Dynamic `PATCH` queries constructed at runtime using `.model_dump()` field maps.
- **Relational Analytics:** Aggregated revenue reporting (`/courses/revenue`) combining `JOIN`, `GROUP BY`, and scalar price multiplications.
- **Interactive Documentation:** Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## 🛠 Architecture & Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance Python web framework |
| **Database Engine** | [Neon Serverless PostgreSQL](https://neon.tech) | Cloud-native serverless PostgreSQL instance |
| **SQL Toolkit** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | Connection management & raw SQL execution via `text()` |
| **Driver** | `psycopg2-binary` / `pg8000` | PostgreSQL database adapter |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) | Strict payload schema enforcement |

---

## 📁 Project Structure

```text
03-fastapi-neon-postgresql/
│
├── app/
│   ├── __init__.py
│   ├── database.py       # SQLAlchemy engine & session dependency (get_db)
│   ├── main.py           # FastAPI application & SQL endpoint definitions
│   └── schemas.py        # Pydantic validation models (Student, Course, Enrollment)
│
├── .env.example          # Database connection string template
├── .gitignore
├── schema.sql            # DDL script for database tables & FK constraints
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🗄️ Database Schema & ER Diagram

```
 ┌───────────────────────┐            ┌─────────────────────────┐
 │        student        │            │         courses         │
 ├───────────────────────┤            ├─────────────────────────┤
 │ id (PK, SERIAL)       │            │ id (PK, SERIAL)         │
 │ name (VARCHAR)        │            │ title (VARCHAR)         │
 │ email (VARCHAR, UQ)   │            │ instructor (VARCHAR)    │
 │ age (INTEGER)         │            │ price (NUMERIC)         │
 │ city (VARCHAR)        │            │ duration_hours (INT)    │
 │ created_at (TIMESTAMP)│            │ created_at (TIMESTAMP)  │
 └───────────┬───────────┘            └────────────┬────────────┘
             │ 1                                   │ 1
             │                                     │
             │ *                                   │ *
 ┌───────────┴─────────────────────────────────────┴────────────┐
 │                          enrollment                          │
 ├──────────────────────────────────────────────────────────────┤
 │ id (PK, SERIAL)                                              │
 │ student_id (FK -> student.id ON DELETE CASCADE)              │
 │ course_id (FK -> courses.id ON DELETE CASCADE)               │
 │ status (VARCHAR: active / completed / dropped)               │
 │ enrolled_at (TIMESTAMP)                                      │
 └──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed.
- A **Neon PostgreSQL** database account ([Sign up free at neon.tech](https://neon.tech)).

---

### Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd 03-fastapi-neon-postgresql
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

4. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and paste your Neon PostgreSQL connection string:
   ```bash
   cp .env.example .env
   ```
   *Example `.env`:*
   ```ini
   DATABASE_URL=postgresql://<user>:<password>@<neon-hostname>/<dbname>?sslmode=require
   ```

---

### Database Provisioning

Run the table creation DDL script `schema.sql` inside your Neon Console SQL Editor or via `psql`:

```sql
CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT CHECK (age > 0),
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    instructor VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) CHECK (price >= 0),
    duration_hours INT CHECK (duration_hours > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS enrollment (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES student(id) ON DELETE CASCADE,
    course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'active',
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Running the Server

Launch the ASGI server with auto-reload:

```bash
uvicorn app.main:app --reload --port 8000
```

Access point URLs:
- **Base URL:** `http://127.0.0.1:8000`
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## 📡 API Specification & Endpoints

### 1. Student Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `POST` | `/students` | Register a new student | `201 Created` |
| `GET` | `/students` | Fetch all registered students | `200 OK` |
| `GET` | `/students/{student_id}` | Fetch a student by primary key ID | `200 OK` |
| `PATCH` | `/students/{student_id}` | Partially update student attributes | `200 OK` |
| `DELETE` | `/students/{student_id}` | Delete student and cascade delete enrollments | `200 OK` |

### 2. Course Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `POST` | `/courses` | Create a new course entry | `201 Created` |
| `GET` | `/courses` | List all available catalog courses | `200 OK` |
| `PATCH` | `/courses/{course_id}` | Partially update course details | `200 OK` |
| `DELETE` | `/courses/{course_id}` | Delete course entry | `200 OK` |

### 3. Enrollment & Analytics Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `POST` | `/enrollments` | Enroll a student in a specific course | `201 Created` |
| `GET` | `/enrollments` | Retrieve enrollments with JOINed student & course data | `200 OK` |
| `PATCH` | `/enrollments/{enrollment_id}` | Update enrollment status (`active`, `completed`, `dropped`) | `200 OK` |
| `DELETE` | `/enrollments/{enrollment_id}` | Remove enrollment record | `200 OK` |
| `GET` | `/courses/revenue` | Aggregated revenue analytics by course | `200 OK` |

---

## 💡 Sample Requests & Responses

### 1. Create a Student (`POST /students`)

```bash
curl -X POST "http://127.0.0.1:8000/students" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Pavan Majji",
       "email": "pavan.majji@example.com",
       "age": 24,
       "city": "Hyderabad"
     }'
```

**Response (`201 Created`):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Pavan Majji",
    "email": "pavan.majji@example.com",
    "age": 24,
    "city": "Hyderabad",
    "created_at": "2026-09-24T10:00:00"
  }
}
```

---

### 2. Create a Course (`POST /courses`)

```bash
curl -X POST "http://127.0.0.1:8000/courses" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "FastAPI & PostgreSQL Masterclass",
       "instructor": "Dr. Sarah Jenkins",
       "price": 299.99,
       "duration_hours": 40
     }'
```

---

### 3. Enroll Student (`POST /enrollments`)

```bash
curl -X POST "http://127.0.0.1:8000/enrollments" \
     -H "Content-Type: application/json" \
     -d '{
       "student_id": 1,
       "course_id": 1,
       "status": "active"
     }'
```

**Response (`201 Created`):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "student_id": 1,
    "course_id": 1,
    "status": "active",
    "enrolled_at": "2026-09-24T10:15:00"
  }
}
```

---

## 📊 SQL Analytics Spotlight

The `/courses/revenue` endpoint executes an aggregated SQL query calculating student enrollments and calculated revenue per course:

```sql
SELECT 
    c.id AS course_id,
    c.title,
    c.price,
    COUNT(e.id) AS total_students,
    (c.price * COUNT(e.id)) AS total_revenue
FROM courses c
JOIN enrollment e ON c.id = e.course_id
GROUP BY c.id, c.title, c.price
ORDER BY total_revenue DESC;
```

---

## 📖 Interactive Documentation

- **Swagger UI:** Access `http://127.0.0.1:8000/docs` for testing API endpoints interactively.
- **ReDoc:** Access `http://127.0.0.1:8000/redoc` for schema specifications.

---

## 📜 License

This project is created for educational and practical assessment purposes.