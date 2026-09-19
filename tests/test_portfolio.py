from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserRole
from app.schemas.user import UserCreate
from app.services import user_service
from tests.conftest import TEST_PASSWORD

PAGE_PATCH = {
    "hero_heading": "Production software that delivers.",
    "cta_heading": "Ready to build something remarkable?",
}

PROJECT = {
    "name": "Gulf Franchise",
    "slug": "gulf-franchise",
    "tagline": "Franchise & Franchisor Shop Buy/Rent",
    "category": "marketplace",
    "year": 2025,
    "status": "Completed",
    "summary": "Full-stack franchise discovery platform with listings and lead workflows.",
    "tech_stack": ["Next.js", "Tailwind CSS", "Laravel"],
    "live_url": "https://gulffranchisehub.com",
    "live_label": "gulffranchisehub.com",
    "outcomes": [{"title": "Live", "description": "Production deployment"}],
    "is_featured": True,
    "is_published": True,
    "sort_order": 10,
    "internal_notes": "Do not show this note on the public website.",
}


async def test_public_hides_drafts_and_internal_notes(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    await client.patch("/api/v1/admin/portfolio", json=PAGE_PATCH, headers=auth_headers)
    created = await client.post(
        "/api/v1/admin/portfolio/projects", json=PROJECT, headers=auth_headers
    )
    assert created.status_code == 201, created.text
    assert created.json()["internal_notes"].startswith("Do not show")

    await client.post(
        "/api/v1/admin/portfolio/projects",
        json={**PROJECT, "name": "Draft Case", "slug": "draft-case", "is_published": False},
        headers=auth_headers,
    )

    public = await client.get("/api/v1/portfolio")
    assert public.status_code == 200, public.text
    body = public.json()
    slugs = [item["slug"] for item in body["projects"]]
    assert slugs == ["gulf-franchise"]
    assert body["featured"]["slug"] == "gulf-franchise"
    assert "internal_notes" not in body["featured"]
    assert "internal_notes" not in body["projects"][0]

    card = await client.get("/api/v1/portfolio/projects/gulf-franchise")
    assert card.status_code == 200
    assert "internal_notes" not in card.json()
    assert (await client.get("/api/v1/portfolio/projects/draft-case")).status_code == 404


async def test_public_rejects_javascript_live_url(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    response = await client.post(
        "/api/v1/admin/portfolio/projects",
        json={**PROJECT, "slug": "bad-url", "live_url": "javascript:alert(1)"},
        headers=auth_headers,
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


async def test_admin_crud_and_auth_boundaries(
    client: AsyncClient, auth_headers: dict[str, str], db_session: AsyncSession
) -> None:
    created = await client.post(
        "/api/v1/admin/portfolio/projects", json=PROJECT, headers=auth_headers
    )
    assert created.status_code == 201
    admin_get = await client.get(
        "/api/v1/admin/portfolio/projects/gulf-franchise", headers=auth_headers
    )
    assert admin_get.json()["internal_notes"].startswith("Do not show")

    patched = await client.patch(
        "/api/v1/admin/portfolio/projects/gulf-franchise",
        json={"status": "Completed", "year": 2025},
        headers=auth_headers,
    )
    assert patched.status_code == 200

    assert (await client.get("/api/v1/admin/portfolio")).status_code == 401
    assert (await client.get("/api/v1/admin/portfolio/projects")).status_code == 401

    await user_service.create_user(
        db_session,
        UserCreate(
            email="viewer@implesia.com",
            full_name="Viewer",
            password=TEST_PASSWORD,
            role=UserRole.VIEWER,
        ),
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "viewer@implesia.com", "password": TEST_PASSWORD},
    )
    assert login.status_code == 200
    viewer = {"Authorization": f"Bearer {login.json()['access_token']}"}
    forbidden = await client.get("/api/v1/admin/portfolio/projects", headers=viewer)
    assert forbidden.status_code == 403
    assert forbidden.json()["error"]["code"] == "forbidden"

    deleted = await client.delete(
        "/api/v1/admin/portfolio/projects/gulf-franchise", headers=auth_headers
    )
    assert deleted.status_code == 200


async def test_duplicate_project_slug_conflicts(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    assert (
        await client.post("/api/v1/admin/portfolio/projects", json=PROJECT, headers=auth_headers)
    ).status_code == 201
    again = await client.post(
        "/api/v1/admin/portfolio/projects", json=PROJECT, headers=auth_headers
    )
    assert again.status_code == 409
