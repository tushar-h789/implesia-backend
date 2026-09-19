"""Upsert the public Implesia /portfolio page and case studies.

Usage:
    python -m scripts.seed_portfolio
"""

import asyncio

from app.core.exceptions import NotFoundError
from app.db.session import SessionLocal
from app.schemas.portfolio import (
    PortfolioPageBase,
    PortfolioProjectCreate,
    PortfolioProjectUpdate,
)
from app.services import portfolio_service

PAGE = PortfolioPageBase(
    slug="portfolio",
    hero_heading="Production software that delivers.",
    hero_body=(
        "A curated portfolio of full-stack web platforms, marketplaces, SaaS "
        "products, and healthcare systems — each built with modern architectures "
        "and delivered to production."
    ),
    hero_metrics=[
        {"value": "12+", "label": "Live projects"},
        {"value": "8+", "label": "Industry verticals"},
        {"value": "100%", "label": "Completed delivery"},
    ],
    hero_highlights=["Full-stack delivery", "Production deployments", "Modern tech stack"],
    featured_kicker="Featured case study",
    featured_heading="Flagship engagement.",
    featured_body=(
        "A representative full-stack delivery — from frontend experience to "
        "backend infrastructure, shipped as a production-ready platform."
    ),
    archive_kicker="Project archive",
    archive_heading="Delivered engagements.",
    archive_body=(
        "Production-ready platforms across marketplaces, SaaS, healthcare, and "
        "enterprise web — engineered with Next.js and modern full-stack architectures."
    ),
    categories=[
        {"slug": "marketplace", "label": "Marketplaces"},
        {"slug": "saas", "label": "SaaS & tools"},
        {"slug": "healthcare", "label": "Healthcare"},
        {"slug": "web", "label": "Web platforms"},
    ],
    impact_kicker="Collective impact",
    impact_heading="Numbers that reflect real delivery.",
    impact_body=(
        "Outcomes across our delivered engagements — measured against production "
        "deployments and completed delivery, not projections."
    ),
    impact_stats=[
        {
            "value": "12+",
            "title": "Production deployments",
            "body": (
                "Enterprise platforms, SaaS products, and web systems shipped to "
                "live production environments."
            ),
        },
        {
            "value": "100%",
            "title": "Completed delivery rate",
            "body": (
                "Every engagement delivered to agreed scope — on time, tested, "
                "and production-ready."
            ),
        },
        {
            "value": "8+",
            "title": "Industry verticals",
            "body": (
                "Marketplaces, healthcare, aviation, LMS, and enterprise web "
                "across diverse industry sectors."
            ),
        },
        {
            "value": "Full-stack",
            "title": "Engineering scope",
            "body": (
                "Frontend, backend, dashboards, and infrastructure — end-to-end "
                "from architecture to deployment."
            ),
        },
    ],
    pillars_kicker="Delivery model",
    pillars_heading="Engineered for outcomes, not just output.",
    pillars_body=(
        "A structured delivery framework applied across every engagement — "
        "reducing risk, maintaining stakeholder visibility, and shipping software "
        "validated in production environments."
    ),
    pillars=[
        {
            "kicker": "Pillar 01",
            "title": "Discovery-led",
            "body": (
                "Structured technical discovery before development begins — aligning "
                "architecture, scope, dependencies, and measurable success criteria "
                "with stakeholders upfront."
            ),
            "deliverables": [
                "Technical scoping",
                "Architecture review",
                "Delivery roadmap",
            ],
        },
        {
            "kicker": "Pillar 02",
            "title": "Engineering-first",
            "body": (
                "Clean architecture, automated testing, and CI/CD pipelines embedded "
                "from sprint one — ensuring maintainable, production-grade code at "
                "every release."
            ),
            "deliverables": [
                "Clean architecture",
                "Automated testing",
                "CI/CD pipelines",
            ],
        },
        {
            "kicker": "Pillar 03",
            "title": "Outcome-driven",
            "body": (
                "Measurable KPIs defined at kickoff and tracked through production — "
                "covering performance, reliability, conversion, and operational "
                "efficiency."
            ),
            "deliverables": [
                "Production KPIs",
                "Performance tracking",
                "Post-launch support",
            ],
        },
    ],
    engagement_highlights=[
        "Agile delivery",
        "Code review standards",
        "Production monitoring",
    ],
    cta_heading="Ready to build something remarkable?",
    cta_body=(
        "Share your requirements and we'll respond with a structured technical "
        "assessment, delivery roadmap, and timeline — typically within one "
        "business day."
    ),
    cta_highlights=["Free discovery call", "Senior architects", "NDA available"],
    cta_primary_label="Book a discovery call",
    cta_secondary_label="Contact our team",
    seo_title="Portfolio | Implesia IT",
    seo_description=(
        "Production software that delivers. Full-stack web platforms, "
        "marketplaces, SaaS, and healthcare systems shipped to live environments."
    ),
)

PROJECTS = [
    PortfolioProjectCreate(
        name="Gulf Franchise",
        slug="gulf-franchise",
        tagline="Franchise & Franchisor Shop Buy/Rent",
        category="marketplace",
        year=2025,
        status="Completed",
        summary=(
            "Full-stack franchise discovery platform connecting franchisors with "
            "buyers and renters across the Gulf — with listings, search, and lead "
            "management workflows."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "Laravel"],
        live_url="https://gulffranchisehub.com",
        live_label="gulffranchisehub.com",
        outcomes=[
            {"title": "Live", "description": "Production deployment"},
            {"title": "Full-stack", "description": "Delivery scope"},
        ],
        is_featured=True,
        sort_order=10,
    ),
    PortfolioProjectCreate(
        name="Baby Grow",
        slug="baby-grow",
        tagline="Baby Growth & Parenting",
        category="web",
        year=2025,
        summary=(
            "Parenting guide platform helping UK families track baby growth "
            "milestones, access curated content, and navigate early-stage childcare "
            "with confidence."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "Node.js"],
        live_url="https://www.thebabygrow.co.uk",
        live_label="thebabygrow.co.uk",
        sort_order=20,
    ),
    PortfolioProjectCreate(
        name="PowerUp",
        slug="powerup",
        tagline="Power Bank Buy & Sell",
        category="marketplace",
        year=2025,
        summary=(
            "E-commerce marketplace for portable power bank devices — with product "
            "listings, inquiry flows, and integrated email notifications for buyers "
            "and sellers."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "Node.js"],
        sort_order=30,
    ),
    PortfolioProjectCreate(
        name="Influencer Hire",
        slug="influencer-hire",
        tagline="Influencer Hiring & Video Commerce",
        category="marketplace",
        year=2025,
        summary=(
            "Influencer hiring marketplace enabling brands to commission recorded "
            "video content — with creator profiles, campaign management, and secure "
            "transaction flows."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "shadcn/ui"],
        sort_order=40,
    ),
    PortfolioProjectCreate(
        name="Career Calculator",
        slug="career-calculator",
        tagline="Career Guidance & Calculation",
        category="saas",
        year=2025,
        summary=(
            "Interactive career guidance platform with calculation engines and "
            "personalised pathway recommendations — helping users make informed "
            "professional decisions."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "shadcn/ui"],
        sort_order=50,
    ),
    PortfolioProjectCreate(
        name="Global Trade Journey",
        slug="global-trade-journey",
        tagline="Global Trade & Safe Food Standards",
        category="web",
        year=2025,
        summary=(
            "Educational platform guiding organisations through global food trade "
            "compliance journeys — with structured modules, resources, and progress "
            "tracking."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "shadcn/ui"],
        sort_order=60,
    ),
    PortfolioProjectCreate(
        name="Digital QA Assistant",
        slug="digital-qa-assistant",
        tagline="QA Audit & Test Automation",
        category="saas",
        year=2025,
        summary=(
            "Digital quality assurance platform bridging manual audit workflows to "
            "automated testing pipelines — reducing QA cycle time and improving "
            "release confidence."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "shadcn/ui"],
        sort_order=70,
    ),
    PortfolioProjectCreate(
        name="Telemedicine",
        slug="telemedicine",
        tagline="Telehealth & Patient Consultations",
        category="healthcare",
        year=2025,
        summary=(
            "Telemedicine platform with doctor appointment scheduling, WebRTC "
            "audio/video consultations, and real-time patient–provider messaging "
            "over WebSocket."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "NestJS"],
        sort_order=80,
    ),
    PortfolioProjectCreate(
        name="Flyger Academy",
        slug="flyger-academy",
        tagline="Aviation Academy & Training",
        category="saas",
        year=2026,
        summary=(
            "Aviation academy platform with a public website plus dedicated "
            "instructor, student, and admin dashboards — delivered as an "
            "organisation-based SaaS product on a microservices architecture."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "Microservices"],
        sort_order=90,
    ),
    PortfolioProjectCreate(
        name="Flyger Tech",
        slug="flyger-tech",
        tagline="Software & Technology",
        category="web",
        year=2026,
        summary=(
            "Corporate website for a software and technology company — presenting "
            "services, technical capabilities, and brand identity with a modern, "
            "performance-focused web experience."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "TypeScript"],
        sort_order=100,
    ),
    PortfolioProjectCreate(
        name="Flyger OTA",
        slug="flyger-ota",
        tagline="Online Travel Agency",
        category="web",
        year=2026,
        summary=(
            "Online travel agency platform for discovering and booking flights and "
            "travel services — with search, booking workflows, and a customer-facing "
            "web experience."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "Node.js"],
        sort_order=110,
    ),
    PortfolioProjectCreate(
        name="Arong LMS",
        slug="arong-lms",
        tagline="Corporate Learning & Development",
        category="saas",
        year=2026,
        summary=(
            "Corporate learning management system built for Arong — enabling course "
            "delivery, employee progress tracking, assessments, and admin reporting "
            "across the organisation."
        ),
        tech_stack=["Next.js", "Tailwind CSS", "NestJS"],
        sort_order=120,
    ),
]


async def main() -> None:
    created = 0
    updated = 0
    async with SessionLocal() as db:
        await portfolio_service.upsert_page(db, PAGE.model_dump(mode="json"))
        for payload in PROJECTS:
            try:
                existing = await portfolio_service.get_project_by_slug(db, payload.slug or "")
            except NotFoundError:
                await portfolio_service.create_project(db, payload)
                created += 1
                continue
            await portfolio_service.update_project(
                db, existing, PortfolioProjectUpdate.model_validate(payload.model_dump())
            )
            updated += 1
    print(f"Portfolio page upserted. Projects +{created}/~{updated}.")


if __name__ == "__main__":
    asyncio.run(main())
