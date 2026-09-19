from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserRole
from app.schemas.user import UserCreate
from app.services import user_service
from tests.conftest import TEST_PASSWORD

PAGE_PATCH = {
    "hero_heading": "Tell us about your project.",
    "cta_heading": "Ready to build?",
    "form_action": "/api/v1/leads",
    "internal_notes": "Do not show this note on the public website.",
}


async def test_public_hides_internal_notes(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    patched = await client.patch("/api/v1/admin/contact", json=PAGE_PATCH, headers=auth_headers)
    assert patched.status_code == 200, patched.text
    assert patched.json()["internal_notes"].startswith("Do not show")

    public = await client.get("/api/v1/contact")
    assert public.status_code == 200, public.text
    body = public.json()
    assert body["hero_heading"].startswith("Tell us about")
    assert body["form_action"] == "/api/v1/leads"
    assert body["cta_heading"] == "Ready to build?"
    assert "internal_notes" not in body


async def test_admin_auth_boundaries(
    client: AsyncClient, auth_headers: dict[str, str], db_session: AsyncSession
) -> None:
    await client.patch("/api/v1/admin/contact", json=PAGE_PATCH, headers=auth_headers)

    assert (await client.get("/api/v1/admin/contact")).status_code == 401
    assert (await client.patch("/api/v1/admin/contact", json=PAGE_PATCH)).status_code == 401

    admin = await client.get("/api/v1/admin/contact", headers=auth_headers)
    assert admin.status_code == 200
    assert admin.json()["internal_notes"].startswith("Do not show")

    await user_service.create_user(
        db_session,
        UserCreate(
            email="viewer-contact@implesia.com",
            full_name="Viewer",
            password=TEST_PASSWORD,
            role=UserRole.VIEWER,
        ),
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "viewer-contact@implesia.com", "password": TEST_PASSWORD},
    )
    assert login.status_code == 200
    viewer = {"Authorization": f"Bearer {login.json()['access_token']}"}
    forbidden = await client.get("/api/v1/admin/contact", headers=viewer)
    assert forbidden.status_code == 403
    assert forbidden.json()["error"]["code"] == "forbidden"
