# Eskelsen Systems — FastAPI Backend Reference Demo

**Independent, synthetic portfolio demonstration. Not a client system or production service.**

A small CRUD-oriented REST API showcasing FastAPI, Pydantic validation, SQLAlchemy, automated tests, OpenAPI documentation, and optional PostgreSQL via Docker Compose.

## Features
- Health endpoint (`GET /health`)
- Create, list, retrieve, delete demo inventory items
- Typed request validation and clear 404/422 responses
- SQLAlchemy persistence; PostgreSQL in Docker Compose or SQLite in local development
- Six automated API tests
- Auto-generated OpenAPI at `/docs`

## Quick start (local SQLite)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs.

## Docker + PostgreSQL
```bash
docker compose up --build
```
This is **development-only** configuration with example credentials. Do not expose or deploy it to production as-is.

## Run tests
```bash
pytest -q
```
Tests use an isolated in-memory SQLite database; PostgreSQL runtime and Docker Compose are supplied but **not integration-tested here**.

## Known non-production features
No authentication, authorization, user tenancy, migrations, rate limiting, secrets management, CI/CD, or production hardening. Tables are created at startup solely for demo convenience.

## Sample request
```bash
curl -X POST http://127.0.0.1:8000/items -H 'Content-Type: application/json' -d '{"name":"Demo Widget","category":"test","quantity":3}'
```

## Suggested Upwork portfolio summary
> A synthetic, independent FastAPI REST API demonstration with SQLAlchemy persistence, request validation, OpenAPI documentation, Docker Compose configuration, and automated endpoint tests. Built to showcase backend coding practices without exposing client systems.
