# GD-Extreme-Demon-Ladder-Generator
Python tool that automatically generates a levels progression list, also known as "Ladder", for Geometry Dash Extreme Demon levels.

## Backend local setup

Install the pinned dependencies and configure local settings:

```powershell
python -m pip install -e .
Copy-Item .env.example .env
$env:DJANGO_DEBUG = "True"
python manage.py migrate
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000`. The future Vite frontend should
proxy `/api` to this address and send session cookies with its requests.

### API endpoints

- `GET /api/health/` checks application and database availability.
- `GET /api/csrf/` initializes the CSRF cookie for the browser.
- `POST /api/ladders/` generates and persists a ladder.
- `GET /api/ladders/history/` returns the current session's paginated history.

For a mutating request, the browser must send both the Django session cookie and
the CSRF token in the `X-CSRFToken` header.

## Docker

Copy `.env.example` to `.env`, replace `DJANGO_SECRET_KEY`, and run:

```powershell
docker compose up --build
```

The container runs migrations before starting Gunicorn on port `8000`.
