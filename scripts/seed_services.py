"""Upsert the public Implesia service catalogue.

Usage:
    python -m scripts.seed_services
"""

import asyncio

from app.core.exceptions import NotFoundError
from app.db.session import SessionLocal
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.services import service_service

CATALOGUE: list[ServiceCreate] = [
    ServiceCreate(
        name="Web Platforms",
        slug="web-platforms",
        tagline=(
            "Enterprise-grade web applications engineered for speed, accessibility, "
            "and measurable conversion at scale."
        ),
        description=(
            "We design and build high-performance web platforms that serve as the digital "
            "backbone of modern enterprises. From customer-facing portals to internal "
            "dashboards, every layer is architected for reliability, security, and "
            "long-term maintainability—so your team can ship faster without accumulating "
            "technical debt."
        ),
        category="engineering",
        icon="desktop_windows",
        engagement_status="Available",
        tech_stack=["Next.js", "React", "TypeScript", "Node.js", "PostgreSQL"],
        hero_metrics=[
            {"value": "1.2s", "label": "Avg. Load Time"},
            {"value": "99.9%", "label": "Uptime SLA"},
        ],
        deliver_heading="What we deliver for web platforms",
        deliver_body=(
            "We design and build high-performance web platforms that serve as the digital "
            "backbone of modern enterprises. From customer-facing portals to internal "
            "dashboards, every layer is architected for reliability, security, and "
            "long-term maintainability."
        ),
        capabilities=[
            "Micro-frontend and modular architecture",
            "Server-side rendering and edge optimization",
            "Role-based access and enterprise SSO",
            "Real-time analytics and observability",
            "WCAG-compliant accessibility standards",
        ],
        deliverables_heading="What You Receive",
        deliverables_kicker="Included in every engagement",
        deliverables=[
            "Production-ready web application",
            "Design system and component library",
            "CI/CD pipeline and deployment docs",
            "Performance audit and monitoring setup",
        ],
        process_heading="How we build your web platforms",
        process_body=(
            "A proven four-phase framework designed for clarity, velocity, and "
            "production-grade outcomes."
        ),
        process_steps=[
            {
                "title": "Discovery",
                "description": "Map business goals, user journeys, and technical constraints.",
            },
            {
                "title": "Architecture",
                "description": "Define scalable system design, APIs, and data models.",
            },
            {
                "title": "Engineering",
                "description": "Iterative development with continuous QA and reviews.",
            },
            {
                "title": "Launch",
                "description": "Deploy, monitor, and hand over with full documentation.",
            },
        ],
        outcomes_heading="Outcomes that move the needle",
        outcomes_body=(
            "Enterprise web platforms we build consistently deliver measurable "
            "performance, reliability, and team velocity gains."
        ),
        outcomes_disclaimer=(
            "Results based on aggregated client engagements. Individual outcomes vary "
            "by scope, team, and market conditions."
        ),
        outcomes=[
            {
                "title": "Faster Releases",
                "description": "Average CI/CD cycle time reduction post-launch",
                "value": None,
            },
            {
                "title": "Less Tech Debt",
                "description": "Modular architecture reduces rework over 12 months",
                "value": None,
            },
            {
                "title": "Conversion Lift",
                "description": "Median improvement on optimized user flows",
                "value": None,
            },
        ],
        related_heading="Related services",
        related_slugs=["mobile-apps", "saas-architecture", "ui-ux-design"],
        faqs_heading="Still have questions?",
        faqs_body="Our senior architects respond within 24 hours on business days.",
        faqs=[
            {
                "question": "How long does a typical web platform project take?",
                "answer": (
                    "Most enterprise web platforms take 12–20 weeks depending on scope. "
                    "We start with a 2-week discovery sprint to define architecture, "
                    "milestones, and a realistic timeline before development begins."
                ),
            },
            {
                "question": "Do you work with our existing design or engineering team?",
                "answer": (
                    "Yes. We embed with your team, share the same backlog, and keep "
                    "architecture decisions in a written brief so handover stays clean."
                ),
            },
            {
                "question": "What tech stack do you recommend for new web platforms?",
                "answer": (
                    "For most new products we recommend Next.js, TypeScript, and a "
                    "FastAPI or Node API on PostgreSQL. We adjust the stack to your "
                    "team and hosting constraints."
                ),
            },
            {
                "question": "Do you provide post-launch support and maintenance?",
                "answer": (
                    "Yes. Every engagement includes a written handover, and we offer "
                    "a maintenance retainer for monitoring, fixes, and small iterations."
                ),
            },
        ],
        cta_heading="Ready to architect your digital future?",
        cta_body=(
            "Schedule a confidential strategy session with our senior architects to "
            "discuss your project requirements and roadmap."
        ),
        cta_highlights=["Free Strategy Call", "NDA Available", "Senior Engineers"],
        seo_title="Web Platforms | Implesia IT",
        seo_description=(
            "Enterprise-grade web applications engineered for speed, accessibility, "
            "and measurable conversion at scale."
        ),
        sort_order=10,
    ),
    ServiceCreate(
        name="Mobile Applications",
        slug="mobile-apps",
        tagline=(
            "Native-quality experiences across iOS and Android—fast, intuitive, "
            "and built to meet global app store standards."
        ),
        description=(
            "Your users expect mobile experiences that feel instant and effortless. "
            "We build native and cross-platform applications with polished UX, offline "
            "resilience, and secure backend integration—engineered to pass app store "
            "review and perform under real-world network conditions."
        ),
        category="engineering",
        icon="phone_iphone",
        engagement_status="Available",
        tech_stack=["Flutter", "Swift", "Kotlin"],
        hero_metrics=[
            {"value": "4.8★", "label": "Avg. Store Rating"},
            {"value": "60fps", "label": "Smooth Animations"},
        ],
        deliver_heading="What we deliver for mobile applications",
        deliver_body=(
            "Your users expect mobile experiences that feel instant and effortless. "
            "We build native and cross-platform applications with polished UX, offline "
            "resilience, and secure backend integration."
        ),
        capabilities=[
            "Native iOS and Android when platform depth matters",
            "Flutter or React Native when a shared codebase is the right trade-off",
            "Offline-first data and resilient networking",
            "Secure API integration and session handling",
            "App store review and rollout support",
        ],
        deliverables_heading="What You Receive",
        deliverables_kicker="Included in every engagement",
        deliverables=[
            "Published mobile application",
            "Backend API integration",
            "Analytics and crash reporting setup",
            "App store assets and listing copy",
        ],
        process_heading="How we ship your mobile app",
        process_body="Prototype, sprint, polish, then a controlled store release.",
        process_steps=[
            {
                "title": "UX Prototype",
                "description": "Interactive flows validated before a single line of code.",
            },
            {
                "title": "Sprint Build",
                "description": "Two-week cycles with TestFlight and internal builds.",
            },
            {
                "title": "QA & Polish",
                "description": "Device matrix testing, performance tuning, accessibility.",
            },
            {
                "title": "Release",
                "description": "Store submission, rollout strategy, and post-launch support.",
            },
        ],
        outcomes_disclaimer=(
            "Results based on aggregated client engagements. Individual outcomes vary "
            "by scope, team, and market conditions."
        ),
        related_slugs=["web-platforms", "saas-architecture", "ui-ux-design"],
        faqs=[
            {
                "question": "Do you build native apps or cross-platform?",
                "answer": (
                    "Both. We choose native (Swift/Kotlin) when performance and "
                    "platform-specific features are critical, and Flutter or React Native "
                    "when speed-to-market and a shared codebase matter most."
                ),
            },
            {
                "question": "Do you handle App Store and Play Store submission?",
                "answer": (
                    "Yes. Listing copy, assets, review responses, and a staged rollout "
                    "are part of the release phase."
                ),
            },
        ],
        cta_body=(
            "Schedule a confidential strategy session with our senior architects to "
            "discuss your project requirements and roadmap."
        ),
        seo_title="Mobile Applications | Implesia IT",
        seo_description=(
            "Native-quality experiences across iOS and Android—fast, intuitive, and "
            "built to meet global app store standards."
        ),
        sort_order=20,
    ),
    ServiceCreate(
        name="SaaS Architecture",
        slug="saas-architecture",
        tagline="Cloud-native backends that scale from MVP to enterprise demand.",
        description=(
            "Cloud-native platforms built for reliability and elasticity — from a "
            "validated MVP through sustained enterprise demand."
        ),
        category="engineering",
        icon="cloud_sync",
        tech_stack=["FastAPI", "PostgreSQL", "Redis", "Docker"],
        deliverables=["API-first backend", "Multi-tenant foundation", "Observability basics"],
        process_steps=["Discovery", "Architecture", "Build", "Scale"],
        sort_order=30,
    ),
    ServiceCreate(
        name="UI/UX Design",
        slug="ui-ux-design",
        tagline="Research-led interfaces and developer-ready design systems.",
        description=(
            "Research-led UX, design systems, and high-fidelity prototypes that "
            "align stakeholders and reduce delivery rework."
        ),
        category="design",
        icon="palette",
        tech_stack=["Figma", "Design Tokens"],
        deliverables=["User flows", "High-fidelity UI", "Handoff kit"],
        process_steps=["Research", "Wireframes", "UI", "Handoff"],
        sort_order=40,
    ),
    ServiceCreate(
        name="Business Automation",
        slug="business-automation",
        tagline="Workflows that remove manual bottlenecks without losing control.",
        description=(
            "Intelligent workflows and process automation that cut repetitive work "
            "while keeping approvals and audit trails in place."
        ),
        category="operations",
        icon="precision_manufacturing",
        tech_stack=["Python", "Webhooks", "PostgreSQL"],
        deliverables=["Mapped workflows", "Automation scripts", "Admin controls"],
        process_steps=["Audit", "Design", "Automate", "Handover"],
        sort_order=50,
    ),
    ServiceCreate(
        name="E-commerce",
        slug="e-commerce",
        tagline="Catalog, cart, and local payments with a staff dashboard.",
        description=(
            "A focused storefront to list products, take orders, and accept common "
            "Bangladesh payment methods — with an admin dashboard to run the shop."
        ),
        category="commerce",
        icon="storefront",
        tech_stack=["Next.js", "PostgreSQL", "SSLCommerz"],
        deliverables=["Storefront", "Cart and checkout", "Order admin"],
        process_steps=["Catalogue", "Build", "Payments", "Launch"],
        sort_order=60,
    ),
    ServiceCreate(
        name="Cloud Hosting & Solutions",
        slug="cloud-hosting-solutions",
        tagline="Reliable hosting, SSL, and environments you can operate.",
        description=(
            "Cloud hosting, environment setup, and operational basics so your product "
            "stays online without a dedicated DevOps hire on day one."
        ),
        category="infrastructure",
        icon="cloud",
        tech_stack=["Docker", "Nginx", "Let's Encrypt"],
        deliverables=["Production host", "Staging environment", "Backup routine"],
        process_steps=["Plan", "Provision", "Deploy", "Handover"],
        sort_order=70,
    ),
    ServiceCreate(
        name="AI Integrations",
        slug="ai-integrations",
        tagline="LLM features with guardrails, not unbounded chat widgets.",
        description=(
            "LLM integrations and RAG-style assistants that sit inside your product "
            "with evaluation, logging, and a kill switch."
        ),
        category="ai",
        icon="psychology",
        tech_stack=["OpenAI-compatible APIs", "PostgreSQL"],
        deliverables=["Scoped AI feature", "Prompt and eval notes", "Usage logging"],
        process_steps=["Use-case", "Prototype", "Guardrails", "Launch"],
        sort_order=80,
    ),
    ServiceCreate(
        name="ERP Systems",
        slug="erp-systems",
        tagline="Operations software shaped around how your team already works.",
        description=(
            "Custom ERP modules for inventory, finance, and operations — scoped for "
            "Bangladesh SMEs rather than a generic enterprise suite."
        ),
        category="operations",
        icon="inventory_2",
        tech_stack=["FastAPI", "PostgreSQL", "Next.js"],
        deliverables=["Role-based modules", "Reports", "Admin dashboard"],
        process_steps=["Process map", "Build", "Pilot", "Rollout"],
        sort_order=90,
    ),
    ServiceCreate(
        name="CRM Systems",
        slug="crm-systems",
        tagline="Leads, pipeline, and follow-up in one place.",
        description=(
            "Customer relationship platforms that track leads, pipelines, and "
            "retention — built around your sales process."
        ),
        category="operations",
        icon="handshake",
        tech_stack=["FastAPI", "PostgreSQL", "Next.js"],
        deliverables=["Lead pipeline", "Follow-up reminders", "Basic reports"],
        process_steps=["Sales map", "Build", "Pilot", "Rollout"],
        sort_order=100,
    ),
    ServiceCreate(
        name="LMS",
        slug="lms",
        tagline="Courses, enrollment, and progress tracking at a modest scale.",
        description=(
            "Learning platforms for training providers and institutes — publish "
            "courses, enroll students, and gate content from an admin dashboard."
        ),
        category="education",
        icon="school",
        tech_stack=["Next.js", "FastAPI", "PostgreSQL"],
        deliverables=["Learner portal", "Instructor dashboard", "Enrollment control"],
        process_steps=["Curriculum", "Platform", "Content", "Launch"],
        sort_order=110,
    ),
    ServiceCreate(
        name="Hospital Management",
        slug="hospital-management",
        tagline="Starter clinic operations: patients, appointments, billing.",
        description=(
            "A starter HMS for outpatient operations — patient records, appointments, "
            "billing, and role-based dashboards for Bangladesh clinics."
        ),
        category="healthcare",
        icon="local_hospital",
        tech_stack=["Next.js", "FastAPI", "PostgreSQL"],
        deliverables=["Patient registry", "OPD appointments", "Billing dashboard"],
        process_steps=["Scope", "Build", "Pilot", "Handover"],
        sort_order=120,
    ),
    ServiceCreate(
        name="Custom Solutions",
        slug="custom-solutions",
        tagline="When the brief does not fit a packaged product.",
        description=(
            "Bespoke software scoped after a discovery sprint — for products that "
            "need senior engineering judgment rather than a fixed package."
        ),
        category="engineering",
        icon="build_circle",
        tech_stack=["FastAPI", "Next.js", "PostgreSQL"],
        deliverables=["Discovery brief", "Architecture note", "Phased build"],
        process_steps=["Discovery", "Design", "Build", "Scale"],
        sort_order=130,
    ),
    ServiceCreate(
        name="Digital Marketing",
        slug="digital-marketing",
        tagline="Campaign setup and measurement, not an open-ended retainer.",
        description=(
            "Focused digital marketing engagements — landing pages, tracking, and "
            "channel setup with a written scope."
        ),
        category="marketing",
        icon="campaign",
        tech_stack=["Analytics", "Meta Ads", "Google Ads"],
        deliverables=["Tracking plan", "Landing page support", "Channel setup"],
        process_steps=["Goals", "Setup", "Launch", "Review"],
        sort_order=140,
    ),
    ServiceCreate(
        name="Content Writing",
        slug="content-writing",
        tagline="Site and campaign copy written to a brief.",
        description=(
            "Website and campaign copy — service pages, landing sections, and "
            "supporting articles against a written brief."
        ),
        category="marketing",
        icon="edit_note",
        tech_stack=["Editorial calendar"],
        deliverables=["Page copy", "SEO basics", "Revision rounds"],
        process_steps=["Brief", "Draft", "Revise", "Publish"],
        sort_order=150,
    ),
    ServiceCreate(
        name="Video Editing",
        slug="video-editing",
        tagline="Promos, explainers, and social cuts from your footage.",
        description=(
            "Professional video editing for promos, social content, explainers, and brand films."
        ),
        category="media",
        icon="movie",
        tech_stack=["Premiere", "After Effects"],
        deliverables=["Edited cut", "Captions", "Export pack"],
        process_steps=["Brief", "Edit", "Review", "Deliver"],
        sort_order=160,
    ),
]


def _with_page_defaults(item: ServiceCreate) -> ServiceCreate:
    """Fill page blocks so every catalogue item can render like /services/web-platforms."""
    data = item.model_dump()
    name = data["name"]
    data.setdefault("deliverables_heading", "What You Receive")
    data.setdefault("deliverables_kicker", "Included in every engagement")
    if not data.get("deliver_body"):
        data["deliver_body"] = data["description"]
    if not data.get("capabilities"):
        data["capabilities"] = list(data.get("deliverables") or [])
    if not data.get("process_body"):
        data["process_body"] = f"A clear four-phase path for {name.lower()}."
    if not data.get("outcomes_disclaimer"):
        data["outcomes_disclaimer"] = (
            "Results based on aggregated client engagements. Individual outcomes vary "
            "by scope, team, and market conditions."
        )
    if not data.get("faqs"):
        data["faqs"] = [
            {
                "question": f"How do we start a {name} project?",
                "answer": (
                    "We begin with a short discovery call, then a written scope, "
                    "milestones, and a commercial path before engineering starts."
                ),
            },
            {
                "question": "Do you work with an existing team?",
                "answer": (
                    "Yes. We embed with your designers and engineers, share one backlog, "
                    "and keep architecture decisions in a written brief."
                ),
            },
        ]
    if not data.get("faqs_body"):
        data["faqs_body"] = "Our senior architects respond within 24 hours on business days."
    if not data.get("cta_body"):
        data["cta_body"] = (
            "Schedule a confidential strategy session with our senior architects to "
            "discuss your project requirements and roadmap."
        )
    if not data.get("cta_highlights"):
        data["cta_highlights"] = ["Free Strategy Call", "NDA Available", "Senior Engineers"]
    if not data.get("seo_title"):
        data["seo_title"] = f"{name} | Implesia IT"
    if not data.get("seo_description"):
        data["seo_description"] = data["tagline"][:200]
    return ServiceCreate.model_validate(data)


async def main() -> None:
    created = 0
    updated = 0
    async with SessionLocal() as db:
        for raw in CATALOGUE:
            payload = _with_page_defaults(raw)
            slug = payload.slug or ""
            try:
                existing = await service_service.get_by_slug(db, slug)
            except NotFoundError:
                await service_service.create_service(db, payload)
                created += 1
                continue
            await service_service.update_service(
                db, existing, ServiceUpdate.model_validate(payload.model_dump())
            )
            updated += 1
    print(f"Seeded {created} new services, updated {updated}.")


if __name__ == "__main__":
    asyncio.run(main())
