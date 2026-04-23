# ☕ Aura Cafe API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-262627?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

**A modern, fast backend API for the Aura Cafe ordering system**

[Features](#-features) • [Quick Start](#-quick-start) • [API Documentation](#-api-endpoints) • [Database](#-database-setup)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Database Setup](#-database-setup)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Development](#-development)
- [Deployment](#-deployment)

---

## 🌟 Overview

Aura Cafe API is a robust and scalable backend service that powers the Aura Cafe ordering system. Built with **FastAPI**, it provides a high-performance REST API for managing menu items, user authentication, shopping carts, and order processing.

The API supports both **dine-in** and **cash-on-delivery (COD)** order types, making it versatile for various cafe operations.

---

## ✨ Features

### 🔐 Authentication & Security
- **User Registration** - Secure signup with password hashing (bcrypt)
- **User Login** - Authentication with token-based sessions
- **Password Security** - Industry-standard bcrypt hashing with 72-character limit

### 🍽️ Menu Management
- **Full CRUD Operations** - Create, Read, Update, Delete menu items
- **Rich Menu Data** - Support for name, price, description, and images
- **Real-time Updates** - Instant menu synchronization

### 🛒 Shopping Cart
- **Add to Cart** - Easily add menu items with quantities
- **View Cart** - Real-time cart status and item management

### 📦 Order Processing
- **Place Orders** - Seamless checkout with order details
- **Order Types** - Support for dine-in (seat number) and COD (delivery address)
- **Order Tracking** - Status management and order history

### 👨‍💼 Admin Panel
- **Admin Authentication** - Separate admin login system
- **Dashboard Access** - Manage cafe operations efficiently

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern async web framework |
| **SQLAlchemy** | SQL toolkit & ORM |
| **Pydantic** | Data validation & settings management |
| **Uvicorn** | ASGI server |
| **Passlib + bcrypt** | Password hashing & verification |
| **Supabase** | PostgreSQL database (cloud) |
| **psycopg2-binary** | PostgreSQL adapter |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Supabase account (for cloud database) or local PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "BACKEND CAFE"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@host:5432/database_name
   USE_SUPABASE_CLIENT=false
   ```

5. **Run the server**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

6. **Access the API**
   - **Base URL:** `http://127.0.0.1:8000`
   - **Interactive Docs:** `http://127.0.0.1:8000/api/docs`
   - **ReDoc:** `http://127.0.0.1:8000/api/redoc`

---

## 📚 API Endpoints

### 🔍 Health Check
```
GET /
```
Returns service health status.

---

### 🔐 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/signup` | Register a new user |
| `POST` | `/login` | User login |

**Example: User Signup**
```json
POST /signup
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "password": "securepassword123"
}
```

**Example: User Login**
```json
POST /login
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

---

### 🍽️ Menu

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/menu/` | Get all menu items |
| `POST` | `/menu/` | Add a new menu item |
| `PUT` | `/menu/{item_id}` | Update a menu item |
| `DELETE` | `/menu/{item_id}` | Delete a menu item |

**Example: Add Menu Item**
```json
POST /menu/
{
  "name": "Cappuccino",
  "price": 4.99,
  "description": "Classic Italian coffee with steamed milk",
  "image": "https://example.com/cappuccino.jpg"
}
```

---

### 🛒 Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/cart/` | View shopping cart |
| `POST` | `/cart/` | Add item to cart |

**Example: Add to Cart**
```json
POST /cart/
{
  "item_id": 1,
  "quantity": 2
}
```

---

### 📦 Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/orders/` | Get all orders |
| `POST` | `/orders/` | Place a new order |

**Example: Place Order (Dine-in)**
```json
POST /orders/
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "+1234567890",
  "order_type": "dine-in",
  "seat_number": "A12",
  "items": [
    {"item_id": 1, "quantity": 2},
    {"item_id": 3, "quantity": 1}
  ]
}
```

**Example: Place Order (Delivery)**
```json
POST /orders/
{
  "customer_name": "Jane Smith",
  "customer_email": "jane@example.com",
  "customer_phone": "+0987654321",
  "order_type": "cod",
  "address": "123 Coffee Street, Brew City",
  "items": [
    {"item_id": 2, "quantity": 1}
  ]
}
```

---

### 👨‍💼 Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/admin/login` | Admin login |

**Default Admin Credentials:**
- **Email:** `admin@aura.com`
- **Password:** `adminaura123`

> ⚠️ **Important:** Change these credentials in `routers/admin.py` before production deployment!

---

## 🗄️ Database Setup

### Option 1: Supabase (Recommended)

1. Create a new project at [supabase.com](https://supabase.com)
2. Get your database connection string from **Project Settings → Database**
3. Update your `.env` file:
   ```env
   DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```

### Option 2: Local PostgreSQL

1. Install PostgreSQL
2. Create a database:
   ```sql
   CREATE DATABASE aura_cafe;
   ```
3. Update your `.env` file:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/aura_cafe
   ```

### Option 3: SQLite (Development Only)

The application automatically falls back to SQLite if no database URL is provided:
```env
# Leave DATABASE_URL empty or unset
```

---

## 📁 Project Structure

```
BACKEND CAFE/
├── main.py              # FastAPI application entry point
├── database.py          # Database configuration & connection
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for validation
├── crud.py              # Database operations (Create, Read, Update, Delete)
├── supabase_client.py   # Supabase REST API client
├── requirement.txt      # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore           # Git ignore rules
│
└── routers/             # API route modules
    ├── __init__.py
    ├── auth.py          # Authentication endpoints
    ├── menu.py          # Menu management endpoints
    ├── cart.py          # Shopping cart endpoints
    ├── order.py         # Order processing endpoints
    └── admin.py         # Admin panel endpoints
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes* |
| `USE_SUPABASE_CLIENT` | Use Supabase REST client (`true`/`false`) | No |

*Required unless using SQLite fallback

### CORS Configuration

The API is configured to allow requests from all origins (development mode). For production, update the CORS settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 👩‍💻 Development

### Running Tests

```bash
python test_admin_features.py
```

### Code Style

This project follows Python PEP 8 style guidelines. Consider using:
- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting

### Hot Reload

During development, run with auto-reload:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

---

## 🚀 Deployment

### Production Server

Use a production ASGI server like **Gunicorn** with Uvicorn workers:

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t aura-cafe-api .
docker run -p 8000:8000 --env-file .env aura-cafe-api
```

### Recommended Platforms

- **Railway.app** - Easy deployment with Supabase integration
- **Render.com** - Free tier available
- **Heroku** - Popular PaaS option
- **AWS/GCP/Azure** - For enterprise deployments

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is part of the Aura Cafe system. All rights reserved.

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact the development team

---

<div align="center">

**Built with ❤️ using FastAPI**

[⬆ Back to Top](#-aura-cafe-api)

</div>