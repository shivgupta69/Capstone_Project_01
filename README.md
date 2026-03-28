# AI Study Planner

Production-ready Flask study planner with authentication, scheduling, and analytics.

## Quick Start (Local)

1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Run the app (one command):
```bash
./start.sh
```

Open: `http://localhost:5000`

## Environment Variables

Configured through `.env` (auto-loaded by `python-dotenv`):

- `SECRET_KEY`: Flask secret key
- `DATABASE_PATH`: SQLite path (default: `study.db`)
- `FLASK_DEBUG`: `1` for debug, `0` for production
- `SESSION_COOKIE_SECURE`: `1` in HTTPS production
- `HOST`: bind host (default `0.0.0.0`)
- `PORT`: bind port (default `5000`)
- `WEB_CONCURRENCY`: Gunicorn workers
- `GUNICORN_THREADS`: Gunicorn threads per worker
- `GUNICORN_TIMEOUT`: Gunicorn request timeout
- `LOG_LEVEL`: Gunicorn log level

## Production Run

Use Gunicorn directly:
```bash
gunicorn -c gunicorn.conf.py run:app
```

Or use the startup script:
```bash
./start.sh
```

## Render Deployment

This repo includes `render.yaml`.

If setting manually in Render:
- Build command: `pip install -r requirements.txt`
- Start command: `./start.sh`
- Required env vars: `SECRET_KEY` (generated), `SESSION_COOKIE_SECURE=1`

## Railway Deployment

This repo includes `railway.toml` and `Procfile`.

Railway start command:
```bash
./start.sh
```

Set env vars in Railway:
- `SECRET_KEY`
- `SESSION_COOKIE_SECURE=1`

## Docker (Optional)

Build:
```bash
docker build -t ai-study-planner .
```

Run:
```bash
docker run -p 5000:5000 --env-file .env ai-study-planner
```

## Test

```bash
pytest -q
```
