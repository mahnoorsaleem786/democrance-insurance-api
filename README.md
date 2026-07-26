# Democrance Insurance API

A RESTful backend application developed using **Django**, **Django REST Framework**, and **PostgreSQL** as part of the Democrance Backend Coding Assessment.

The application allows users to:

- Create customers
- Generate insurance quotes
- Activate insurance policies
- Track policy state history
- Search customers and policies
- Secure endpoints using JWT Authentication
- Manage data through the Django Admin panel
- Validate functionality with automated unit tests using Pytest

---

# Features

## Customer Management

- Create a new customer
- Validate customer input
- Store customer information in PostgreSQL
- Search customers by:
  - First name
  - Last name
  - Date of birth

---

## Insurance Quote Management

- Generate insurance quotes
- Calculate premium based on customer age
- Associate policies with customers
- Convert quotes into active policies

---

## Policy Lifecycle

Implemented policy states:

```
NEW
  │
  ▼
QUOTED
  │
  ▼
ACTIVE
```

---

## Policy History

Every policy state transition is stored in a separate history table for audit purposes.

Example:

| Previous State | New State |
|---------------|-----------|
| NULL | QUOTED |
| QUOTED | ACTIVE |

---

## Search

Customer Search

```
GET /api/v1/customers/?name=Ben
```

```
GET /api/v1/customers/?dob=1991-06-25
```

Policy Search

```
GET /api/v1/policies/?type=personal-accident
```

---

# Technology Stack

## Backend

- Python 3
- Django
- Django REST Framework

## Database

- PostgreSQL

## Authentication

- JWT (Simple JWT)

## Testing

- Pytest
- Pytest-Django
- Coverage

## Development Tools

- Git
- Postman
- Black
- Flake8
- isort

---

# Project Structure

```
democrance-insurance-api/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── customers/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│
├── policies/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── history_service.py
│   ├── policy_servic.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│
├── common/
│   ├── __init__.py
│   ├── logger.py
│   └── (Reserved for reusable shared components)
│
├── manage.py
├── requirements.txt
├── pytest.ini
├── README.md
└── .env.example
```

---

# Architecture

The project follows a layered architecture.

```
HTTP Request
      │
      ▼
DRF View
      │
      ▼
Serializer
      │
      ▼
Service Layer
      │
      ▼
Django ORM
      │
      ▼
PostgreSQL
```

### Responsibilities

**Views**
- Receive HTTP requests
- Return HTTP responses
- Coordinate application flow

**Serializers**
- Validate request data
- Transform JSON into Python objects
- Serialize responses

**Services**
- Handle business logic
- Calculate premiums
- Manage policy state transitions

**Models**
- Define database schema
- Manage relationships
- Persist data

---

# Database Design

## Customer

| Field | Type |
|-------|------|
| id | Integer |
| first_name | CharField |
| last_name | CharField |
| dob | DateField |
| created_at | DateTime |
| updated_at | DateTime |

---

## Policy

| Field | Type |
|-------|------|
| id | Integer |
| customer | ForeignKey |
| policy_type | CharField |
| premium | Decimal |
| cover | Decimal |
| state | CharField |
| created_at | DateTime |
| updated_at | DateTime |

---

## Policy History

| Field | Type |
|-------|------|
| id | Integer |
| policy | ForeignKey |
| previous_state | CharField |
| new_state | CharField |
| changed_at | DateTime |

---

### Entity Relationship

```
Customer
    │
    │ One-to-Many
    ▼
Policy
    │
    │ One-to-Many
    ▼
PolicyHistory
```

---

# Prerequisites

Before running the project, ensure you have:

- Python 3.10+
- PostgreSQL
- Git
- pip
- Virtual Environment (venv)

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd democrance-insurance-api
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a file named `.env` in the project root.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=democrance_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

An `.env.example` file is included for reference.

---

# PostgreSQL Database Setup

Create a PostgreSQL database.

Example:

```sql
CREATE DATABASE democrance_db;
```

Update the `.env` file with your PostgreSQL credentials.

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Create Django Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account.

---

# Run the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```

The Django Admin panel will be available at:

```
http://127.0.0.1:8000/admin/
```

---


# Authentication

The application uses **JWT (JSON Web Token)** authentication for protected endpoints.

Public endpoints:

- Create Customer
- Generate JWT Token

Protected endpoints:

- Create Insurance Quote
- Accept Quote
- View Policy History
- Search Customers
- Search Policies

---

## Generate Access Token

Before accessing protected endpoints, generate an access token.

### Endpoint

```http
POST /api/token/
```

### Request

```json
{
    "username": "admin",
    "password": "your_password"
}
```

### Successful Response

```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

---

## Using JWT Token

For every protected endpoint include the following HTTP Header:

```
Authorization: Bearer <access_token>
```

Example:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR...
```

---

# API Endpoints

---

## 1. Create Customer

Creates a new customer.

### Endpoint

```http
POST /api/v1/create_customer/
```

### Authentication

Not Required

### Request

```json
{
    "first_name": "Ben",
    "last_name": "Stokes",
    "dob": "1991-06-25"
}
```

### Success Response

```json
{
    "message": "Customer created successfully.",
    "data": {
        "id": 3,
        "first_name": "Ben",
        "last_name": "Stokes",
        "dob": "1991-06-25"
    }
}
```

---

## 2. Generate Insurance Quote

Creates a policy quote for an existing customer.

### Endpoint

```http
POST /api/v1/quote/
```

### Authentication

JWT Required

### Request

```json
{
    "customer_id": 1,
    "policy_type": "personal-accident"
}
```

### Success Response

```json
{
    "message": "Quote generated successfully.",
    "data": {
        "policy_id": 1,
        "customer_id": 1,
        "policy_type": "personal-accident",
        "premium": "200.00",
        "cover": "200000.00",
        "state": "QUOTED"
    }
}
```

---

## 3. Accept Quote

Converts a quoted policy into an active policy.

### Endpoint

```http
POST /api/v1/quote/accept/
```

### Authentication

JWT Required

### Request

```json
{
    "policy_id": 1
}
```

### Success Response

```json
{
    "message": "Policy activated successfully.",
    "data": {
        "policy_id": 1,
        "customer_id": 1,
        "policy_type": "personal-accident",
        "premium": "200.00",
        "cover": "200000.00",
        "state": "QUOTED"
    }
}
```

---

## 4. Customer Search

Search by customer name.

```http
GET /api/v1/customers/?name=Ben
```

Search by date of birth.

```http
GET /api/v1/customers/?dob=1991-06-25
```

Authentication Required

---

## 5. Policy Search

Search by policy type.

```http
GET /api/v1/policies/?type=personal-accident
```

Authentication Required

---

## 6. Policy History

Returns all policy state transitions.

### Endpoint

```http
GET /api/v1/policies/1/history/
```

Authentication Required

### Example Response

```json
[
    {
        "previous_state": "NEW",
        "new_state": "QUOTED",
        "changed_at": "2026-07-26T12:30:15Z"
    },
    {
        "previous_state": "QUOTED",
        "new_state": "ACTIVE",
        "changed_at": "2026-07-26T12:35:41Z"
    }
]
```

---

# Acceptance Testing Guide

The project has been designed so it can be tested easily using either:

- Postman
- cURL
- Any REST Client

The recommended testing sequence is:

## Step 1

Clone the repository.

```bash
git clone <repository-url>
```

---

## Step 2

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Step 3

Create PostgreSQL database.

Example:

```sql
CREATE DATABASE democrance_db;
```

---

## Step 4

Create `.env` using `.env.example`.

---

## Step 5

Run migrations.

```bash
python manage.py migrate
```

---

## Step 6

Create Django Superuser.

```bash
python manage.py createsuperuser
```

---

## Step 7

Run the server.

```bash
python manage.py runserver
```

---

## Step 8

Import the Postman Collection.

```
Democrance API.postman_collection.json
```

---

## Step 9

Generate JWT Token.

```
POST /api/token/
```

---

## Step 10

Create Customer.

```
POST /api/v1/create_customer/
```

---

## Step 11

Create Insurance Quote.

```
POST /api/v1/quote/
```

---

## Step 12

Accept Quote.

```
POST /api/v1/quote/accept/
```

---

## Step 13

Verify Policy History.

```
GET /api/v1/policies/1/history/
```

---

## Step 14

Verify Customer and Policy relationships through Django Admin.

```
http://127.0.0.1:8000/admin/
```

---

# Postman Collection

A Postman Collection is included with this repository.

Import:

```
Democrance API.postman_collection.json
```

The collection contains requests in the correct execution order:

1. Generate JWT Token
2. Create Customer
3. Create Quote
4. Accept Quote
5. Search Customers
6. Search Policies
7. View Policy History

This allows the project to be tested in a reproducible manner.

---

# Running Tests

Run all tests.

```bash
pytest
```

Run tests with coverage.

```bash
pytest --cov
```

Run a specific test file.

```bash
pytest customers/tests/
```

or

```bash
pytest policies/tests/
```

---

# Test Coverage

The project includes unit tests covering:

- Customer creation
- Customer validation
- Quote generation
- Premium calculation
- Invalid customer scenarios
- Quote acceptance
- Policy state transitions
- Policy history
- Customer search
- Policy search


---

# Future Enhancements

Possible improvements include:

## Infrastructure

- Docker support
- Docker Compose
- Kubernetes deployment
- CI/CD pipeline


## Performance

- Redis caching
- Database indexing
- Read replicas
- Query optimisation


## Security

- Role-Based Access Control (RBAC)
- API rate limiting
- Multi-factor authentication
- Audit logging
- Security headers


## Business Features

- Payment gateway integration
- Email notifications
- SMS notifications
- Customer self-service portal
- Claims management
- Policy renewal workflow


## Monitoring

- Centralised logging
- OpenTelemetry
- Prometheus
- Grafana
- Sentry

---