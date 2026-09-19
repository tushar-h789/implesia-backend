from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserRole
from app.schemas.user import UserCreate
from app.services import user_service
from tests.conftest import TEST_PASSWORD

PAGE_PATCH = {
    "hero_heading": "Technical insights for engineering leaders.",
    "cta_heading": "Need a technical conversation?",
}

ARTICLE = {
    "title": "Why Zero-Trust is No Longer Optional for Modern SaaS",
    "slug": "zero-trust-modern-saas",
    "excerpt": "The architectural shift required to protect data in decentralized work.",
    "body": (
        "For decades, enterprise security was built around a simple idea: "
        "everything inside the corporate network could be trusted."
    ),
    "topic": "security",
    "topic_label": "Security",
    "tags": ["zero-trust", "saas"],
    "author_name": "Implesia Engineering",
    "author_role": "Security Architecture",
    "reading_minutes": 18,
    "published_at": "2025-11-12T00:00:00Z",
    "is_featured": True,
    "is_published": True,
    "sort_order": 10,
    "internal_notes": "Do not show this note on the public website.",
}


async def test_public_hides_drafts_and_internal_notes(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    await client.patch("/api/v1/admin/articles", json=PAGE_PATCH, headers=auth_headers)
    created = await client.post(
        "/api/v1/admin/articles/posts", json=ARTICLE, headers=auth_headers
    )
    assert created.status_code == 201, created.text
    assert created.json()["internal_notes"].startswith("Do not show")

    await client.post(
        "/api/v1/admin/articles/posts",
        json={
            **ARTICLE,
            "title": "Draft Insight",
            "slug": "draft-insight",
            "is_published": False,
            "is_featured": False,
        },
        headers=auth_headers,
    )

    public = await client.get("/api/v1/articles")
    assert public.status_code == 200, public.text
    body = public.json()
    slugs = [item["slug"] for item in body["articles"]]
    assert slugs == ["zero-trust-modern-saas"]
    assert body["featured"]["slug"] == "zero-trust-modern-saas"
    assert "internal_notes" not in body["featured"]
    assert "internal_notes" not in body["articles"][0]

    card = await client.get("/api/v1/articles/zero-trust-modern-saas")
    assert card.status_code == 200
    assert "internal_notes" not in card.json()
    assert (await client.get("/api/v1/articles/draft-insight")).status_code == 404

    filtered = await client.get("/api/v1/articles", params={"topic": "security"})
    assert [item["slug"] for item in filtered.json()["articles"]] == ["zero-trust-modern-saas"]
    empty = await client.get("/api/v1/articles", params={"topic": "ai-ml"})
    assert empty.json()["articles"] == []


async def test_admin_crud_and_auth_boundaries(
    client: AsyncClient, auth_headers: dict[str, str], db_session: AsyncSession
) -> None:
    created = await client.post(
        "/api/v1/admin/articles/posts", json=ARTICLE, headers=auth_headers
    )
    assert created.status_code == 201
    admin_get = await client.get(
        "/api/v1/admin/articles/posts/zero-trust-modern-saas", headers=auth_headers
    )
    assert admin_get.json()["internal_notes"].startswith("Do not show")

    patched = await client.patch(
        "/api/v1/admin/articles/posts/zero-trust-modern-saas",
        json={"reading_minutes": 19, "is_published": True},
        headers=auth_headers,
    )
    assert patched.status_code == 200
    assert patched.json()["reading_minutes"] == 19

    assert (await client.get("/api/v1/admin/articles")).status_code == 401
    assert (await client.get("/api/v1/admin/articles/posts")).status_code == 401

    await user_service.create_user(
        db_session,
        UserCreate(
            email="viewer-articles@implesia.com",
            full_name="Viewer",
            password=TEST_PASSWORD,
            role=UserRole.VIEWER,
        ),
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "viewer-articles@implesia.com", "password": TEST_PASSWORD},
    )
    assert login.status_code == 200
    viewer = {"Authorization": f"Bearer {login.json()['access_token']}"}
    forbidden = await client.get("/api/v1/admin/articles/posts", headers=viewer)
    assert forbidden.status_code == 403
    assert forbidden.json()["error"]["code"] == "forbidden"

    deleted = await client.delete(
        "/api/v1/admin/articles/posts/zero-trust-modern-saas", headers=auth_headers
    )
    assert deleted.status_code == 200


async def test_duplicate_article_slug_conflicts(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    assert (
        await client.post("/api/v1/admin/articles/posts", json=ARTICLE, headers=auth_headers)
    ).status_code == 201
    again = await client.post(
        "/api/v1/admin/articles/posts", json=ARTICLE, headers=auth_headers
    )
    assert again.status_code == 409
