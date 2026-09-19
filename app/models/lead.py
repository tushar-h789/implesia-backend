from enum import StrEnum

from sqlalchemy import Enum, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ServiceArea(StrEnum):
    WEB_PLATFORMS = "web-platforms"
    MOBILE_APPLICATIONS = "mobile-applications"
    SAAS_ARCHITECTURE = "saas-architecture"
    UI_UX_DESIGN = "ui-ux-design"
    BUSINESS_AUTOMATION = "business-automation"
    E_COMMERCE = "e-commerce"


class Timeline(StrEnum):
    ASAP = "asap"
    ONE_TO_THREE_MONTHS = "1-3-months"
    THREE_TO_SIX_MONTHS = "3-6-months"
    EXPLORING = "exploring"


class LeadStatus(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    WON = "won"
    LOST = "lost"
    SPAM = "spam"


class Lead(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A project enquiry submitted through the public contact form."""

    __tablename__ = "leads"
    __table_args__ = (Index("ix_leads_status_created_at", "status", "created_at"),)

    full_name: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str] = mapped_column(String(320), index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(40))
    organisation: Mapped[str | None] = mapped_column(String(200))
    service_area: Mapped[ServiceArea | None] = mapped_column(
        Enum(ServiceArea, name="service_area", values_callable=lambda e: [m.value for m in e])
    )
    timeline: Mapped[Timeline | None] = mapped_column(
        Enum(Timeline, name="lead_timeline", values_callable=lambda e: [m.value for m in e])
    )
    brief: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus, name="lead_status", values_callable=lambda e: [m.value for m in e]),
        default=LeadStatus.NEW,
        nullable=False,
        index=True,
    )
    internal_notes: Mapped[str | None] = mapped_column(Text)

    # Submission metadata, used for spam triage and attribution.
    source_page: Mapped[str | None] = mapped_column(String(255))
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(512))

    # Set by the client so a retried POST does not create a duplicate lead.
    idempotency_key: Mapped[str | None] = mapped_column(String(64), unique=True)

    def __repr__(self) -> str:
        return f"<Lead {self.email} ({self.status})>"
