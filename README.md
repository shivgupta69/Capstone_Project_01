# AI Study Planner

AI Study Planner is a Flask web application for managing study tasks, generating a daily study plan, and tracking study progress through a simple analytics dashboard. The project is organized into separate `backend`, `frontend`, and `deployment` layers so it is easier to understand, run locally, and present on GitHub.

## Features

- Secure user registration and login
- Task creation, deletion, filtering, and status updates
- Study schedule generation based on current tasks
- Analytics dashboard for completed work and study hours
- Server-rendered UI plus JSON endpoints for future frontend expansion
- Docker, Gunicorn, and Nginx-ready deployment setup

## Tech Stack

- Python 3.11+
- Flask
- SQLite
- Jinja2
- Gunicorn
- Docker
- pytest

## Repository Structure

```text
project-root/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── config/
│   ├── instance/
│   ├── scripts/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── static/
│   └── templates/
├── deployment/
│   ├── nginx/
│   ├── scripts/
│   ├── Dockerfile
│   ├── Procfile
│   ├── docker-compose.yml
│   ├── gunicorn.conf.py
│   ├── railway.toml
│   └── render.yaml
├── .gitignore
└── README.md
```

## Folder Guide

- `backend/app/routes/`: Flask blueprints and HTTP handlers
- `backend/app/services/`: business logic and application workflows
- `backend/app/repositories/`: database access layer
- `backend/app/models/`: lightweight data models
- `backend/app/utils/`: helpers for auth, DB, and shared utilities
- `backend/config/`: environment-aware app configuration
- `backend/scripts/`: operational scripts such as database initialization
- `backend/tests/`: automated tests
- `frontend/templates/`: server-rendered HTML templates
- `frontend/static/`: CSS, JS, and future images/assets
- `deployment/`: Docker, Gunicorn, Nginx, and platform deployment files

## Prerequisites

Make sure these are installed before running the project:

- Python 3.11 or newer
- `pip`
- `venv`
- Docker and Docker Compose, if you want containerized setup

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
python backend/scripts/init_db.py
python backend/run.py
```

Open `http://localhost:5000` in your browser.

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ai-study-planner
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure environment variables

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` if you want to change defaults like the port, debug mode, or database path.

### 5. Initialize the database

```bash
python backend/scripts/init_db.py
```

This creates the SQLite database and required tables inside `backend/instance/`.

### 6. Run the application

Option A: run the Flask app directly

```bash
python backend/run.py
```

Option B: run with the deployment startup script

```bash
bash deployment/scripts/start_backend.sh
```

The app will be available at:

```text
http://localhost:5000
```

## Environment Variables

The backend reads variables from `backend/.env`.

| Variable | Description | Default |
| --- | --- | --- |
| `SECRET_KEY` | Flask secret key for sessions and auth tokens | `dev-secret-key-change-in-production` fallback |
| `DATABASE_PATH` | SQLite database path relative to `backend/` unless absolute | `instance/study.db` |
| `FLASK_DEBUG` | Enable Flask debug mode with `1` | `0` |
| `SESSION_COOKIE_SECURE` | Use secure cookies in HTTPS environments | `0` |
| `HOST` | Host for the development server | `0.0.0.0` |
| `PORT` | Application port | `5000` |
| `WEB_CONCURRENCY` | Gunicorn worker count | `2` in example file |
| `GUNICORN_THREADS` | Gunicorn threads per worker | `2` in example file |
| `GUNICORN_TIMEOUT` | Gunicorn timeout in seconds | `120` |
| `LOG_LEVEL` | Gunicorn log level | `info` |

## Running Tests

Run the backend test suite with:

```bash
pytest backend/tests -q
```

Current verified result:

```text
40 passed
```

## Docker Setup

### Build the app image

```bash
docker build -f deployment/Dockerfile -t ai-study-planner .
```

### Run the app container

```bash
docker run --env-file backend/.env -p 5000:5000 ai-study-planner
```

### Run with Docker Compose and Nginx

```bash
docker compose -f deployment/docker-compose.yml up --build
```

Available endpoints after Compose startup:

- Flask app: `http://localhost:5000`
- Nginx reverse proxy: `http://localhost:8080`

## Deployment

The repository already includes deployment-ready files:

- `deployment/Dockerfile`
- `deployment/docker-compose.yml`
- `deployment/gunicorn.conf.py`
- `deployment/nginx/default.conf`
- `deployment/render.yaml`
- `deployment/railway.toml`
- `deployment/Procfile`

Manual production-style startup:

```bash
bash deployment/scripts/start_backend.sh
```

Direct Gunicorn startup:

```bash
python -m gunicorn -c deployment/gunicorn.conf.py backend.run:app
```

## Application Routes

### Auth

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/register` | Registration page |
| `POST` | `/register` | Register a new user |
| `GET` | `/login` | Login page |
| `POST` | `/login` | Authenticate a user |
| `GET` / `POST` | `/logout` | Logout current user |

### Tasks

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Dashboard |
| `POST` | `/add` | Add a task from the UI |
| `POST` | `/api/tasks` | Add a task via JSON |
| `GET` / `POST` | `/delete/<id>` | Delete a task from the UI |
| `DELETE` | `/api/tasks/<id>` | Delete a task via API |
| `POST` | `/task/<id>/status` | Update task status from the UI |
| `PUT` | `/api/tasks/<id>/status` | Update task status via API |
| `GET` | `/api/dashboard-fragments` | Load dashboard partials |

### Schedule and Analytics

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/schedule` | View generated study schedule |
| `GET` | `/analytics` | View analytics dashboard |

## How It Works

1. Users register and log in through the Flask auth routes.
2. Tasks are stored in SQLite and loaded through the repository layer.
3. Services handle validation, scheduling, and analytics calculations.
4. Flask renders the interface using templates from `frontend/templates/`.

## Screenshots

Add screenshots here before publishing publicly on GitHub:

- Dashboard screenshot
- Schedule screenshot
- Analytics screenshot

## Troubleshooting

### Port already in use

Run with a different port:

```bash
PORT=5001 python backend/run.py
```

or

```bash
PORT=5001 bash deployment/scripts/start_backend.sh
```

### Database issues

If the local DB gets corrupted or you want a clean start, remove the SQLite file in `backend/instance/` and run:

```bash
python backend/scripts/init_db.py
```

You can also use:

```bash
python -m backend.scripts.init_db
```

### Missing dependencies

Make sure your virtual environment is active, then reinstall:

```bash
pip install -r backend/requirements.txt
```

## Future Improvements

### Convert the frontend to React

1. Keep Flask as the backend service layer.
2. Build a React app inside `frontend/`.
3. Move current JSON endpoints into versioned API routes like `/api/v1/...`.
4. Replace server-rendered dashboard sections gradually.

### Turn the backend into a full REST API

1. Standardize API response shapes.
2. Add versioned blueprints such as `/api/v1/tasks`.
3. Introduce request validation and serializers.
4. Move authentication toward API-friendly flows for SPA/mobile clients.

### Production hardening

- Replace SQLite with PostgreSQL
- Add database migrations
- Add structured logging
- Put Nginx behind HTTPS
- Add CI for tests and linting

## License

Add your preferred license here before publishing the repository.
