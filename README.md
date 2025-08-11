# Task 4 - ORM with FastAPI

##  Overview
This project demonstrates how to build a simple **ORM-based CRUD API** using **FastAPI**, **SQLAlchemy**, and **PostgreSQL** with **Alembic** for database migrations.

The application allows defining models, running migrations, and exposing FastAPI endpoints for interacting with the database.

---

##  Tech Stack
- **FastAPI** - Web framework for building APIs
- **SQLAlchemy ORM** - Object Relational Mapping for PostgreSQL
- **Alembic** - Database migrations
- **Pydantic** - Data validation and request/response schemas
- **PostgreSQL** - Relational database

##  Project Structure

| Path / File                | Description |
|----------------------------|-------------|
| **alembic/**               | Alembic migration scripts folder |
| ├── `versions/`            | Contains migration files |
| ├── `env.py`               | Alembic environment configuration |
| ├── `script.py.mako`       | Alembic migration script template |
| `.env`                     | Environment variables (DB credentials, etc.) |
| `.gitignore`               | Git ignore file |
| `alembic.ini`              | Alembic configuration file |
| `api.py`                   | FastAPI route definitions |
| `crud.py`                  | CRUD operations for database models |
| `db.py`                    | Database connection setup |
| `insert_data.py`           | Script to insert initial/sample data |
| `main.py`                  | FastAPI application entry point |
| `models.py`                | SQLAlchemy ORM model definitions |
| `schemas.py`               | Pydantic schemas for request/response validation |
| `README.md`                | Project documentation |


