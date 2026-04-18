README.md

# Workout Tracker API – Flask + JWT

## Overview

A secure REST API for managing users and workouts built with Flask and JWT authentication.

## Features

- JWT-based authentication
- SQLAlchemy ORM with relationships
- Marshmallow validation and serialization
- Pytest test suite
- Pipenv dependency management

## Installation

```bash
cd backend
pipenv install
pipenv shell
flask db upgrade
python seed.py
Run
python app.py

Server: http://127.0.0.1:5555

### Endpoints
Auth
POST /signup
POST /login
GET /me
POST /logout

Workouts
GET /api/workouts?page=1&per_page=10
POST /api/workouts
PATCH /api/workouts/<id>
DELETE /api/workouts/<id>


### Testing
pytest -v


Environment Variables
DATABASE_URL=
JWT_SECRET_KEY=
FLASK_ENV=

---

## Project Structure


backend/
│── Pipfile
│── Pipfile.lock
│── app.py
│── config.py
│── extensions.py
│── seed.py
│── migrations/
│
├── server/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── workout.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   └── workout_routes.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   └── workout_schema.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_auth_routes.py
│       ├── test_models.py
│       ├── test_schemas.py
│       └── test_workout_routes.py
│
└── README.md
```
