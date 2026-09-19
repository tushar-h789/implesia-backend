from httpx import AsyncClient

VALID_SERVICE = {
    "name": "SaaS Architecture",
    "slug": "saas-architecture",
    "tagline": "Cloud-native backends that scale from MVP to enterprise demand.",
    "description": "Cloud-native platforms built for reliability and elasticity from day one.",
    "category": "engineering",
    "icon": "cloud_sync",
    "engagement_status": "Available",
    "tech_stack": ["FastAPI", "PostgreSQL"],
    "hero_metrics": [{"value": "99.9%", "label": "Uptime SLA"}],
    "deliver_heading": "What we deliver for SaaS",
    "deliver_body": (
        "API-first backends with tenancy, observability, and a written architecture brief."
    ),
    "capabilities": ["Multi-tenant foundation", "Observability"],
    "deliverables_heading": "What You Receive",
    "deliverables_kicker": "Included in every engagement",
    "deliverables": ["API-first backend", "Admin hooks"],
    "process_heading": "How we work",
    "process_body": "Discovery, then a production-minded build.",
    "process_steps": ["Discovery", "Build", "Scale"],
    "outcomes_heading": "Before → After",
    "outcomes_disclaimer": "Results vary by scope and team.",
    "outcomes": [{"title": "Faster releases", "description": "Shorter cycle time after launch"}],
    "related_heading": "Related services",
    "related_slugs": ["web-platforms", "mobile-apps"],
    "faqs_heading": "Still have questions?",
    "faqs_body": "Our senior architects respond within 24 hours on business days.",
    "faqs": [
        {
            "question": "How long does a typical SaaS engagement take?",
            "answer": "Most first releases take 8–16 weeks after a two-week discovery sprint.",
        }
    ],
    "cta_heading": "Ready to architect your digital future?",
    "cta_body": "Schedule a confidential strategy session with our senior architects.",
    "cta_highlights": ["Free Strategy Call", "NDA Available", "Senior Engineers"],
    "seo_title": "SaaS Architecture | Implesia IT",
    "seo_description": "Cloud-native backends that scale from MVP to enterprise demand.",
    "is_published": True,
    "sort_order": 10,
}


async def test_public_list_hides_drafts(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    await client.post("/api/v1/admin/services", json=VALID_SERVICE, headers=auth_headers)
    await client.post(
        "/api/v1/admin/services",
        json={**VALID_SERVICE, "name": "Draft Only", "slug": "draft-only", "is_published": False},
        headers=auth_headers,
    )

    public = await client.get("/api/v1/services")
    assert public.status_code == 200
    slugs = [item["slug"] for item in public.json()["items"]]
    assert slugs == ["saas-architecture"]


async def test_public_get_by_id(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    created = await client.post("/api/v1/admin/services", json=VALID_SERVICE, headers=auth_headers)
    assert created.status_code == 201
    service_id = created.json()["id"]
    response = await client.get(f"/api/v1/services/{service_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "SaaS Architecture"
    assert body["engagement_status"] == "Available"
    assert body["hero_metrics"][0]["value"] == "99.9%"
    assert body["process_steps"][0]["title"] == "Discovery"
    assert body["faqs"][0]["question"].startswith("How long")
    assert body["cta_highlights"] == ["Free Strategy Call", "NDA Available", "Senior Engineers"]
    assert body["related_slugs"] == ["web-platforms", "mobile-apps"]
    assert body["seo_title"] == "SaaS Architecture | Implesia IT"
    assert (await client.get("/api/v1/services/saas-architecture")).status_code == 422


async def test_admin_get_by_id(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    created = await client.post("/api/v1/admin/services", json=VALID_SERVICE, headers=auth_headers)
    assert created.status_code == 201
    service_id = created.json()["id"]
    response = await client.get(f"/api/v1/admin/services/{service_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["slug"] == "saas-architecture"


async def test_public_cannot_read_draft_by_id(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    created = await client.post(
        "/api/v1/admin/services",
        json={**VALID_SERVICE, "slug": "hidden", "is_published": False},
        headers=auth_headers,
    )
    assert created.status_code == 201
    service_id = created.json()["id"]
    assert (await client.get(f"/api/v1/services/{service_id}")).status_code == 404
    assert (await client.get("/api/v1/services/hidden")).status_code == 422


async def test_admin_crud_round_trip(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    created = await client.post("/api/v1/admin/services", json=VALID_SERVICE, headers=auth_headers)
    assert created.status_code == 201, created.text
    service_id = created.json()["id"]

    listed = await client.get("/api/v1/admin/services", headers=auth_headers)
    assert listed.json()["total"] == 1

    updated = await client.patch(
        f"/api/v1/admin/services/{service_id}",
        json={"tagline": "Updated tagline for the SaaS offer."},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["tagline"].startswith("Updated")

    deleted = await client.delete(f"/api/v1/admin/services/{service_id}", headers=auth_headers)
    assert deleted.status_code == 200
    missing = await client.get(f"/api/v1/admin/services/{service_id}", headers=auth_headers)
    assert missing.status_code == 404


async def test_duplicate_slug_conflicts(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    assert (
        await client.post("/api/v1/admin/services", json=VALID_SERVICE, headers=auth_headers)
    ).status_code == 201
    again = await client.post("/api/v1/admin/services", json=VALID_SERVICE, headers=auth_headers)
    assert again.status_code == 409
    assert again.json()["error"]["code"] == "conflict"


async def test_admin_services_require_auth(client: AsyncClient) -> None:
    assert (await client.get("/api/v1/admin/services")).status_code == 401
