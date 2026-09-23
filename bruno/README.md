# Implesia Backend — Bruno

Open this folder as a Bruno collection. Same layout as Flyger LMS `docs/`:

- `bruno.json` + `collection.bru`
- `environments/` — Local, Stage, Production
- `Public/` — no JWT
- `Private/` — collection script attaches `Authorization: Bearer {{ACCESS_TOKEN}}`

## Open in Bruno

1. Bruno → **Open Collection**
2. Select `/home/tushar/Desktop/office/practice/implesia/implesia-backend/bruno`
3. Environment = **Local** (or **Production** for live public GETs)

API must be running: `uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`

Local login: `admin@implesia.com` / `LocalAdmin#2026!`

## Private CRUD (do this every session)

Access tokens last **30 minutes**. Without a fresh token every private request is `401`.

1. `Public / Health / Ready` — confirm the API is up
2. `Public / Auth / Login` — writes `ACCESS_TOKEN` into the Local env
3. Run anything under `Private /`

The collection pre-request script adds the Bearer header for `/api/v1/admin/*`, `/api/v1/users`, `/auth/me`, and `/auth/change-password`. You do not set the header by hand.

### Safe Read / Update (seeded catalogue)

These UUIDs already exist after seed. Use them for Get / List / Patch. Slug stays on the row for frontend URLs; the API looks up by id.

| Folder | Get / Update uses |
|---|---|
| Services | `SERVICE_ID` (`web-platforms`). Run **Public / Services / List Services** first — it copies the UUID from `SERVICE_SLUG`. A slug in the path is `422`. |
| Pricing models | `MODEL_ID` (`discovery-sprint`) |
| Pricing packages | `PACKAGE_ID` (`product-landing-page`) |
| Portfolio | `PROJECT_ID` (`gulf-franchise`) |
| Articles (public) | `ARTICLE_ID` (`zero-trust-modern-saas`) |
| Articles (admin) | `POST_ID` (same UUID as `ARTICLE_ID`) |
| About | singleton page — no id var |
| Team | `MEMBER_ID` (`tushar-hossen`) |
| Contact | singleton page — form still posts to `POST /api/v1/leads` |
| Orders | `ORDER_ID` from Submit Order |
| Leads | `LEAD_ID` from a public lead submit |

### Create / Delete (demo rows only)

Create writes a `DEMO_*_ID`. Delete uses that id, never the live catalogue.

| Create | Then delete |
|---|---|
| Services → Create Service (`bruno-crud-service`) | Services → Get Demo → Update → Delete Service |
| Pricing → Create Model (`bruno-demo-model`) | Pricing → Delete Model |
| Pricing → Create Package (`bruno-demo-package`) | Pricing → Delete Package |
| Portfolio → Create Project (`bruno-demo-case`) | Portfolio → Delete Project |
| Articles → Create Post (`bruno-demo-insight`) | Articles → Delete Post |
| Team → Create Member (`bruno-demo-member`) | Team → Delete Member |

Do not run Delete Service after an order exists for that service (API returns `409`).

Do not run `Private / Auth / Change Password` unless you mean to change the admin password.

## Error codes

- `401` / `Not authenticated` — run Login again
- `403` / `forbidden` — account is viewer, needs editor or superadmin
- `http_error` / `Not Found` — route missing (restart uvicorn) or empty path var
- `not_found` — that id is not in the database
- `422` — path is not a UUID (slug is not accepted)
