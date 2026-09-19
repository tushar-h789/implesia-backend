"""Upsert the public Implesia /about-us page.

Usage:
    python -m scripts.seed_about
"""

import asyncio

from app.db.session import SessionLocal
from app.schemas.about import AboutPageBase
from app.services import about_service

PAGE = AboutPageBase(
    slug="about-us",
    hero_kicker="About Implesia IT",
    hero_heading="Engineering platforms that perform under pressure.",
    hero_body=(
        "Implesia IT is a software engineering partner for organisations that "
        "treat uptime, security, and maintainability as business priorities—"
        "not afterthoughts. We design and deliver systems built to operate "
        "reliably at scale."
    ),
    hero_primary_label="Explore Services",
    hero_secondary_label="Our Process",
    hero_highlights=[
        "Enterprise Delivery Standards",
        "100+ Projects Shipped",
        "98% Client Retention",
    ],
    hero_metrics=[
        {"value": "100+", "label": "Projects Delivered"},
        {"value": "45+", "label": "Global Clients"},
        {"value": "12+", "label": "Years Expertise"},
        {"value": "98%", "label": "Retention Rate"},
    ],
    quote_kicker="Delivery in practice",
    quote_text=(
        "Sustainable software is not a feature. It is the outcome of deliberate "
        "architecture, accountable delivery, and systems designed to evolve."
    ),
    quote_attribution="Implesia IT · Engineering principles",
    story_kicker="Who We Are",
    story_heading="Built for Enterprise Outcomes",
    story_body=(
        "Implesia IT partners with organisations that require dependable digital "
        "platforms—where uptime, security, and maintainability are "
        "non-negotiable. We combine architectural discipline with modern "
        "engineering to deliver systems built for long-term operation."
    ),
    story_emphasis="We believe scale is earned through rigour — not through shortcuts alone.",
    story_body_secondary=(
        "Our work spans discovery, architecture, implementation, and ongoing "
        "optimisation. We help leadership teams reduce delivery risk, contain "
        "technical debt, and build platforms that remain fit for purpose as "
        "requirements, traffic, and compliance demands grow."
    ),
    pillars=[
        {
            "icon": "architecture",
            "title": "Architecture-Led Delivery",
            "body": (
                "Engagements begin with scalable system design, explicit "
                "non-functional requirements, and structures that support change "
                "without costly rework."
            ),
        },
        {
            "icon": "hub",
            "title": "Integrated Engineering",
            "body": (
                "Product, platform, and operations are aligned so performance, "
                "security, and maintainability stay consistent across the lifecycle."
            ),
        },
    ],
    operating_principles_heading="Operating principles",
    operating_principles=[
        "Enterprise-grade standards",
        "Architecture-led decisions",
        "Accountable delivery",
    ],
    founder_name="Tushar Hossen",
    founder_role="Founder & CEO",
    founder_org="Implesia IT",
    founder_kicker="Founder's note",
    founder_heading="A letter from leadership",
    founder_lede=(
        "We did not start Implesia IT to ship more software. We started it to "
        "ship software people can trust when the stakes are real."
    ),
    founder_body=(
        "Every platform we build carries someone's revenue, reputation, or "
        "operational continuity. That responsibility is why we refuse shortcuts "
        "that look fast on a timeline and expensive in production. Architecture, "
        "security, and maintainability are not polish—they are the product.\n\n"
        "From Dhaka, we work with teams across markets who expect senior "
        "judgment, clear communication, and delivery that holds up under load, "
        "audit, and change. My commitment is simple: we stay close to the work, "
        "we tell the truth about trade-offs, and we measure success by systems "
        "that still perform years after launch—not by demos that impress for a day."
    ),
    founder_close=(
        "If you are building something that must not fail quietly, I would be glad to talk."
    ),
    founder_signoff="— Tushar",
    founder_location="Dhaka, Bangladesh",
    founder_cta_label="Speak with leadership",
    founder_highlights=[
        {"label": "Focus", "value": "Trustworthy delivery"},
        {"label": "Based", "value": "Dhaka · Global clients"},
        {"label": "Standard", "value": "Senior-led engineering"},
    ],
    purpose_kicker="Purpose & Direction",
    purpose_heading="Mission & Vision",
    purpose_body=(
        "The strategic commitments that guide how we architect, deliver, and "
        "support software for organisations where reliability is a business "
        "requirement."
    ),
    commitments=[
        {
            "icon": "flag",
            "kicker": "Mission",
            "timing": "Today",
            "title": "Deliver production-grade platforms built for continuous operation.",
            "body": (
                "We partner with enterprises and growth-stage organisations that "
                "cannot afford downtime, data compromise, or uncontrolled technical "
                "debt. Our teams apply architecture-first engineering, disciplined "
                "delivery practices, and operational readiness from day one—so "
                "systems perform under real-world load, audit, and change."
            ),
        },
        {
            "icon": "visibility",
            "kicker": "Vision",
            "timing": "Tomorrow",
            "title": "Set the standard for dependable software at enterprise scale.",
            "body": (
                "We aim to show that security, observability, and maintainability "
                "are compatible with delivery speed—not trade-offs. By raising the "
                "bar for how modern platforms are built and run, we help clients "
                "compete with confidence as complexity, regulation, and demand "
                "increase."
            ),
        },
    ],
    tenets_kicker="Operating Principles",
    tenets_heading="Core Tenets in practice",
    tenets_body=(
        "The engineering and delivery standards we apply across every "
        "engagement—from initial discovery through long-term production support."
    ),
    tenets=[
        {
            "icon": "bolt",
            "kicker": "Evidence-led change",
            "title": "Innovation",
            "body": (
                "Technology decisions are assessed against business outcomes, "
                "total cost of ownership, and operational risk. We favour proven "
                "approaches by default and introduce new capabilities only when "
                "the value case is clear."
            ),
        },
        {
            "icon": "target",
            "kicker": "Defined acceptance",
            "title": "Precision",
            "body": (
                "Functional scope, non-functional requirements, and success "
                "metrics are agreed before development begins and validated "
                "throughout delivery, testing, and release."
            ),
        },
        {
            "icon": "verified_user",
            "kicker": "Operational integrity",
            "title": "Reliability",
            "body": (
                "Systems are built for observability, incident response, and "
                "controlled deployment—so availability and performance hold as "
                "workloads, integrations, and compliance requirements evolve."
            ),
        },
        {
            "icon": "trending_up",
            "kicker": "Scalable architecture",
            "title": "Growth",
            "body": (
                "We design platforms to expand with the organisation—supporting "
                "increased demand, new markets, and additional teams without "
                "disruptive re-architecture or unmanaged technical debt."
            ),
        },
    ],
    stability_kicker="Engineering Philosophy",
    stability_heading="Why Stability Matters",
    stability_body=(
        "For organisations running business-critical software, stability is not "
        "a nice-to-have—it is a commercial requirement. These three foundations "
        "shape how we architect, secure, and scale every platform."
    ),
    stability_quote_kicker="Stability in practice",
    stability_quote=(
        "Reliable systems are the result of deliberate architecture, disciplined "
        "delivery, and operational readiness—not luck on launch day."
    ),
    foundations=[
        {
            "icon": "timeline",
            "kicker": "Sustainable architecture",
            "title": "Long-term Lifecycle",
            "body": (
                "Software must remain operable and adaptable as regulations, "
                "product scope, and infrastructure evolve. We prioritise modular "
                "design, clear ownership boundaries, and controlled change over "
                "quick fixes that compound technical debt."
            ),
        },
        {
            "icon": "shield_lock",
            "kicker": "Defence in depth",
            "title": "Security by Design",
            "body": (
                "Security controls are embedded across identity, data, "
                "infrastructure, and release pipelines—not bolted on before "
                "go-live. This reduces exposure, simplifies audit, and supports "
                "compliance without slowing delivery."
            ),
        },
        {
            "icon": "speed",
            "kicker": "Capacity by design",
            "title": "Scalable Performance",
            "body": (
                "Throughput, latency, and fault tolerance are specified upfront "
                "and validated under load. Platforms can absorb growth in traffic, "
                "data volume, and integrations without unplanned re-architecture "
                "or service degradation."
            ),
        },
    ],
    culture_kicker="People & Ways of Working",
    culture_heading="Our Culture",
    culture_body=(
        "Implesia IT operates as a senior engineering organisation. Ownership, "
        "technical discipline, and direct communication define how we work—"
        "and the standard of delivery our clients expect."
    ),
    culture_items=[
        {
            "icon": "groups",
            "title": "Accountable ownership",
            "body": (
                "Every engagement has clear accountability—from architecture and "
                "implementation through production operations and stakeholder "
                "communication."
            ),
        },
        {
            "icon": "workspace_premium",
            "title": "Engineering standards",
            "body": (
                "Peer review, shared practices, and continuous professional "
                "development ensure consistent quality across teams and projects."
            ),
        },
        {
            "icon": "balance",
            "title": "Disciplined delivery",
            "body": (
                "Priorities, timelines, and dependencies are managed with "
                "intent—protecting quality as scope and organisational demands "
                "evolve."
            ),
        },
    ],
    culture_cta_label="Join the Team",
    cta_heading="Ready to build?",
    cta_body="Tell us about your next software project.",
    cta_highlights=["Free discovery call. Response within one business day."],
    cta_primary_label="Start a project",
    cta_secondary_label="View services",
    seo_title="About Us | Implesia IT",
    seo_description=(
        "Implesia IT is a software engineering partner for organisations that "
        "treat uptime, security, and maintainability as business priorities."
    ),
)


async def main() -> None:
    async with SessionLocal() as db:
        await about_service.upsert_page(db, PAGE.model_dump(mode="json"))
    print("About-us page upserted.")


if __name__ == "__main__":
    asyncio.run(main())
