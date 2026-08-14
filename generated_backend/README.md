# Acme Orders API - Generated FastAPI Backend

Auto-generated backend application built from OpenAPI specification v1.0.0.

## 🚀 Quick Start (Local)

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run Server**:
```bash
uvicorn app.main:app --reload --port 8000
```

3. **Access Interactive API Docs**:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🐳 Quick Start (Docker Compose)

Run the full stack with PostgreSQL database:
```bash
docker compose up --build
```

---

## 📁 Clean Architecture Project Structure

```
backend/
├── app/
│   ├── api/          # FastAPI Route Handlers
│   ├── core/         # Settings & Security Config
│   ├── db/           # SQLAlchemy Session & Engine
│   ├── models/       # SQLAlchemy 2.0 ORM Models
│   ├── schemas/      # Pydantic v2 Request/Response Schemas
│   └── services/     # Service Layer Business Logic
├── tests/            # Pytest Integration Test Suite
├── Dockerfile        # Production Docker container setup
├── docker-compose.yml# Multi-container Compose config
└── requirements.txt
```

---

## 🛠️ Developer Customization Points

Custom business logic markers are present inside `app/services/*.py`:

```python
##################################################
# Developer Customization Starts Here
# TODO: Replace generated logic with custom rules
##################################################
```