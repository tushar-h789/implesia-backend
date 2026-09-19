# Implesia Backend

FastAPI backend for the [implesia.com](https://implesia.com) website.

**Current scope:** auth, leads, services, orders, pricing, portfolio, and articles CMS.

## Stack

| Concern | Choice |
|---|---|
| API | FastAPI, Pydantic v2, Uvicorn / Gunicorn |
| Database | PostgreSQL 16, SQLAlchemy 2.0 async, asyncpg, Alembic |
| Cache & rate limiting | Redis, slowapi |
| Auth | JWT access + refresh (PyJWT), bcrypt, role hierarchy |
| Email | aiosmtplib, logged to stdout when SMTP is unset |
| Spam control | Cloudflare Turnstile, honeypot field, per-IP rate limit |
| Logging | structlog (JSON in production, console in debug) |
| Quality | pytest, Ruff, mypy |

## Getting started

```bash
cp .env.example .env
# Generate a real key: python -c "import secrets; print(secrets.token_urlsafe(48))"

docker compose up -d postgres redis

uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -e ".[dev]"

alembic upgrade head
python -m scripts.create_superuser

uvicorn app.main:app --reload
```

The API is then on <http://localhost:8000> with interactive docs at `/docs`.

To exercise every endpoint from a desktop client, open the Bruno collection in [`bruno/`](bruno/README.md).

To run everything in containers instead, use `docker compose up --build`.

> Postgres is published on host port **5433** and Redis on **6380** so they do not clash
> with services already installed on the host. Inside the compose network they use their
> standard ports.

## Commands

```bash
pytest                       # test suite (runs on in-memory SQLite, no services needed)
ruff check . && ruff format . # lint and format
mypy app scripts             # type check
alembic revision --autogenerate -m "add articles"
alembic upgrade head
alembic check                # fail if models have drifted from migrations
python -m scripts.seed_services   # upsert the public service catalogue
python -m scripts.seed_pricing    # upsert /pricing page, models, packages
python -m scripts.seed_portfolio  # upsert /portfolio page and case studies
python -m scripts.seed_articles   # upsert /articles page and posts
```

## Layout

```
app/
  api/deps.py            shared dependencies: db session, current user, role guards
  api/v1/endpoints/      route handlers, one module per resource
  core/                  settings, security primitives, logging, error envelope
  db/                    declarative base, mixins, async session factory
  models/                SQLAlchemy models
  schemas/               Pydantic request and response models
  services/              business logic, kept out of the route handlers
alembic/versions/        migrations
scripts/                 operational one-offs
tests/                   pytest suite
```

## API

Public:

| Method | Path | Notes |
|---|---|---|
| `GET` | `/api/v1/services` | Published services for the website. |
| `GET` | `/api/v1/services/{slug}` | One published service. |
| `GET` | `/api/v1/pricing` | Full `/pricing` page: chrome, models, packages, FAQs. |
| `GET` | `/api/v1/pricing/models/{slug}` | One published engagement model. |
| `GET` | `/api/v1/pricing/packages/{slug}` | One published BDT package. |
| `GET` | `/api/v1/portfolio` | Full `/portfolio` page: chrome + published projects only. |
| `GET` | `/api/v1/portfolio/projects/{slug}` | One published case study. No `internal_notes`. |
| `GET` | `/api/v1/articles` | Full `/articles` page: chrome + featured + published posts. Optional `?topic=`. |
| `GET` | `/api/v1/articles/{slug}` | One published article. No `internal_notes`. |
| `POST` | `/api/v1/orders` | Buy / order a published service. Saved to the admin inbox. Emails only if free Gmail SMTP is set. |
| `POST` | `/api/v1/leads` | Contact form submission. Rate limited, honeypot + Turnstile checked. |
| `GET` | `/health/live` | Liveness probe. |
| `GET` | `/health/ready` | Readiness probe, verifies database connectivity. |

Authenticated:

| Method | Path | Minimum role |
|---|---|---|
| `POST` | `/api/v1/auth/login` | — |
| `POST` | `/api/v1/auth/refresh` | — |
| `GET` | `/api/v1/auth/me` | viewer |
| `POST` | `/api/v1/auth/change-password` | viewer |
| `GET` `POST` `PATCH` `DELETE` | `/api/v1/admin/services[/{id or slug}]` | editor |
| `GET` `PATCH` | `/api/v1/admin/pricing` | editor |
| `GET` `POST` `PATCH` `DELETE` | `/api/v1/admin/pricing/models[/{id or slug}]` | editor |
| `GET` `POST` `PATCH` `DELETE` | `/api/v1/admin/pricing/packages[/{id or slug}]` | editor |
| `GET` `PATCH` | `/api/v1/admin/portfolio` | editor |
| `GET` `POST` `PATCH` `DELETE` | `/api/v1/admin/portfolio/projects[/{id or slug}]` | editor |
| `GET` `PATCH` | `/api/v1/admin/articles` | editor |
| `GET` `POST` `PATCH` `DELETE` | `/api/v1/admin/articles/posts[/{id or slug}]` | editor |
| `GET` `PATCH` | `/api/v1/admin/orders[/{id}]` | editor |
| `GET` | `/api/v1/admin/orders/stats` | editor |
| `GET` `PATCH` | `/api/v1/admin/leads[/{id}]` | editor |
| `GET` | `/api/v1/admin/leads/stats` | editor |
| `GET` `POST` `PATCH` | `/api/v1/users[/{id}]` | superadmin |

Roles are hierarchical: `superadmin` > `editor` > `viewer`.

### Error format

Every error uses the same envelope, so the frontend needs one handler:

```json
{ "error": { "code": "validation_error", "message": "...", "details": null } }
```

### Duplicate submissions

Send an `Idempotency-Key` header with the contact form POST. A retry with the same key
returns the original lead instead of creating a second one.

## Notes for the next phase

- Lead notification emails currently run in a FastAPI `BackgroundTask`. Move these to
  Celery once the worker is introduced, so a restart cannot drop a queued email.
- Public content endpoints should send `Cache-Control` and `ETag` so Cloudflare can serve
  them from the edge.
