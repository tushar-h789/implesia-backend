from httpx import AsyncClient

MODEL = {
    "name": "Discovery Sprint",
    "slug": "discovery-sprint",
    "icon": "explore",
    "kicker": "2-week intensive",
    "price_label": "From $1,500",
    "price_amount": 1500,
    "currency": "USD",
    "cadence": "one_time",
    "subtitle": "Typical for a focused 2-week discovery",
    "description": "Validate your idea fast with research and a production-ready roadmap.",
    "inclusions": ["Stakeholder workshops", "Architecture blueprint"],
    "ideal_for": "New products & MVPs",
    "cta_label": "Discuss this model",
    "is_published": True,
    "sort_order": 10,
}

PACKAGE = {
    "name": "Product Landing Page",
    "slug": "product-landing-page",
    "icon": "rocket_launch",
    "tagline": "Single offer · conversion-focused",
    "price_label": "৳40,000",
    "price_amount_bdt": 40000,
    "timeline_label": "7–10 working days",
    "bugfix_label": "14-day bug fix",
    "audience": "Product launches & campaigns",
    "description": "One high-converting page to present an offer and drive enquiries.",
    "dashboard_heading": "No admin dashboard",
    "dashboard_body": "Public landing page only. Enquiries go to email or WhatsApp.",
    "inclusions": ["1 mobile-first custom landing page", "Lead form or WhatsApp CTA"],
    "exclusions": ["Admin dashboard or staff login", "Payment gateway / checkout"],
    "cta_label": "Enquire about Product Landing Page",
    "is_published": True,
    "sort_order": 10,
}

PAGE_PATCH = {
    "hero_heading": "Clear commercial paths. No guesswork.",
    "cta_heading": "Get a tailored investment estimate",
    "bdt_per_usd": 123,
    "faqs": [
        {
            "question": "What’s the difference between engagement models and packages?",
            "answer": "Models are custom ranges. Packages are fixed-scope BDT offers.",
        }
    ],
}


async def test_public_pricing_assembles_page(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    page = await client.patch("/api/v1/admin/pricing", json=PAGE_PATCH, headers=auth_headers)
    assert page.status_code == 200, page.text
    await client.post("/api/v1/admin/pricing/models", json=MODEL, headers=auth_headers)
    await client.post(
        "/api/v1/admin/pricing/models",
        json={**MODEL, "name": "Hidden Model", "slug": "hidden-model", "is_published": False},
        headers=auth_headers,
    )
    await client.post("/api/v1/admin/pricing/packages", json=PACKAGE, headers=auth_headers)
    await client.post(
        "/api/v1/admin/pricing/packages",
        json={
            **PACKAGE,
            "name": "Hidden Package",
            "slug": "hidden-package",
            "is_published": False,
        },
        headers=auth_headers,
    )

    public = await client.get("/api/v1/pricing")
    assert public.status_code == 200, public.text
    body = public.json()
    assert body["hero_heading"].startswith("Clear commercial")
    assert body["bdt_per_usd"] == 123
    assert body["faqs"][0]["question"].startswith("What’s the difference")
    slugs = [item["slug"] for item in body["models"]]
    assert slugs == ["discovery-sprint"]
    package_slugs = [item["slug"] for item in body["packages"]]
    assert package_slugs == ["product-landing-page"]
    assert body["packages"][0]["price_amount_bdt"] == 40000
    assert body["packages"][0]["exclusions"][0].startswith("Admin dashboard")


async def test_public_get_model_and_package(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    created_model = await client.post(
        "/api/v1/admin/pricing/models", json=MODEL, headers=auth_headers
    )
    created_package = await client.post(
        "/api/v1/admin/pricing/packages", json=PACKAGE, headers=auth_headers
    )
    assert created_model.status_code == 201
    assert created_package.status_code == 201
    model_id = created_model.json()["id"]
    package_id = created_package.json()["id"]

    model = await client.get(f"/api/v1/pricing/models/{model_id}")
    assert model.status_code == 200
    assert model.json()["price_label"] == "From $1,500"

    package = await client.get(f"/api/v1/pricing/packages/{package_id}")
    assert package.status_code == 200
    assert package.json()["price_label"] == "৳40,000"
    assert (await client.get("/api/v1/pricing/models/discovery-sprint")).status_code == 422

    hidden = await client.post(
        "/api/v1/admin/pricing/models",
        json={**MODEL, "slug": "draft-model", "is_published": False},
        headers=auth_headers,
    )
    assert hidden.status_code == 201
    assert (await client.get(f"/api/v1/pricing/models/{hidden.json()['id']}")).status_code == 404


async def test_admin_model_and_package_crud(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    created_model = await client.post(
        "/api/v1/admin/pricing/models", json=MODEL, headers=auth_headers
    )
    assert created_model.status_code == 201, created_model.text
    model_id = created_model.json()["id"]
    by_id = await client.get(f"/api/v1/admin/pricing/models/{model_id}", headers=auth_headers)
    assert by_id.status_code == 200
    patched = await client.patch(
        f"/api/v1/admin/pricing/models/{model_id}",
        json={"price_label": "From $1,800"},
        headers=auth_headers,
    )
    assert patched.json()["price_label"] == "From $1,800"

    created_package = await client.post(
        "/api/v1/admin/pricing/packages", json=PACKAGE, headers=auth_headers
    )
    assert created_package.status_code == 201, created_package.text
    package_id = created_package.json()["id"]
    updated = await client.patch(
        f"/api/v1/admin/pricing/packages/{package_id}",
        json={"price_amount_bdt": 42000, "price_label": "৳42,000"},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["price_amount_bdt"] == 42000

    listed = await client.get("/api/v1/admin/pricing/packages", headers=auth_headers)
    assert listed.json()["total"] == 1

    deleted = await client.delete(
        f"/api/v1/admin/pricing/packages/{package_id}", headers=auth_headers
    )
    assert deleted.status_code == 200
    assert (
        await client.get(f"/api/v1/admin/pricing/packages/{package_id}", headers=auth_headers)
    ).status_code == 404


async def test_duplicate_model_slug_conflicts(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    assert (
        await client.post("/api/v1/admin/pricing/models", json=MODEL, headers=auth_headers)
    ).status_code == 201
    again = await client.post("/api/v1/admin/pricing/models", json=MODEL, headers=auth_headers)
    assert again.status_code == 409
    assert again.json()["error"]["code"] == "conflict"


async def test_admin_pricing_requires_auth(client: AsyncClient) -> None:
    assert (await client.get("/api/v1/admin/pricing")).status_code == 401
    assert (await client.get("/api/v1/admin/pricing/models")).status_code == 401
    assert (await client.get("/api/v1/admin/pricing/packages")).status_code == 401
