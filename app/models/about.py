from __future__ import annotations

from typing import Any

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AboutPage(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Chrome for /about-us: hero, story, founder, mission, tenets, culture."""

    __tablename__ = "about_pages"

    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    hero_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    hero_heading: Mapped[str] = mapped_column(String(200), nullable=False)
    hero_body: Mapped[str] = mapped_column(Text, nullable=False)
    hero_primary_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    hero_secondary_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    hero_highlights: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    hero_metrics: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    quote_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    quote_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    quote_attribution: Mapped[str] = mapped_column(String(160), nullable=False, default="")

    story_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    story_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    story_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    story_emphasis: Mapped[str] = mapped_column(String(280), nullable=False, default="")
    story_body_secondary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    pillars: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    operating_principles_heading: Mapped[str] = mapped_column(
        String(120), nullable=False, default=""
    )
    operating_principles: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    founder_name: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    founder_role: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    founder_org: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    founder_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    founder_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    founder_lede: Mapped[str] = mapped_column(Text, nullable=False, default="")
    founder_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    founder_close: Mapped[str] = mapped_column(Text, nullable=False, default="")
    founder_signoff: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    founder_location: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    founder_cta_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    founder_highlights: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=list, nullable=False
    )

    purpose_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    purpose_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    purpose_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    commitments: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    tenets_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    tenets_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    tenets_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    tenets: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    stability_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    stability_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    stability_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    stability_quote_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    stability_quote: Mapped[str] = mapped_column(Text, nullable=False, default="")
    foundations: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    culture_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    culture_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    culture_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    culture_items: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    culture_cta_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")

    cta_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    cta_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    cta_highlights: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    cta_primary_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    cta_secondary_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")

    seo_title: Mapped[str | None] = mapped_column(String(80))
    seo_description: Mapped[str | None] = mapped_column(String(200))
    internal_notes: Mapped[str | None] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"<AboutPage {self.slug}>"
