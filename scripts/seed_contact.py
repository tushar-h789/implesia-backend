"""Upsert the public Implesia /contact page.

Usage:
    python -m scripts.seed_contact
"""

import asyncio

from app.db.session import SessionLocal
from app.schemas.contact import ContactPageBase
from app.services import contact_service

PAGE = ContactPageBase(
    slug="contact",
    hero_kicker="New Enquiries",
    hero_heading="Tell us about your project.",
    hero_body=(
        "Whether you have a defined brief or an early-stage idea, our team will "
        "assess your requirements and respond with a clear path forward — typically "
        "within one business day."
    ),
    hero_highlights=[
        "< 24 hr response",
        "Confidentiality guaranteed",
        "No-commitment discovery call",
    ],
    hero_metrics=[
        {"value": "< 24 hr", "label": "Guaranteed response SLA"},
        {"value": "100%", "label": "Confidential by default"},
        {"value": "No cost", "label": "Initial discovery session"},
    ],
    form_intro=(
        "Submit your brief using the form below. Our team will assess your "
        "requirements and respond with a structured, tailored assessment within "
        "one business day."
    ),
    channels_kicker="Contact channels",
    channels_heading="Speak with our team",
    channels_body=(
        "Prefer to connect directly? Choose the channel that suits you and a "
        "member of our team will respond promptly."
    ),
    channels=[
        {
            "icon": "mail",
            "title": "Business email",
            "value": "implesiaitltd@gmail.com",
            "body": "Guaranteed reply within one business day",
            "href": "mailto:implesiaitltd@gmail.com",
        },
        {
            "icon": "chat",
            "title": "WhatsApp",
            "value": "+88 01516527932",
            "body": "Direct line to our business development team",
            "href": "https://wa.me/8801516527932",
        },
        {
            "icon": "location_on",
            "title": "Headquarters",
            "value": "Mirpur 10, Dhaka",
            "body": "Bangladesh — serving clients globally",
            "href": "https://maps.google.com/?q=Mirpur+10,+Dhaka",
        },
    ],
    office_hours_heading="Office hours",
    office_hours=[
        {"days": "Sunday – Thursday", "hours": "9:00 AM – 7:00 PM"},
        {"days": "Friday – Saturday", "hours": "Closed"},
    ],
    office_hours_note=(
        "All times in UTC+6 (Dhaka). Remote availability for international clients may vary."
    ),
    form_heading="Submit your project brief",
    form_body="Required fields are marked with an asterisk (*).",
    form_privacy=(
        "All information submitted is treated with strict confidence and used solely "
        "to assess and respond to your enquiry. We do not share, sell, or distribute "
        "your data to any third party."
    ),
    form_submit_label="Send enquiry",
    form_action="/api/v1/leads",
    service_options=[
        {"value": "web-platforms", "label": "Web Platforms"},
        {"value": "mobile-applications", "label": "Mobile Applications"},
        {"value": "saas-architecture", "label": "SaaS Architecture"},
        {"value": "ui-ux-design", "label": "UI/UX Design"},
        {"value": "business-automation", "label": "Business Automation"},
        {"value": "e-commerce", "label": "E-commerce"},
    ],
    timeline_options=[
        {"value": "asap", "label": "ASAP — within 2 weeks"},
        {"value": "1-3-months", "label": "1–3 months"},
        {"value": "3-6-months", "label": "3–6 months"},
        {"value": "exploring", "label": "Still exploring options"},
    ],
    process_kicker="Our process",
    process_heading="From first contact to project launch",
    process_body=(
        "A defined, four-stage engagement process that removes ambiguity — so every "
        "stakeholder knows exactly what to expect and when."
    ),
    process_steps=[
        {
            "number": "01",
            "icon": "mark_email_read",
            "timing": "Day 0",
            "title": "Enquiry reviewed",
            "body": (
                "Every submission is assessed by a senior team member. We qualify "
                "scope, identify the right technical lead, and prepare an informed "
                "initial response."
            ),
        },
        {
            "number": "02",
            "icon": "record_voice_over",
            "timing": "Day 1–2",
            "title": "Discovery session",
            "body": (
                "A structured 30-minute call covering your business objectives, "
                "existing infrastructure, constraints, and definition of success. "
                "No sales pitch — just focused listening."
            ),
        },
        {
            "number": "03",
            "icon": "contract",
            "timing": "Day 3–5",
            "title": "Scoped proposal",
            "body": (
                "A written proposal covering solution architecture, phased delivery "
                "timeline, team composition, acceptance criteria, and a transparent "
                "cost breakdown."
            ),
        },
        {
            "number": "04",
            "icon": "rocket_launch",
            "timing": "Week 1",
            "title": "Onboarding & kickoff",
            "body": (
                "Upon agreement, your dedicated squad begins a structured onboarding "
                "sprint — provisioning environments, establishing delivery cadence, "
                "and aligning on milestones."
            ),
        },
    ],
    process_quote=(
        "Every engagement at Implesia IT is governed by defined scope, written "
        "commitments, and full transparency — from the first message to production "
        "handover."
    ),
    faqs_kicker="Common questions",
    faqs_heading="Before you reach out",
    faqs_body=(
        "Answers to the questions we hear most often from prospective clients, "
        "covering scope, process, confidentiality, and what to expect."
    ),
    faq_highlights=[
        "Remote-first",
        "International clients",
        "NDA available",
        "Fixed-scope & retainer",
    ],
    faqs=[
        {
            "question": "Do you work with clients outside Bangladesh?",
            "answer": (
                "Yes. Our client base is predominantly international. We operate "
                "remotely across UK, Europe, North America, and the Middle East, "
                "aligning to client timezones for meetings and maintaining async "
                "communication via structured project documentation throughout."
            ),
        },
        {
            "question": "What should I prepare before the discovery session?",
            "answer": (
                "A rough description of the problem you are solving, any constraints "
                "(budget range, deadline, existing infrastructure), and a sense of "
                "what success looks like after 6–12 months. You do not need a formal "
                "specification — the discovery session is specifically designed to "
                "help shape one."
            ),
        },
        {
            "question": "How do you handle confidentiality and IP ownership?",
            "answer": (
                "An NDA is available on request prior to any technical discussion. "
                "All intellectual property developed during an engagement is assigned "
                "in full to the client upon final settlement. We operate under clear "
                "contractual terms and do not reuse client-specific work in any other "
                "project."
            ),
        },
        {
            "question": "What is your minimum engagement size?",
            "answer": (
                "We take on projects from £10,000 upwards for fixed-scope delivery, "
                "and ongoing retainer arrangements from £3,500 per month. For "
                "early-stage teams with strong fit, we are open to structured "
                "milestone agreements."
            ),
        },
        {
            "question": "Can we begin with a small discovery or pilot phase?",
            "answer": (
                "Absolutely. A scoped discovery sprint — typically 1–2 weeks — is "
                "often the most effective way to validate technical approach, assess "
                "team compatibility, and produce a delivery roadmap before committing "
                "to a full build."
            ),
        },
        {
            "question": "What happens if our requirements change mid-project?",
            "answer": (
                "All engagements are governed by a formal change-control process. "
                "Scope changes are documented, assessed for impact on timeline and "
                "cost, and agreed in writing before implementation. We prioritise "
                "predictability and avoid scope drift."
            ),
        },
    ],
    faqs_cta_heading="Still have questions?",
    faqs_cta_body=(
        "If your question isn't covered here, reach us directly — we respond to "
        "all messages within one business day."
    ),
    agreement_note=(
        "All client engagements are covered by a formal service agreement with "
        "clearly defined scope, deliverables, and escalation paths."
    ),
    agreement_kicker="No ambiguity. No hidden terms.",
    cta_heading="Ready to build?",
    cta_body="Tell us about your next software project.",
    cta_highlights=["Free discovery call. Response within one business day."],
    cta_primary_label="Start a project",
    cta_secondary_label="View services",
    seo_title="Contact | Implesia IT",
    seo_description=(
        "Tell us about your project. We assess requirements and respond with a "
        "clear path forward — typically within one business day."
    ),
)


async def main() -> None:
    async with SessionLocal() as db:
        await contact_service.upsert_page(db, PAGE.model_dump(mode="json"))
    print("Contact page upserted.")


if __name__ == "__main__":
    asyncio.run(main())
