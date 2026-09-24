# 🎟️ MongoDB Support Ticket API (`06-mongodb-support-ticket-api`)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Motor](https://img.shields.io/badge/Motor_Async-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://motor.readthedocs.io/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic_v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

A high-performance, asynchronous RESTful API for managing customer support tickets built with **FastAPI**, **Motor** (Async MongoDB Driver), and **Pydantic v2**.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Data Model & Document Architecture](#-data-model--document-architecture)
- [Why MongoDB vs Relational Databases?](#-why-mongodb-vs-relational-databases)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Environment Variables](#-environment-variables)
- [Getting Started](#-getting-started)
- [Interactive Documentation](#-interactive-documentation)

---

## 📌 Overview

This API provides end-to-end lifecycle management for customer support tickets. Built with an event-driven document schema architecture leveraging MongoDB's flexible document model, it embeds customer profiles and threaded activity comments into a single ticket document.

---

## ✨ Key Features

- **Async Architecture:** Powered by FastAPI and `Motor` (`AsyncIOMotorClient`) for non-blocking database I/O.
- **Embedded Document Model:** Eliminates multi-table SQL `JOIN` bottlenecks by storing customer information and threaded comments directly inside ticket documents.
- **Atomic Operations:** Atomic `$push` operations for appending real-time comment threads without lock contention.
- **Optimized MongoDB Indexing:**
  - Compound index on `(status, priority)` for filtered dashboard queries.
  - Index on `customer.email` for user lookup operations.
  - MongoDB `$text` index across `title`, `description`, and `tags` for native keyword searches.
- **Flexible Filtering & Pagination:** Filter tickets by status, priority, category, or perform full-text search with skip/limit pagination.
- **Robust Validation:** Type safety and validation via Pydantic v2 models and custom BSON ObjectId validators.

---

## 📐 Data Model & Document Architecture

Instead of splitting related entities into isolated relational tables (e.g., separate tables for `customers`, `tickets`, `comments`, and a junction table for `ticket_tags`), this project leverages MongoDB's document model to embed customer profiles, activity threads, and tags inside a single ticket document:

```json
{
  "_id": { "$oid": "664c1f4e724a896d8b3c10a1" },
  "customer": {
    "name": "Pavan Kumar",
    "email": "pavan.kumar@example.com",
    "phone": "+91-9876543210"
  },
  "title": "Payment Gateway Timeout on Checkout",
  "description": "UPI transactions are timing out after receiving authorization token from bank gateway.",
  "category": "Billing",
  "priority": "high",
  "status": "in_progress",
  "tags": ["payment", "gateway", "upi", "timeout"],
  "comments": [
    {
      "author": "Santosh Kumar",
      "message": "Acknowledged issue. Checking microservice error rate in logs.",
      "created_at": "2026-09-19T09:30:00Z"
    },
    {
      "author": "Rakesh Kumar",
      "message": "Restarted stale connection pool on billing worker nodes.",
      "created_at": "2026-09-19T09:45:00Z"
    }
  ],
  "created_date": "2026-09-19T09:00:00Z",
  "updated_date": "2026-09-19T09:45:00Z"
}
```

---

## 💡 Why MongoDB vs Relational Databases?

1. **Atomic Reads & Zero Multi-Table JOIN Overheads:**
   In relational databases, rendering a single support ticket view requires JOIN operations across 3 or 4 tables (`tickets`, `ticket_comments`, `users`, `tags`). In MongoDB, the entire ticket lifecycle and conversation thread are fetched via a single read operation (`find_one({"_id": ...})`), drastically reducing latency on high-throughput support dashboards.
2. **Native Atomicity via Array Operators (`$push`):**
   Adding updates to a ticket's activity thread uses atomic operators like `$push`, avoiding external transaction coordination while keeping data consistent.
3. **Schema Flexibility for Dynamic Ticket Metadata:**
   Support tickets frequently require dynamic attributes depending on the incident or department. MongoDB's flexible schema easily accommodates polymorphic metadata without requiring schema migrations (`ALTER TABLE`).
4. **Integrated Full-Text Search Across Incident Logs:**
   Compound and full-text indexes (`$text`) across title, description, and tags allow fast incident searches out-of-the-box.

---

## 📁 Project Structure

```text
06-mongodb-support-ticket-api/
│
├── app/
│   ├── __init__.py
│   ├── config.py         # App settings & Pydantic BaseSettings
│   ├── database.py       # Motor client connection lifecycle & index creation
│   ├── main.py           # FastAPI application entry point & lifespan handler
│   ├── models.py         # Pydantic models & Enums (PriorityEnum, StatusEnum)
│   └── routes.py         # API Endpoints (CRUD, Status Update, Comment Push)
│
├── .env.example          # Environment variables template
├── .gitignore
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🛠️ API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Application health check endpoint |
| `POST` | `/api/tickets/` | Create a new support ticket |
| `GET` | `/api/tickets/` | List tickets with filters (`priority`, `status`, `category`, `search`, `skip`, `limit`) |
| `GET` | `/api/tickets/{ticket_id}` | Retrieve full ticket document by BSON ObjectId |
| `PUT` | `/api/tickets/{ticket_id}` | Update ticket details |
| `PATCH` | `/api/tickets/{ticket_id}/status` | Update status (`open`, `in_progress`, `resolved`, `closed`) |
| `POST` | `/api/tickets/{ticket_id}/comments` | Append a comment thread item using atomic `$push` |
| `DELETE` | `/api/tickets/{ticket_id}` | Delete a ticket document |

---

## ⚙️ Environment Variables

Configuration is loaded dynamically from `.env` using `pydantic-settings`.

| Variable | Default | Description |
| :--- | :--- | :--- |
| `APP_NAME` | `Support Ticket API` | Name of the FastAPI application |
| `APP_ENV` | `development` | Deployment environment mode |
| `PORT` | `8000` | Application port |
| `MONGODB_URL` | *Required* | MongoDB connection URI string |
| `DATABASE_NAME` | `support_ticket_db` | Target MongoDB database name |

---

## 🚀 Getting Started

### 1. Activate Virtual Environment & Install Dependencies

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

Install requirements:
```bash
pip install -r requirements.txt
```

---

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Update `.env` with your active MongoDB cluster or local MongoDB URI:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@cluster-address.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=support_ticket_db
```

---

### 3. Launch Server

```bash
uvicorn app.main:app --reload --port 8000
```

---

## 📖 Interactive Documentation

- **Swagger UI:** Access `http://127.0.0.1:8000/docs` to test endpoints interactively.
- **ReDoc:** Access `http://127.0.0.1:8000/redoc` for schema specifications.

---

## 📜 License

This project is created for educational and practical assessment purposes.