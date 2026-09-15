# GD Extreme Demon Ladder Generator

Web application for generating progression ladders between Geometry Dash Extreme
Demon levels. The project uses Django and Django REST Framework as its backend,
while the future user interface will be implemented with React and Vite.

The web application is the primary interface. The former Python CLI is kept
temporarily as a legacy reference and is not the target execution flow.

## Architecture

```text
React/Vite (future frontend)
        |
        | HTTP/JSON through /api
        v
Django + Django REST Framework
        |
        +-- Anonymous session history
        +-- CSRF protection
        +-- SQLite for local development
        +-- AREDL API client and TTL cache
        v
Domain services
        |
        +-- LadderBuilder
        +-- CandidateSelector
        +-- CandidateScoring
        +-- LevelService
        v
AREDL API
```

The generation logic remains independent from Django. This allows the same
domain code to be tested independently while Django handles HTTP, sessions,
validation and persistence.

## Requirements

For local backend development:

- Python 3.11 or newer.
- Git.
- Internet access for AREDL requests and Python dependencies.

For Docker development:

- Docker Desktop.
- WSL 2 enabled on Windows when using the Linux engine.
- Docker Compose.

The frontend toolchain is not included yet. It will be added later under a
separate `frontend/` directory.

## Installation for local development

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
Copy-Item .env.example .env
```

The current settings module reads environment variables from the process; it
does not automatically load `.env` files. For local development, enable debug
and configure the required variables in the current PowerShell session:

```powershell
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
$env:AREDL_BASE_URL = "https://api.aredl.net/v2/api"
$env:AREDL_REQUEST_TIMEOUT = "10"
$env:AREDL_CACHE_TTL = "300"
```

Run migrations and start Django:

```powershell
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

The backend will be available at `http://127.0.0.1:8000`.

### Local checks

```powershell
$env:DJANGO_DEBUG = "True"
python manage.py test
python -m unittest discover -s tests -v
python manage.py check
python manage.py makemigrations --check --dry-run
```

## Docker setup

Docker is the recommended way to run the backend with the same Gunicorn-based
process used by the production-oriented image.

Create the local environment file:

```powershell
Copy-Item .env.example .env
```

For a local Docker run, `DJANGO_DEBUG=True` is acceptable. Do not commit `.env`
or put real production secrets in it.

Build and start the backend:

```powershell
docker compose build backend
docker compose up -d
docker compose ps
```

The container:

1. Installs the pinned runtime and build dependencies.
2. Runs Django migrations.
3. Starts Gunicorn on port `8000`.
4. Runs as a non-root user.
5. Exposes a Docker health check through `/api/health/`.

Stop the stack:

```powershell
docker compose down
```

The SQLite database is stored in the `django-data` Docker volume.

Verify the container:

```powershell
curl.exe http://localhost:8000/api/health/
```

Expected response:

```json
{"status": "ok"}
```

## Environment variables

Use [.env.example](.env.example) as the starting point.

| Variable | Purpose | Local default |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Secret used to sign sessions, CSRF data and Django messages. | Generated temporarily when debug is enabled |
| `DJANGO_DEBUG` | Enables detailed development behavior. | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hostnames. | `127.0.0.1,localhost` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origins allowed to send trusted CSRF requests. | Empty |
| `DJANGO_SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS. | `False` |
| `DJANGO_HSTS_SECONDS` | HSTS duration in seconds. | `0` |
| `SESSION_COOKIE_SAMESITE` | SameSite policy for the session cookie. | `Lax` |
| `CSRF_COOKIE_SAMESITE` | SameSite policy for the CSRF cookie. | `Lax` |
| `AREDL_BASE_URL` | AREDL API base URL. | `https://api.aredl.net/v2/api` |
| `AREDL_REQUEST_TIMEOUT` | AREDL request timeout in seconds. | `10` |
| `AREDL_CACHE_TTL` | AREDL level cache duration in seconds. | `300` |
| `HISTORY_MAX_PER_SESSION` | Maximum anonymous history records per session. | `50` |
| `HISTORY_RETENTION_DAYS` | History retention period; `0` disables expiration. | `0` |

In production, set a long, random `DJANGO_SECRET_KEY`, set
`DJANGO_DEBUG=False`, configure real allowed hosts and trusted origins, and
serve the application through HTTPS.

## API contract

All API routes are prefixed with `/api/`.

### Health check

```http
GET /api/health/
```

Returns `200` when Django can reach its database:

```json
{"status": "ok"}
```

### Initialize CSRF

```http
GET /api/csrf/
```

This endpoint sets the `csrftoken` cookie. The frontend must call it before
making a mutating request.

### Generate a ladder

```http
POST /api/ladders/
Content-Type: application/json
X-CSRFToken: <value from csrftoken cookie>
```

Request:

```json
{
  "start": "Acheron",
  "target": "Tidal Wave",
  "steps": 20,
  "window": 5
}
```

`start` and `target` can be level names or numeric IDs. `steps` must be at
least `1`; `window` must be at least `0`.

Successful response: `201 Created`.

```json
{
  "id": 1,
  "start": "Acheron",
  "target": "Tidal Wave",
  "steps": 20,
  "window": 5,
  "result": [
    {
      "id": "aredl-id",
      "name": "Example Level",
      "position": 0,
      "level_id": 123,
      "gddl_tier": 35,
      "tags": ["Wave"],
      "song_id": 456,
      "publisher": ""
    }
  ],
  "warnings": [],
  "created_at": "2026-09-15T22:00:00Z"
}
```

Possible responses:

- `400 Bad Request`: invalid input.
- `404 Not Found`: start or target level was not found.
- `403 Forbidden`: missing or invalid CSRF token.
- `502 Bad Gateway`: AREDL failed or returned an invalid payload.

### Session history

```http
GET /api/ladders/history/?page=1&page_size=20
```

The response contains only records associated with the current anonymous
Django session:

```json
{
  "results": [],
  "count": 0,
  "next": null,
  "previous": null
}
```

The history is limited to 50 records per session by default and supports
configurable retention.

## Frontend integration

The planned local development setup uses separate ports:

```text
React/Vite: http://localhost:5173
Django API: http://localhost:8000
```

Vite should proxy `/api` to Django. This avoids unnecessary CORS complexity
during local development.

The frontend HTTP client must preserve cookies:

```javascript
await fetch("/api/csrf/", {
  credentials: "include"
});

await fetch("/api/ladders/", {
  method: "POST",
  credentials: "include",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": csrfToken
  },
  body: JSON.stringify(payload)
});
```

The frontend must not import Python modules or reproduce ladder-generation
logic. It should consume the API contract and handle loading, success,
validation, upstream errors and empty history states.

## Project structure

```text
config/                              Django project configuration
ladder/                              Django API application
  models.py                          Persistent ladder history model
  serializers.py                     Request and response validation
  services.py                        Django/domain integration
  views.py                           API endpoints
  urls.py                            API routes
gd_extreme_demon_ladder_generator/   Framework-independent domain and AREDL client
tests/                               Unit tests for the domain
Dockerfile                           Production-oriented backend image
docker-compose.yml                   Local Docker orchestration
manage.py                            Django command-line entry point
```

## CLI status

The old CLI entry point remains temporarily in
`gd_extreme_demon_ladder_generator/main.py` for reference and regression
purposes. It is not the intended public interface. New features should be
implemented through the Django API and consumed by the future web frontend.

## Production considerations

The current Docker setup is suitable for local validation and a simple
single-container deployment. Before a larger production deployment, consider:

- PostgreSQL instead of SQLite.
- Redis for shared cache across multiple workers or replicas.
- A reverse proxy terminating HTTPS.
- A production `DJANGO_SECRET_KEY`.
- Restricted `DJANGO_ALLOWED_HOSTS`.
- Explicit `DJANGO_CSRF_TRUSTED_ORIGINS`.
- Secure cookies and HSTS only when HTTPS is correctly configured.
- Centralized logs and monitoring.
- A scheduled cleanup strategy for expired history.

Authentication, user accounts, asynchronous generation, complete AREDL
synchronization and real-time updates are intentionally out of scope for the
initial version.
