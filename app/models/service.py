from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.order import Order

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Service(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Full content model for a public /services/{slug} page."""

    __tablename__ = "services"

    name: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    tagline: Mapped[str] = mapped_column(String(280), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False, default="engineering")
    icon: Mapped[str | None] = mapped_column(String(80))
    engagement_status: Mapped[str] = mapped_column(String(40), nullable=False, default="Available")

    tech_stack: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    hero_metrics: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    deliver_heading: Mapped[str] = mapped_column(
        String(160), nullable=False, default="What we deliver"
    )
    deliver_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    capabilities: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    deliverables_heading: Mapped[str] = mapped_column(
        String(160), nullable=False, default="What You Receive"
    )
    deliverables_kicker: Mapped[str] = mapped_column(
        String(160), nullable=False, default="Included in every engagement"
    )
    deliverables: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    process_heading: Mapped[str] = mapped_column(String(160), nullable=False, default="How we work")
    process_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    process_steps: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    outcomes_heading: Mapped[str] = mapped_column(
        String(160), nullable=False, default="Before → After"
    )
    outcomes_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    outcomes_disclaimer: Mapped[str] = mapped_column(String(400), nullable=False, default="")
    outcomes: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    related_heading: Mapped[str] = mapped_column(
        String(160), nullable=False, default="Related services"
    )
    related_slugs: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    faqs_heading: Mapped[str] = mapped_column(
        String(160), nullable=False, default="Still have questions?"
    )
    faqs_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    faqs: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    cta_heading: Mapped[str] = mapped_column(
        String(160), nullable=False, default="Ready to architect your digital future?"
    )
    cta_body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    cta_highlights: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    seo_title: Mapped[str | None] = mapped_column(String(80))
    seo_description: Mapped[str | None] = mapped_column(String(200))

    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    orders: Mapped[list[Order]] = relationship("Order", back_populates="service")

    def __repr__(self) -> str:
        return f"<Service {self.slug}>"
