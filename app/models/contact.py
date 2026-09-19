from __future__ import annotations

from typing import Any

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ContactPage(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Chrome for /contact: hero, channels, hours, form copy, process, FAQs."""

    __tablename__ = "contact_pages"

    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    hero_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    hero_heading: Mapped[str] = mapped_column(String(200), nullable=False)
    hero_body: Mapped[str] = mapped_column(Text, nullable=False)
    hero_highlights: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    hero_metrics: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    form_intro: Mapped[str] = mapped_column(Text, nullable=False, default="")

    channels_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    channels_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    channels_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    channels: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    office_hours_heading: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    office_hours: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    office_hours_note: Mapped[str] = mapped_column(Text, nullable=False, default="")

    form_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    form_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    form_privacy: Mapped[str] = mapped_column(Text, nullable=False, default="")
    form_submit_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    form_action: Mapped[str] = mapped_column(String(120), nullable=False, default="/api/v1/leads")
    service_options: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=list, nullable=False
    )
    timeline_options: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=list, nullable=False
    )

    process_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    process_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    process_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    process_steps: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    process_quote: Mapped[str] = mapped_column(Text, nullable=False, default="")

    faqs_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    faqs_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    faqs_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    faq_highlights: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    faqs: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    faqs_cta_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    faqs_cta_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    agreement_note: Mapped[str] = mapped_column(Text, nullable=False, default="")
    agreement_kicker: Mapped[str] = mapped_column(String(160), nullable=False, default="")

    cta_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    cta_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    cta_highlights: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    cta_primary_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    cta_secondary_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")

    seo_title: Mapped[str | None] = mapped_column(String(80))
    seo_description: Mapped[str | None] = mapped_column(String(200))
    internal_notes: Mapped[str | None] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"<ContactPage {self.slug}>"
