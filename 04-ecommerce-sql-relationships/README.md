# 🛒 E-Commerce REST API (`04-ecommerce-sql-relationships`)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Neon DB](https://img.shields.io/badge/Neon_PostgreSQL-00E599?style=for-the-badge&logo=postgresql&logoColor=black)](https://neon.tech/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)

A high-performance backend microservice built using **FastAPI**, **SQLAlchemy ORM**, and **Neon Serverless PostgreSQL**. This service manages relational models for `users`, `products`, `orders`, and `order_items` with transaction-safe calculations, row-level locks, dynamic price formulas, and atomic inventory adjustments.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Database Schema & ER Diagram](#-database-schema--er-diagram)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [Applying Database Schema](#applying-database-schema)
  - [Running the Server](#running-the-server)
- [API Endpoints](#-api-endpoints)
- [Highlighted SQL Query & Analytics](#-highlighted-sql-query--analytics)
- [Interactive Documentation](#-interactive-documentation)

---

## ✨ Features

- **Relational Data Modeling:** Strict Foreign Key constraints, cascading deletes, and generated price calculations across `users`, `products`, `orders`, and `order_items`.
- **Atomic Stock Management:** Row-level locks (`with_for_update()`) executed during order placement to prevent race conditions and overselling stock under concurrent load.
- **Dynamic Price & Order Total Calculations:**
  - $\text{Item Total} = \text{Quantity} \times \text{Unit Price}$
  - $\text{Order Total} = \sum (\text{Item Totals})$
- **Order Cancellation & Stock Restoration:** Automatically restores reserved product stock quantities back into catalog inventory when an order is cancelled.
- **Relational SQL Analytics:** Demonstrates aggregated customer spending reports combining `JOIN`, `WHERE`, `GROUP BY`, and `SUM`.

---

## 🛠 Architecture & Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance async Python web framework |
| **Database Engine** | [Neon Serverless PostgreSQL](https://neon.tech) | Cloud-native serverless relational PostgreSQL engine |
| **ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | Async relational data mapping and transaction control |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) | Strict API request and response payload validation |

---

## 🗄️ Database Schema & ER Diagram

### Entity-Relationship Breakdown
- **Users to Orders (`1:M`):** One user can place multiple orders (`ON DELETE CASCADE`).
- **Orders to Order Items (`1:M`):** One order contains one or more line-items (`ON DELETE CASCADE`).
- **Products to Order Items (`1:M`):** Products are referenced across multiple order line-items (`ON DELETE RESTRICT` protects catalog integrity).

```text
   ┌─────────────┐             ┌─────────────┐
   │    users    │ 1         * │   orders    │
   ├─────────────┤─────────────├─────────────┤
   │ id (PK)     │             │ id (PK)     │
   │ name        │             │ user_id(FK) │
   │ email (UQ)  │             │ total_amount│
   │ created_at  │             │ status      │
   └─────────────┘             │ created_at  │
                               └──────┬──────┘
                                      │ 1
                                      │
                                      │ *
   ┌─────────────┐             ┌──────┴──────┐
   │  products   │ 1         * │ order_items │
   ├─────────────┤─────────────├─────────────┤
   │ id (PK)     │             │ id (PK)     │
   │ name        │             │ order_id(FK)│
   │ description │             │ prod_id (FK)│
   │ price       │             │ quantity    │
   │ stock_qty   │             │ unit_price  │
   │ created_at  │             │ item_total  │
   └─────────────┘             └─────────────┘
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
   cd 04-ecommerce-sql-relationships
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
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://<user>:<password>@<neon-hostname>/<dbname>?sslmode=require
   ```

---

### Applying Database Schema

Execute `schema.sql` and `sample_data.sql` inside your Neon Console SQL Editor or via `psql`:

```bash
psql "your_neon_connection_string" -f schema.sql
psql "your_neon_connection_string" -f sample_data.sql
```

---

### Running the Server

```bash
uvicorn app.main:app --reload --port 8000
```

Access point URLs:
- **Base URL:** `http://127.0.0.1:8000`
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/users` | Register a new user |
| `POST` | `/products` | Add a new product to the catalog |
| `GET` | `/products` | List all available catalog items |
| `PATCH` | `/products/{product_id}/inventory` | Manually update available stock quantity |
| `POST` | `/orders` | Place a new order with stock validation and row locks |
| `GET` | `/users/{user_id}/orders` | Retrieve all orders placed by a specific user |
| `POST` | `/orders/{order_id}/cancel` | Cancel an order and restore product stock inventory |
| `GET` | `/analytics/spending-by-user` | Aggregated user spending and order volume report |

---

## 🔍 Highlighted SQL Query & Analytics

Implemented in `/analytics/spending-by-user`, this query aggregates user spending across non-cancelled orders:

```sql
SELECT 
    u.id AS user_id, 
    u.name AS user_name, 
    COUNT(o.id) AS total_orders, 
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status != 'CANCELLED'
GROUP BY u.id, u.name
ORDER BY total_spent DESC;
```

---

## 📖 Interactive Documentation

- **Swagger UI:** Access `http://127.0.0.1:8000/docs` to test endpoints interactively.
- **ReDoc:** Access `http://127.0.0.1:8000/redoc` for schema specifications.

---

## 📜 License

This project is created for educational and practical assessment purposes.