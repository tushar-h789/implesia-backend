from httpx import AsyncClient

VALID_LEAD = {
    "full_name": "Jonathan Reid",
    "email": "j.reid@acme.com",
    "phone": "+44 20 7946 0000",
    "organisation": "Acme Corporation",
    "service_area": "saas-architecture",
    "timeline": "1-3-months",
    "brief": "We need to modernise a legacy monolith into a cloud-native platform.",
    "source_page": "/contact",
}


async def test_submit_lead_creates_a_record(client: AsyncClient) -> None:
    response = await client.post("/api/v1/leads", json=VALID_LEAD)
    assert response.status_code == 201, response.text
    assert response.json()["id"]


async def test_brief_must_be_substantial(client: AsyncClient) -> None:
    response = await client.post("/api/v1/leads", json={**VALID_LEAD, "brief": "hi"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


async def test_invalid_email_is_rejected(client: AsyncClient) -> None:
    response = await client.post("/api/v1/leads", json={**VALID_LEAD, "email": "not-an-email"})
    assert response.status_code == 422


async def test_idempotency_key_prevents_duplicates(client: AsyncClient) -> None:
    headers = {"Idempotency-Key": "abc-123"}
    first = await client.post("/api/v1/leads", json=VALID_LEAD, headers=headers)
    second = await client.post("/api/v1/leads", json=VALID_LEAD, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] == second.json()["id"]


async def test_honeypot_submission_is_parked_as_spam(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    response = await client.post(
        "/api/v1/leads", json={**VALID_LEAD, "website": "http://spam.example"}
    )
    assert response.status_code == 201

    stats = await client.get("/api/v1/admin/leads/stats", headers=auth_headers)
    assert stats.json()["spam"] == 1
    assert stats.json()["new"] == 0


async def test_listing_leads_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/admin/leads")
    assert response.status_code == 401


async def test_admin_can_list_and_update_leads(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    created = await client.post("/api/v1/leads", json=VALID_LEAD)
    lead_id = created.json()["id"]

    listing = await client.get("/api/v1/admin/leads", headers=auth_headers)
    assert listing.status_code == 200
    assert listing.json()["total"] == 1

    updated = await client.patch(
        f"/api/v1/admin/leads/{lead_id}",
        json={"status": "qualified", "internal_notes": "Booked a discovery call."},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "qualified"


async def test_lead_search_filters_by_organisation(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    await client.post("/api/v1/leads", json=VALID_LEAD)

    hit = await client.get("/api/v1/admin/leads?search=acme", headers=auth_headers)
    miss = await client.get("/api/v1/admin/leads?search=nordic", headers=auth_headers)

    assert hit.json()["total"] == 1
    assert miss.json()["total"] == 0
