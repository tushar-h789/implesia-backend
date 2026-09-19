"""Upsert the public Implesia /pricing page, models, and BDT packages.

Usage:
    python -m scripts.seed_pricing
"""

import asyncio

from app.core.exceptions import NotFoundError
from app.db.session import SessionLocal
from app.schemas.pricing import (
    EngagementModelCreate,
    EngagementModelUpdate,
    PricingPackageCreate,
    PricingPackageUpdate,
    PricingPageBase,
)
from app.services import pricing_service

PAGE = PricingPageBase(
    slug="pricing",
    hero_heading="Clear commercial paths. No guesswork.",
    hero_body=(
        "Choose a custom engagement for product work, or a fixed BDT package "
        "when your brief is already defined. Strategy calls are free either way."
    ),
    paths_kicker="Start here",
    paths_heading="Pick the path that fits your brief",
    paths_body=(
        "Custom product work and fixed local packages are priced differently "
        "on purpose—so expectations stay clear from day one."
    ),
    paths=[
        {
            "icon": "hub",
            "kicker": "Custom engagements",
            "title": "Software teams & tailored builds",
            "body": (
                "Discovery sprints, dedicated squads, and milestone delivery "
                "for products that need senior engineering judgment."
            ),
            "note": "Typical ranges · scoped after a strategy call",
            "cta_label": "View engagement models",
            "anchor": "models",
        },
        {
            "icon": "inventory_2",
            "kicker": "Productized packages",
            "title": "Fixed-scope work for Bangladesh",
            "body": (
                "Landing pages, starter e-commerce, and a simple LMS—with "
                "fixed BDT pricing, written scope, and a defined timeline."
            ),
            "note": "Fixed BDT · clear inclusions & exclusions",
            "cta_label": "View starter packages",
            "anchor": "packages",
        },
    ],
    models_kicker="Custom engagements",
    models_heading="How we partner on custom work",
    models_body=(
        "Typical starting ranges for discovery, embedded teams, and milestone "
        "delivery—not fixed SKUs. Your strategy call produces a tailored estimate."
    ),
    models_currency_note="Ranges shown in USD · switch anytime",
    models_disclaimer=(
        "Typical investment ranges for mid-market engagements. BDT figures are "
        "approximate (≈ ৳123 / USD) for local reference and may differ at invoice "
        "time. Enterprise or highly regulated scope may differ. Ranges are "
        "directional and do not constitute a binding offer."
    ),
    packages_kicker="Productized packages · Bangladesh",
    packages_heading="Fixed scope. Fixed BDT.",
    packages_body=(
        "Repeatable deliverables for local businesses that want a clear price "
        "and timeline. Each package states whether you get a public website only, "
        "a content CMS, or a full operations dashboard."
    ),
    packages_currency_note="Prices are set in BDT · USD is an approximate conversion",
    commercial_terms=[
        {
            "icon": "payments",
            "title": "50 / 50 billing",
            "body": "50% to kick off, 50% on acceptance of the agreed deliverables.",
        },
        {
            "icon": "description",
            "title": "Written brief first",
            "body": "Kickoff starts after content, brand assets, and a signed package brief.",
        },
        {
            "icon": "rate_review",
            "title": "Two revision rounds",
            "body": "Included in every package. Extra rounds are quoted as add-ons.",
        },
        {
            "icon": "verified",
            "title": "Post-launch cover",
            "body": "Bug fix for the window listed on each package—functional defects only.",
        },
    ],
    packages_disclaimer=(
        "Package prices are fixed for the written scope only. “Content CMS” means "
        "editing website content—not running orders, bookings, or clinical ops. "
        "“Admin dashboard” means a staff backend for day-to-day operations listed "
        "in that package. Domain, hosting, SSL, premium plugins, payment gateway "
        "fees, SMS gateways, and third-party licenses are separate unless confirmed "
        "in writing. Hospital Management is a starter clinic/small-hospital "
        "scope—not a full enterprise HIS. USD amounts are approximate conversions "
        "for reference."
    ),
    process_kicker="Custom engagements",
    process_heading="How custom quoting works",
    process_body=(
        "For engagement models only. Fixed packages skip ROM estimating—after a "
        "short fit call we confirm the package brief and kick off."
    ),
    process_steps=[
        {
            "title": "Strategy call",
            "description": (
                "Free discovery session with a senior engineer to align on goals, "
                "constraints, and success criteria."
            ),
        },
        {
            "title": "ROM estimate",
            "description": (
                "A rough order-of-magnitude range based on scope, complexity, and "
                "team composition—not a binding quote."
            ),
        },
        {
            "title": "Statement of work",
            "description": (
                "Detailed deliverables, milestones, commercial terms, and "
                "change-control process—ready to sign."
            ),
        },
        {
            "title": "Kickoff",
            "description": (
                "Dedicated channel, shared roadmap, and first sprint planned "
                "within days of agreement."
            ),
        },
    ],
    faqs_kicker="Pricing FAQ",
    faqs_heading="Common questions about investment",
    faqs=[
        {
            "question": "What’s the difference between engagement models and packages?",
            "answer": (
                "Engagement models are for custom or evolving software—scoped after "
                "discovery, with typical USD/BDT ranges. Productized packages are "
                "fixed-scope, fixed-BDT offers for Bangladesh businesses, with written "
                "inclusions, exclusions, and commercial terms."
            ),
        },
        {
            "question": "How do package payments work?",
            "answer": (
                "Packages use 50 / 50 billing: 50% to kick off and 50% on acceptance "
                "of the agreed deliverables. Kickoff starts after content, brand "
                "assets, and a signed package brief."
            ),
        },
        {
            "question": "Why don’t custom projects have a fixed price menu?",
            "answer": (
                "Custom work is scoped after a strategy call. The ranges on this page "
                "are typical starting points for discovery, embedded teams, and "
                "milestone delivery—not fixed SKUs or a binding offer."
            ),
        },
        {
            "question": "What currency do you invoice in?",
            "answer": (
                "Packages are priced and invoiced in BDT. Engagement-model ranges are "
                "shown in USD and can be converted at about ৳123 / USD for local "
                "reference. The invoice currency is confirmed in the statement of work."
            ),
        },
        {
            "question": "Do packages include a dashboard or backend?",
            "answer": (
                "Only when the card says so. Some packages are a public site only, "
                "some include a content CMS to edit text and images, and some include "
                "a staff operations dashboard. That distinction is written on each card."
            ),
        },
        {
            "question": "Is the Hospital Management package a full hospital HIS?",
            "answer": (
                "No. It is a starter clinic / small-hospital scope for outpatient "
                "operations—not a full enterprise HIS, multi-branch chain, LIS, RIS, "
                "PACS, or insurance claims suite."
            ),
        },
        {
            "question": "What if I need more than a package includes?",
            "answer": (
                "We quote the extra work as an add-on or move you to a custom "
                "engagement model after a strategy call. Package prices stay fixed "
                "for the written scope only."
            ),
        },
        {
            "question": "Do you offer retainers after launch?",
            "answer": (
                "Yes. Dedicated Squad is a monthly retainer for ongoing product work. "
                "Packages include a listed bug-fix window; longer support is scoped "
                "separately."
            ),
        },
    ],
    cta_heading="Get a tailored investment estimate",
    cta_body=(
        "Book a confidential strategy session. We’ll map your scope to the right "
        "engagement model or package and a clear commercial path."
    ),
    cta_highlights=["Free strategy call", "NDA available", "No obligation quote"],
    cta_primary_label="Book a consultation",
    cta_secondary_label="View case studies",
    seo_title="Pricing | Implesia IT",
    seo_description=(
        "Clear commercial paths. Custom engagement ranges or fixed BDT packages "
        "for Bangladesh—strategy calls are free either way."
    ),
    bdt_per_usd=123,
)

MODELS = [
    EngagementModelCreate(
        name="Discovery Sprint",
        slug="discovery-sprint",
        icon="explore",
        kicker="2-week intensive",
        price_label="From $1,500",
        price_amount=1500,
        currency="USD",
        cadence="one_time",
        subtitle="Typical for a focused 2-week discovery",
        description=(
            "Validate your idea fast with user research, technical feasibility, "
            "and a production-ready roadmap."
        ),
        inclusions=[
            "Stakeholder workshops",
            "Architecture blueprint",
            "MVP scope & timeline",
        ],
        ideal_for="New products & MVPs",
        cta_label="Discuss this model",
        sort_order=10,
    ),
    EngagementModelCreate(
        name="Dedicated Squad",
        slug="dedicated-squad",
        icon="groups",
        kicker="Embedded engineers",
        badge="Most Popular",
        price_label="From $6,000/mo",
        price_amount=6000,
        currency="USD",
        cadence="monthly",
        subtitle="Senior-led small squad · monthly retainer",
        description=(
            "A senior-led team integrated into your workflow—shipping features "
            "every sprint with full transparency."
        ),
        inclusions=[
            "Senior tech lead included",
            "Bi-weekly sprint demos",
            "Slack & dashboard access",
        ],
        ideal_for="Scaling product teams",
        cta_label="Discuss this model",
        sort_order=20,
    ),
    EngagementModelCreate(
        name="Fixed-scope Delivery",
        slug="fixed-scope-delivery",
        icon="flag",
        kicker="Milestone-based",
        price_label="From $10,000",
        price_amount=10000,
        currency="USD",
        cadence="one_time",
        subtitle="Defined deliverables · milestone billing",
        description=(
            "Clearly defined deliverables, fixed timeline, and predictable "
            "budget—ideal for well-scoped initiatives."
        ),
        inclusions=[
            "Signed scope document",
            "Milestone payment schedule",
            "Acceptance criteria per phase",
        ],
        ideal_for="Defined project briefs",
        cta_label="Discuss this model",
        sort_order=30,
    ),
]

PACKAGES = [
    PricingPackageCreate(
        name="Product Landing Page",
        slug="product-landing-page",
        icon="rocket_launch",
        tagline="Single offer · conversion-focused",
        price_label="৳40,000",
        price_amount_bdt=40000,
        timeline_label="7–10 working days",
        bugfix_label="14-day bug fix",
        audience="Product launches & campaigns",
        description=(
            "One high-converting page to present an offer, build trust, and drive "
            "enquiries or purchases."
        ),
        dashboard_heading="No admin dashboard",
        dashboard_body=(
            "Public landing page only. Enquiries go to email or WhatsApp—no staff login panel."
        ),
        inclusions=[
            "1 mobile-first custom landing page",
            "Hero, benefits, proof, FAQ, and primary CTA",
            "Lead form or WhatsApp / buy CTA",
            "Basic on-page SEO and Open Graph tags",
            "Staging review before go-live",
        ],
        exclusions=[
            "Admin dashboard or staff login",
            "Multi-page site, CMS, or blog",
            "Payment gateway / checkout",
            "Ad creatives or copywriting retainers",
        ],
        cta_label="Enquire about Product Landing Page",
        sort_order=10,
    ),
    PricingPackageCreate(
        name="Marketing Site",
        slug="marketing-site",
        icon="web",
        tagline="Up to 5 pages · SME presence",
        price_label="৳55,000",
        price_amount_bdt=55000,
        timeline_label="10–14 working days",
        bugfix_label="14-day bug fix",
        audience="Service businesses & local brands",
        description=(
            "A compact marketing site to explain what you do, earn trust, and "
            "collect qualified enquiries."
        ),
        dashboard_heading="Content CMS only",
        dashboard_body=(
            "Lightweight CMS to update text and images. Not an operations "
            "dashboard for orders or users."
        ),
        inclusions=[
            "Up to 5 pages (Home + 4 inner pages)",
            "Contact form plus map or WhatsApp link",
            "Content CMS for text and images",
            "Responsive UI and basic SEO structure",
            "Staging review before go-live",
        ],
        exclusions=[
            "Operations / analytics dashboard",
            "Member logins or staff role panels",
            "E-commerce cart or payments",
            "Custom ERP / CRM integrations",
        ],
        cta_label="Enquire about Marketing Site",
        sort_order=20,
    ),
    PricingPackageCreate(
        name="Company Profile Website",
        slug="company-profile-website",
        icon="apartment",
        tagline="About · services · credibility",
        price_label="৳65,000",
        price_amount_bdt=65000,
        timeline_label="12–16 working days",
        bugfix_label="14-day bug fix",
        audience="SMEs, agencies & local firms",
        description=(
            "A polished company website to present your brand, services, team, "
            "and contact paths—built for Bangladesh business credibility."
        ),
        dashboard_heading="Content CMS only",
        dashboard_body=(
            "Edit pages, services, team, and gallery from a simple CMS. No "
            "business-operations dashboard."
        ),
        inclusions=[
            "Up to 7 pages (Home, About, Services, Team, Gallery, FAQ, Contact)",
            "Service detail sections and enquiry form",
            "Google Maps embed and WhatsApp CTA",
            "Content CMS for text and images",
            "Basic SEO structure and staging review",
        ],
        exclusions=[
            "Staff operations dashboard",
            "Online payments or booking engine",
            "Multi-language beyond Bangla/English",
            "Custom portal or HR / CRM modules",
        ],
        cta_label="Enquire about Company Profile Website",
        sort_order=30,
    ),
    PricingPackageCreate(
        name="Restaurant Menu & Orders",
        slug="restaurant-menu-orders",
        icon="restaurant",
        tagline="Digital menu · order intake",
        price_label="৳85,000",
        price_amount_bdt=85000,
        timeline_label="2–4 weeks",
        bugfix_label="21-day bug fix",
        audience="Cafés, restaurants & cloud kitchens",
        description=(
            "A mobile-first menu site so customers browse dishes, place orders, "
            "and reach you—plus an admin dashboard to keep the menu current."
        ),
        dashboard_heading="Includes admin dashboard",
        dashboard_body=(
            "Staff dashboard to manage menu items, availability, and incoming "
            "orders (WhatsApp / call handoff)."
        ),
        inclusions=[
            "Public menu site with up to 80 items seeded",
            "Item photos, prices, and availability flags",
            "Order form with WhatsApp / call handoff",
            "Admin dashboard for menu & order intake",
            "Responsive UI and basic SEO",
        ],
        exclusions=[
            "Full payment gateway checkout",
            "Rider / delivery logistics system",
            "Multi-branch inventory sync",
            "Customer account portal",
        ],
        cta_label="Enquire about Restaurant Menu & Orders",
        sort_order=40,
    ),
    PricingPackageCreate(
        name="Appointment Booking",
        slug="appointment-booking",
        icon="event_available",
        tagline="Schedule · confirm · manage",
        price_label="৳95,000",
        price_amount_bdt=95000,
        timeline_label="3–4 weeks",
        bugfix_label="30-day bug fix",
        audience="Clinics, salons & consultants",
        description=(
            "A focused booking system for services that sell time—customers book "
            "online; your team runs the schedule from an admin dashboard."
        ),
        dashboard_heading="Includes admin dashboard",
        dashboard_body=(
            "Staff dashboard with calendar to accept, reschedule, and track "
            "appointments day to day."
        ),
        inclusions=[
            "Public booking page with service slots",
            "Customer booking form with confirmation",
            "Admin dashboard & calendar to manage bookings",
            "Email or SMS notification hook (one channel)",
            "Responsive UI and basic SEO page",
        ],
        exclusions=[
            "Multi-location staff rostering",
            "Insurance / EMR integrations",
            "Native mobile apps or full wallet suite",
            "Advanced analytics suite",
        ],
        cta_label="Enquire about Appointment Booking",
        sort_order=50,
    ),
    PricingPackageCreate(
        name="Starter E-commerce",
        slug="starter-ecommerce",
        icon="storefront",
        tagline="Catalog · cart · local payments",
        badge="Most requested",
        price_label="৳1,25,000",
        price_amount_bdt=125000,
        timeline_label="3–5 weeks",
        bugfix_label="30-day bug fix",
        audience="Retail & D2C brands",
        description=(
            "A focused storefront to list products, take orders, and accept common "
            "Bangladesh payment methods—with a backend admin dashboard to run the shop."
        ),
        dashboard_heading="Includes admin dashboard",
        dashboard_body=(
            "Store admin dashboard to manage products, inventory basics, and orders "
            "after customers check out."
        ),
        inclusions=[
            "Public storefront with up to 50 seeded products",
            "Cart, checkout, and order management",
            "One payment gateway integration",
            "Admin dashboard for products and orders",
            "Responsive storefront and basic SEO",
        ],
        exclusions=[
            "Multi-vendor marketplace",
            "Native mobile apps",
            "Warehouse / advanced inventory systems",
            "Customer loyalty / wallet modules",
        ],
        cta_label="Enquire about Starter E-commerce",
        sort_order=60,
    ),
    PricingPackageCreate(
        name="Simple LMS",
        slug="simple-lms",
        icon="school",
        tagline="Courses · enrollment · access control",
        price_label="৳1,95,000",
        price_amount_bdt=195000,
        timeline_label="4–6 weeks",
        bugfix_label="30-day bug fix",
        audience="Coaches & training institutes",
        description=(
            "A lean learning platform to publish courses, enroll students, and gate "
            "content—with an admin dashboard for instructors and a learner login "
            "for students."
        ),
        dashboard_heading="Includes admin dashboard",
        dashboard_body=(
            "Instructor/admin dashboard to publish courses, manage enrollments, "
            "and control content access. Students get a learner login—not a staff "
            "ops suite."
        ),
        inclusions=[
            "Course and lesson management (admin dashboard)",
            "Student signup / login (learner portal)",
            "Enrollment and content gating",
            "Basic progress tracking",
            "One payment option for course fees",
        ],
        exclusions=[
            "Live class / Zoom integrations",
            "Certificates, quizzes, or proctoring",
            "Mobile apps or SCORM / multi-tenant",
            "Enterprise HR / SSO suites",
        ],
        cta_label="Enquire about Simple LMS",
        sort_order=70,
    ),
    PricingPackageCreate(
        name="Hospital Management System",
        slug="hospital-management-system",
        icon="local_hospital",
        tagline="Clinic / starter hospital ops",
        badge="Healthcare",
        price_label="৳3,75,000",
        price_amount_bdt=375000,
        timeline_label="8–12 weeks",
        bugfix_label="60-day bug fix",
        audience="Clinics, diagnostic centres & small hospitals",
        description=(
            "A starter HMS for outpatient operations—patient records, appointments, "
            "billing, and role-based dashboards—scoped for Bangladesh clinics and "
            "small hospitals. Full enterprise HIS is quoted separately."
        ),
        dashboard_heading="Role-based dashboards",
        dashboard_body=(
            "Staff dashboards by role (reception, doctor, accounts) plus operational "
            "reports. This is a backend system first—not a marketing website package."
        ),
        inclusions=[
            "Patient registration and basic profiles",
            "Doctor / department setup and OPD appointments",
            "Visit notes / basic clinical record per visit",
            "Billing, invoices, and payment status tracking",
            "Role-based admin dashboards (reception, doctor, accounts)",
            "Dashboard reports (patients, revenue, appointments)",
        ],
        exclusions=[
            "Public marketing website rebuild",
            "Full HIS / multi-branch hospital chains",
            "LIS, RIS, PACS, or advanced EMR",
            "Insurance claims, biometric, or telemedicine suites",
        ],
        cta_label="Enquire about Hospital Management System",
        sort_order=80,
    ),
]


async def main() -> None:
    models_created = 0
    models_updated = 0
    packages_created = 0
    packages_updated = 0
    async with SessionLocal() as db:
        await pricing_service.upsert_page(db, PAGE.model_dump(mode="json"))
        for payload in MODELS:
            try:
                existing = await pricing_service.get_model_by_slug(db, payload.slug or "")
            except NotFoundError:
                await pricing_service.create_model(db, payload)
                models_created += 1
                continue
            await pricing_service.update_model(
                db, existing, EngagementModelUpdate.model_validate(payload.model_dump())
            )
            models_updated += 1
        for payload in PACKAGES:
            try:
                existing = await pricing_service.get_package_by_slug(db, payload.slug or "")
            except NotFoundError:
                await pricing_service.create_package(db, payload)
                packages_created += 1
                continue
            await pricing_service.update_package(
                db, existing, PricingPackageUpdate.model_validate(payload.model_dump())
            )
            packages_updated += 1
    print(
        "Pricing page upserted. "
        f"Models +{models_created}/~{models_updated}. "
        f"Packages +{packages_created}/~{packages_updated}."
    )


if __name__ == "__main__":
    asyncio.run(main())
