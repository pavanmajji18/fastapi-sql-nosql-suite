# ⚡ FastAPI: SQL (PostgreSQL) vs NoSQL (MongoDB) API Comparison (`05-sql-vs-mongodb-api`)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_2.0-D71F00?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Motor](https://img.shields.io/badge/Motor_Async-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://motor.readthedocs.io/)

A side-by-side comparative study and reference implementation of a **Task Management REST API** built with **FastAPI**, demonstrating the architectural, data-modeling, and operational differences between a relational SQL database (**PostgreSQL**) and a document-oriented NoSQL database (**MongoDB**).

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Repository Structure](#-repository-structure)
- [Comparative Feature Matrix](#-comparative-feature-matrix)
- [API Specification & Endpoints](#-api-specification--endpoints)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Running the PostgreSQL Version](#running-the-postgresql-version)
  - [Running the MongoDB Version](#running-the-mongodb-version)
- [Key Architectural Insights](#-key-architectural-insights)
- [Interactive Documentation](#-interactive-documentation)

---

## 📌 Overview

This directory features two complete, standalone implementations of the exact same Task Management API specification:

1. **[`postgres-version/`](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/05-sql-vs-mongodb-api/postgres-version)**: Uses **PostgreSQL** with **SQLAlchemy 2.0 (Async Engine)** and **asyncpg** driver.
2. **[`mongo-version/`](file:///d:/Euron/Work%20and%20Learn%20Super%2030/Python/Tasks/fastapi-sql-nosql/05-sql-vs-mongodb-api/mongo-version)**: Uses **MongoDB** with **Motor** (`AsyncIOMotorClient`) for async document operations.

Both implementations expose identical HTTP endpoints for managing **Projects** and **Tasks**, allowing developers to compare schema enforcement, primary key strategies (`UUIDv4` vs `BSON ObjectId`), query paradigms, and referential integrity mechanisms.

---

## 📁 Repository Structure

```text
05-sql-vs-mongodb-api/
│
├── postgres-version/          # PostgreSQL implementation
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Environment settings (Pydantic BaseSettings)
│   │   ├── database.py        # SQLAlchemy async engine & session maker
│   │   ├── models.py          # SQLAlchemy ORM models (Project, Task, TaskStatus)
│   │   ├── schemas.py         # Pydantic request & response schemas
│   │   └── main.py            # FastAPI app & endpoint handlers
│   ├── .env.example           # PostgreSQL environment template
│   └── requirements.txt       # Dependencies (FastAPI, SQLAlchemy, asyncpg)
│
└── mongo-version/             # MongoDB implementation
    ├── app/
    │   ├── __init__.py
    │   ├── config.py          # Environment settings (Pydantic BaseSettings)
    │   ├── database.py        # AsyncIOMotorClient connection pool
    │   ├── schemas.py         # Pydantic schemas (with BSON ObjectId alias)
    │   └── main.py            # FastAPI app & BSON ObjectId handlers
    ├── .env.example           # MongoDB environment template
    └── requirements.txt       # Dependencies (FastAPI, Motor, certifi)
```

---

## ⚡ Comparative Feature Matrix

| Feature | PostgreSQL Version | MongoDB Version |
| :--- | :--- | :--- |
| **Database Architecture** | Relational SQL | Document NoSQL |
| **Async Driver** | `asyncpg` | `motor` (`AsyncIOMotorClient`) |
| **ORM / Data Access Layer** | `SQLAlchemy 2.0` (Mapped Declarative Base) | Native MongoDB queries / PyMongo syntax |
| **Primary Keys** | `UUIDv4` (`uuid.uuid4()`) | 12-byte `BSON ObjectId` (`_id`) |
| **Foreign Key Relationships**| Database-enforced FK + `ondelete="CASCADE"` | Application-level manual reference validation (`project_id`) |
| **Enum Constraints** | Native PostgreSQL / SQLAlchemy Enum (`TODO`, `IN_PROGRESS`, `DONE`) | String values managed via Pydantic / application code |
| **Schema Initialization** | `Base.metadata.create_all` (Lifespan handler) | Dynamic collection creation on insert |
| **Query Mechanism** | SQLAlchemy `select(Model).where(...)` | Motor `db[collection].find(...)` |

---

## 🛠️ API Specification & Endpoints

Both versions share the same HTTP interface:

### 1. Projects API

| Method | Endpoint | Description | Payload / Query |
| :--- | :--- | :--- | :--- |
| `POST` | `/projects` | Create a new project | `{ "title": "str", "description": "str (optional)" }` |

### 2. Tasks API

| Method | Endpoint | Description | Payload / Query |
| :--- | :--- | :--- | :--- |
| `POST` | `/tasks` | Create a task linked to a project | `{ "title": "str", "description": "str", "project_id": "ID", "assignee_name": "str" }` |
| `GET` | `/tasks` | Filter and list tasks | Query: `project_id`, `status` (`TODO`, `IN_PROGRESS`, `DONE`) |
| `PATCH` | `/tasks/{task_id}/assign` | Assign task to a user | Payload: `{ "assignee_name": "str" }` |
| `PATCH` | `/tasks/{task_id}/status` | Update task status | Payload: `{ "status": "IN_PROGRESS" }` |
| `DELETE` | `/tasks/{task_id}` | Delete a task | Returns `204 No Content` |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed.
- A running **PostgreSQL** database instance (Local or [Neon DB](https://neon.tech)).
- A running **MongoDB** cluster (Local or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)).

---

### Running the PostgreSQL Version

1. **Navigate to the `postgres-version` directory:**
   ```bash
   cd postgres-version
   ```

2. **Create and activate a virtual environment:**
   - **Windows:** `python -m venv venv && .\venv\Scripts\activate`
   - **macOS / Linux:** `python3 -m venv venv && source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy `.env.example` to `.env` and supply your PostgreSQL connection URI:
   ```ini
   DATABASE_URL="postgresql+asyncpg://<username>:<password>@<host>/<dbname>?ssl=require"
   ```

5. **Start the server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

---

### Running the MongoDB Version

1. **Navigate to the `mongo-version` directory:**
   ```bash
   cd mongo-version
   ```

2. **Create and activate a virtual environment:**
   - **Windows:** `python -m venv venv && .\venv\Scripts\activate`
   - **macOS / Linux:** `python3 -m venv venv && source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy `.env.example` to `.env` and supply your MongoDB connection string:
   ```ini
   MONGODB_URL="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
   DATABASE_NAME="task_management"
   ```

5. **Start the server:**
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

---

## 🔍 Key Architectural Insights

### 1. ID Handling & Schema Mapping
- **PostgreSQL:** Primary keys use standard 128-bit `UUIDv4`. Native Pydantic UUID validation works seamlessly across request and response models.
- **MongoDB:** Native document keys use 12-byte BSON `ObjectId` strings. Motor returned documents require converting `_id` from `ObjectId` to string using helper functions (`fix_id`) and field aliasing (`Field(alias="_id")`) in Pydantic.

### 2. Referential Integrity
- **PostgreSQL:** Handled natively by the database engine using `ForeignKey("projects.id", ondelete="CASCADE")`. Inserting a task with a non-existent `project_id` fails at the database level.
- **MongoDB:** Documents in separate collections (`projects` and `tasks`) lack database-enforced relational integrity. Validation must be performed explicitly in application code (`db["projects"].find_one(...)`) before insertion.

---

## 📖 Interactive Documentation

Once the server is running, explore and test the endpoints via interactive Swagger UI:
- **PostgreSQL Version:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **MongoDB Version:** [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## 📜 License

This project is created for educational and practical assessment purposes.
