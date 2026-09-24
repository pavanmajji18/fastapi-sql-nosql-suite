# 🚀 FastAPI SQL & NoSQL Master Collection

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic_v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

A comprehensive collection of production-grade RESTful APIs built with **FastAPI**, **Pydantic v2**, **PostgreSQL** (Neon Serverless, SQLAlchemy), and **MongoDB** (Motor, BSON).

This repository showcases modern Python backend architectural patterns—ranging from basic in-memory CRUD operations and strict schema validation to complex relational database transactions, row-level locking, asynchronous document data modeling, API security, client rate-limiting, and side-by-side SQL vs. NoSQL comparative benchmarks.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Repository Structure](#-repository-structure)
- [Module Breakdown](#-module-breakdown)
  - [01. Student Management REST API](#01-student-management-rest-api)
  - [02. Course Management API (Auth & Rate Limiting)](#02-course-management-api-auth--rate-limiting)
  - [03. FastAPI + Neon PostgreSQL API](#03-fastapi--neon-postgresql-api)
  - [04. E-Commerce SQL Relationships API](#04-e-commerce-sql-relationships-api)
  - [05. SQL vs MongoDB Task API Comparison](#05-sql-vs-mongodb-task-api-comparison)
  - [06. MongoDB Support Ticket API](#06-mongodb-support-ticket-api)
- [Tech Stack Overview](#-tech-stack-overview)
- [SQL vs NoSQL Architectural Matrix](#-sql-vs-nosql-architectural-matrix)
- [Getting Started](#-getting-started)
- [Interactive API Documentation](#-interactive-api-documentation)
- [License](#-license)

---

## 📌 Overview

This workspace serves as an all-in-one hands-on architectural reference for building scalable Python microservices. Key architectural highlights include:

- **FastAPI & Async I/O:** High-performance asynchronous request handling powered by ASGI (`uvicorn`).
- **Pydantic v2 Validation:** Type safety, custom field validators, data serialization, and environment configuration management (`pydantic-settings`).
- **Relational SQL Databases:** Entity relationships (`1:M`), cascading deletes, raw & ORM query building (`JOIN`, `GROUP BY`, aggregate functions), explicit transaction isolation, and row-level locks (`with_for_update`).
- **Document NoSQL Databases:** Embedded schemas, array update operators (`$push`), compound & `$text` search indexes, and custom `BSON ObjectId` validation.
- **API Security & Middleware:** Header-based API Key authentication and client IP rate-limiting middleware.

---

## 📁 Repository Structure

```text
fastapi-sql-nosql/
│
├── 01-student-management-api/         # Basic FastAPI CRUD with Pydantic v2 validation
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── 02-course-api-pydantic/            # Advanced Pydantic, API Key Auth & IP Rate Limiting
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── security.py
│   ├── requirements.txt
│   └── README.md
│
├── 03-fastapi-neon-postgresql/        # Serverless Neon PostgreSQL + Raw SQL via SQLAlchemy
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── schema.sql
│   ├── requirements.txt
│   └── README.md
│
├── 04-ecommerce-sql-relationships/    # SQL 1:M Relationships, Inventory Locks & Analytics
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── schema.sql
│   ├── sample_data.sql
│   ├── requirements.txt
│   └── README.md
│
├── 05-sql-vs-mongodb-api/             # Side-by-Side Architectural Comparison (PostgreSQL vs MongoDB)
│   ├── postgres-version/              # PostgreSQL + asyncpg + UUIDs
│   │   └── app/
│   ├── mongo-version/                 # MongoDB + Motor + ObjectIds
│   │   └── app/
│   └── README.md
│
└── 06-mongodb-support-ticket-api/    # Async MongoDB Support System (Embedded Docs & $text search)
    ├── app/
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   └── routes.py
    ├── requirements.txt
    └── README.md
```

---

## 🛠 Module Breakdown

### [01. Student Management REST API](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/01-student-management-api)
- **Directory:** [`01-student-management-api/`](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/01-student-management-api)
- **Key Concepts:** Fundamentals of REST APIs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), status code handling (`201 Created`, `204 No Content`, `422 Unprocessable Entity`), query parameter filtering (`major`, `min_gpa`), and in-memory persistence.

### [02. Course Management API (Auth & Rate Limiting)](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/02-course-api-pydantic)
- **Directory:** [`02-course-api-pydantic/`](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/02-course-api-pydantic)
- **Key Concepts:** Multi-file modular app layout, native API Key header security (`X-API-Key`), rolling window client IP rate-limiting (`429 Too Many Requests`), and partial model updates via `model_dump(exclude_unset=True)`.

### [03. FastAPI + Neon PostgreSQL API](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/03-fastapi-neon-postgresql)
- **Directory:** [`03-fastapi-neon-postgresql/`](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/03-fastapi-neon-postgresql)
- **Key Concepts:** Connecting FastAPI to cloud-hosted serverless PostgreSQL ([Neon DB](https://neon.tech)), raw SQL parameterized execution using SQLAlchemy `text()`, schema migration execution, and environment configuration with `.env`.

### [04. E-Commerce SQL Relationships API](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/04-ecommerce-sql-relationships)
- **Directory:** [`04-ecommerce-sql-relationships/`](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/04-ecommerce-sql-relationships)
- **Key Concepts:** Multi-table database design (`users`, `products`, `orders`, `order_items`), `1:M` relationships with Foreign Keys, row-level stock locks (`with_for_update`) to prevent race conditions, automated inventory restoration on cancellation, and SQL analytical queries with `JOIN`, `GROUP BY`, and `SUM`.

### [05. SQL vs MongoDB Task API Comparison](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/05-sql-vs-mongodb-api)
- **Directory:** [`05-sql-vs-mongodb-api/`](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/05-sql-vs-mongodb-api)
- **Key Concepts:** Dual implementation of an identical Task Management specification comparing **PostgreSQL** (`SQLAlchemy 2.0` + `asyncpg` + `UUIDv4`) vs **MongoDB** (`Motor` + `BSON ObjectId`). Analyzes key differences in referential integrity, primary keys, and query paradigms.

### [06. MongoDB Support Ticket API](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/06-mongodb-support-ticket-api)
- **Directory:** [`06-mongodb-support-ticket-api/`](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/06-mongodb-support-ticket-api)
- **Key Concepts:** Asynchronous document data modeling using `Motor`. Stores customer info and comment threads as embedded documents inside tickets, performs atomic `$push` updates, creates compound indexes, and executes MongoDB `$text` search queries.

---

## 💻 Tech Stack Overview

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10+** | Primary programming language |
| **FastAPI** | High-performance async web framework |
| **Pydantic v2** | Type validation, serialization, and settings management |
| **Uvicorn** | ASGI server for high-throughput asynchronous request processing |
| **PostgreSQL / Neon DB** | Relational serverless cloud database engine |
| **SQLAlchemy 2.0** | Async SQL toolkit and Object-Relational Mapper (ORM) |
| **asyncpg** | High-speed, async PostgreSQL database driver |
| **MongoDB / Atlas** | Scalable document-oriented NoSQL database |
| **Motor** | Async Python driver for MongoDB |

---

## ⚡ SQL vs NoSQL Architectural Matrix

| Architectural Feature | PostgreSQL (Relational SQL) | MongoDB (Document NoSQL) |
| :--- | :--- | :--- |
| **Data Model** | Normalized tables with columns & rows | Flexible JSON-like BSON documents |
| **Primary Keys** | `UUIDv4` or Auto-incrementing Integers | 12-byte `BSON ObjectId` (`_id`) |
| **Referential Integrity** | Database-enforced Foreign Keys & CASCADE rules | Application-level schema validation |
| **Data Nesting** | Normalized across linked tables (`1:M`, `M:N`) | Embedded sub-documents & arrays |
| **Query Mechanism** | SQL `SELECT`, `JOIN`, `GROUP BY`, `HAVING` | MongoDB `find()`, `$push`, Aggregation Pipelines |
| **Best Used For** | Financial transactions, inventory control, strict ACID requirements | Dynamic schemas, log feeds, threaded messaging, rapid iteration |

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.10+** installed on your system.
2. **PostgreSQL** instance (Local or [Neon Cloud](https://neon.tech)).
3. **MongoDB** cluster (Local or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)).

---

### General Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fastapi-sql-nosql
   ```

2. **Navigate to any specific project directory:**
   ```bash
   cd 01-student-management-api
   # or
   cd 04-ecommerce-sql-relationships
   ```

3. **Create and activate a virtual environment:**
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

4. **Install project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables (for projects 03 – 06):**
   Copy `.env.example` to `.env` and configure your database credentials:
   ```bash
   cp .env.example .env
   ```

6. **Run the Uvicorn server:**
   ```bash
   # Standard entrypoint (e.g., project 01)
   uvicorn main:app --reload

   # Or for modular app packages (e.g., projects 02, 03, 04, 05, 06)
   uvicorn app.main:app --reload --port 8000
   ```

---

## 📖 Interactive API Documentation

Every project automatically generates interactive OpenAPI documentation:

- **Swagger UI:** Access at `http://127.0.0.1:8000/docs` to test endpoints interactively directly from the browser.
- **ReDoc:** Access at `http://127.0.0.1:8000/redoc` for schema specifications.

---

## 📜 License

This repository is maintained for educational and practical assessment purposes.
