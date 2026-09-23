from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

if TYPE_CHECKING:
    from app.models.order import Order

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class PricingPage(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Chrome for /pricing: hero, path cards, notes, process, FAQs, CTA, SEO."""

    __tablename__ = "pricing_pages"

    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    hero_heading: Mapped[str] = mapped_column(String(200), nullable=False)
    hero_body: Mapped[str] = mapped_column(Text, nullable=False)
    paths_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    paths_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    paths_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    paths: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    models_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    models_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    models_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    models_currency_note: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    models_disclaimer: Mapped[str] = mapped_column(Text, nullable=False, default="")

    packages_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    packages_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    packages_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    packages_currency_note: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    commercial_terms: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=list, nullable=False
    )
    packages_disclaimer: Mapped[str] = mapped_column(Text, nullable=False, default="")

    process_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    process_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    process_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    process_steps: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    faqs_kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    faqs_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    faqs: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    cta_heading: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    cta_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    cta_highlights: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    cta_primary_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    cta_secondary_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")

    seo_title: Mapped[str | None] = mapped_column(String(80))
    seo_description: Mapped[str | None] = mapped_column(String(200))
    bdt_per_usd: Mapped[int] = mapped_column(Integer, nullable=False, default=123)

    def __repr__(self) -> str:
        return f"<PricingPage {self.slug}>"


class EngagementModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Custom engagement card on /pricing (Discovery, Squad, Fixed-scope)."""

    __tablename__ = "engagement_models"

    name: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    icon: Mapped[str | None] = mapped_column(String(80))
    kicker: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    badge: Mapped[str | None] = mapped_column(String(80))
    price_label: Mapped[str] = mapped_column(String(80), nullable=False)
    price_amount: Mapped[int | None] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    cadence: Mapped[str] = mapped_column(String(20), nullable=False, default="one_time")
    subtitle: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    description: Mapped[str] = mapped_column(Text, nullable=False)
    inclusions: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    ideal_for: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    cta_label: Mapped[str] = mapped_column(String(80), nullable=False, default="Discuss this model")
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    orders: Mapped[list[Order]] = relationship("Order", back_populates="model")

    def __repr__(self) -> str:
        return f"<EngagementModel {self.slug}>"


class PricingPackage(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Fixed-BDT productized package card on /pricing."""

    __tablename__ = "pricing_packages"

    name: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    icon: Mapped[str | None] = mapped_column(String(80))
    tagline: Mapped[str] = mapped_column(String(200), nullable=False)
    badge: Mapped[str | None] = mapped_column(String(80))
    price_label: Mapped[str] = mapped_column(String(80), nullable=False)
    price_amount_bdt: Mapped[int] = mapped_column(Integer, nullable=False)
    timeline_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    bugfix_label: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    audience: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    description: Mapped[str] = mapped_column(Text, nullable=False)
    dashboard_heading: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    dashboard_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    inclusions: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    exclusions: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    cta_label: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    orders: Mapped[list[Order]] = relationship("Order", back_populates="package")

    def __repr__(self) -> str:
        return f"<PricingPackage {self.slug}>"
