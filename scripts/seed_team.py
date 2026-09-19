"""Upsert the public Implesia /team page and members.

Usage:
    python -m scripts.seed_team
"""

import asyncio

from app.core.exceptions import NotFoundError
from app.db.session import SessionLocal
from app.schemas.team import TeamMemberCreate, TeamMemberUpdate, TeamPageBase
from app.services import team_service

PAGE = TeamPageBase(
    slug="team",
    hero_kicker="Our Team",
    hero_heading="Senior engineers. Accountable delivery.",
    hero_body=(
        "Implesia IT is built around experienced practitioners—not layers of "
        "handoffs. Our teams integrate directly with yours, bringing architecture "
        "discipline, transparent communication, and production-grade standards "
        "to every engagement."
    ),
    hero_metrics=[
        {"value": "35+", "label": "Engineers & Designers"},
        {"value": "6", "label": "Practice Areas"},
        {"value": "12+", "label": "Years Avg. Experience"},
        {"value": "45+", "label": "Clients Served"},
    ],
    hero_highlights=["Senior-Led Squads", "Cross-Functional Pods", "Global Client Delivery"],
    members_kicker="Leadership",
    members_heading="The people behind delivery.",
    members_body=(
        "Our leadership team combines deep technical expertise with accountable "
        "client delivery—setting standards, mentoring engineers, and staying "
        "close to the work."
    ),
    practices_kicker="Practice Areas",
    practices_heading="Disciplines we deploy on every project.",
    practices_body=(
        "Six focused capabilities—each led by senior practitioners and aligned "
        "to the same engineering standards, delivery rhythm, and quality bar."
    ),
    practices_highlights=[
        "Senior-led pods",
        "Shared engineering standards",
        "Production-first mindset",
    ],
    practices=[
        {
            "number": "01",
            "icon": "dns",
            "kicker": "Build & scale",
            "title": "Platform Engineering",
            "body": (
                "Full-stack web platforms, API layers, and data architecture built "
                "for reliability, security, and long-term maintainability."
            ),
            "skills": ["Next.js", "Node.js", "PostgreSQL"],
        },
        {
            "number": "02",
            "icon": "palette",
            "kicker": "Experience design",
            "title": "Product Design",
            "body": (
                "Research-led UX, design systems, and developer-ready prototypes "
                "that align stakeholders and reduce delivery rework."
            ),
            "skills": ["Figma", "Design Tokens", "Accessibility"],
        },
        {
            "number": "03",
            "icon": "cloud_sync",
            "kicker": "Cloud operations",
            "title": "DevOps & Quality",
            "body": (
                "CI/CD, infrastructure as code, automated testing, and "
                "observability—so releases stay predictable and recoverable."
            ),
            "skills": ["AWS", "Docker", "Monitoring"],
        },
        {
            "number": "04",
            "icon": "psychology",
            "kicker": "Intelligent systems",
            "title": "AI & Automation",
            "body": (
                "LLM integrations, intelligent workflows, and process automation "
                "that remove manual bottlenecks without sacrificing control."
            ),
            "skills": ["LLM APIs", "RAG", "Workflow Automation"],
        },
        {
            "number": "05",
            "icon": "smartphone",
            "kicker": "Mobile products",
            "title": "Mobile Engineering",
            "body": (
                "Cross-platform and native mobile applications with strong "
                "performance, offline resilience, and secure data handling."
            ),
            "skills": ["React Native", "iOS", "Android"],
        },
        {
            "number": "06",
            "icon": "handshake",
            "kicker": "Delivery leadership",
            "title": "Client Delivery",
            "body": (
                "Sprint planning, scope governance, and stakeholder "
                "communication—keeping timelines, quality, and expectations aligned."
            ),
            "skills": ["Agile", "Scrum", "Stakeholder Mgmt"],
        },
    ],
    principles_kicker="How We Work",
    principles_heading="Principles that define us.",
    principles_body=(
        "The standards every Implesia team member is expected to uphold—"
        "regardless of role, client, or project phase."
    ),
    principles=[
        {
            "icon": "engineering",
            "title": "Technical Ownership",
            "body": (
                "Engineers own outcomes—not tickets. Every team member is "
                "accountable for quality, performance, and maintainability of "
                "what they ship."
            ),
        },
        {
            "icon": "forum",
            "title": "Direct Communication",
            "body": (
                "No unnecessary layers. Clients work directly with the people "
                "doing the work—clear updates, honest timelines, and transparent "
                "trade-offs."
            ),
        },
        {
            "icon": "school",
            "title": "Continuous Growth",
            "body": (
                "Peer review, knowledge sharing, and structured learning keep "
                "our teams at the forefront of modern engineering practice."
            ),
        },
    ],
    principles_cta_label="Learn about our culture",
    principles_cta_secondary="Work With Us",
    meet_heading="Ready to meet your team?",
    meet_body=(
        "Whether you need a dedicated squad or specialist support for a critical "
        "initiative, we'll match you with engineers who fit your stack, culture, "
        "and delivery cadence."
    ),
    meet_highlights=[
        "Free discovery call",
        "Senior-led from day one",
        "Flexible engagement models",
    ],
    meet_cta_label="Book a Consultation",
    cta_heading="Ready to build?",
    cta_body="Tell us about your next software project.",
    cta_highlights=["Free discovery call. Response within one business day."],
    cta_primary_label="Start a project",
    cta_secondary_label="View services",
    seo_title="Team | Implesia IT",
    seo_description=(
        "Senior engineers and accountable delivery. Implesia teams integrate "
        "with yours on architecture, communication, and production standards."
    ),
)

MEMBERS = [
    TeamMemberCreate(
        name="Tushar Hossen",
        slug="tushar-hossen",
        role="Founder and CEO",
        bio=(
            "Leads company vision, client partnerships, and delivery strategy—"
            "ensuring every project aligns with business goals and Implesia's "
            "engineering standards."
        ),
        skills=["Leadership", "Strategy", "Client Delivery"],
        is_featured=True,
        sort_order=10,
    ),
    TeamMemberCreate(
        name="Md Nazrul Islam",
        slug="md-nazrul-islam",
        role="Senior Backend & DevOps",
        bio=(
            "Architects scalable backend systems and cloud infrastructure—"
            "building reliable APIs, deployment pipelines, and production "
            "environments that perform under load."
        ),
        skills=["Backend", "DevOps", "Cloud Infrastructure"],
        sort_order=20,
    ),
    TeamMemberCreate(
        name="Md Rabbi Hossen",
        slug="md-rabbi-hossen",
        role="Senior Full Stack Engineer",
        bio=(
            "Delivers end-to-end web applications across frontend and backend—"
            "translating product requirements into secure, maintainable, "
            "production-ready software."
        ),
        skills=["Full Stack", "Next.js", "TypeScript"],
        sort_order=30,
    ),
    TeamMemberCreate(
        name="Arafat Hossen",
        slug="arafat-hossen",
        role="Senior UI/UX Engineer",
        bio=(
            "Crafts intuitive interfaces and design systems—combining user "
            "research, visual design, and front-end implementation for polished "
            "digital experiences."
        ),
        skills=["UI/UX", "Design Systems", "Figma"],
        sort_order=40,
    ),
]


async def main() -> None:
    created = 0
    updated = 0
    async with SessionLocal() as db:
        await team_service.upsert_page(db, PAGE.model_dump(mode="json"))
        for payload in MEMBERS:
            try:
                existing = await team_service.get_member_by_slug(db, payload.slug or "")
            except NotFoundError:
                await team_service.create_member(db, payload)
                created += 1
                continue
            await team_service.update_member(
                db, existing, TeamMemberUpdate.model_validate(payload.model_dump())
            )
            updated += 1
    print(f"Team page upserted. Members +{created}/~{updated}.")


if __name__ == "__main__":
    asyncio.run(main())
