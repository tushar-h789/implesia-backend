from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.pricing import EngagementModel, PricingPackage
    from app.models.service import Service


class OrderStatus(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    QUOTED = "quoted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A buy request for a published service, pricing package, or engagement model."""

    __tablename__ = "orders"
    __table_args__ = (Index("ix_orders_status_created_at", "status", "created_at"),)

    service_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    service: Mapped[Service | None] = relationship(back_populates="orders")

    package_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("pricing_packages.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    package: Mapped[PricingPackage | None] = relationship(back_populates="orders")

    model_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("engagement_models.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    model: Mapped[EngagementModel | None] = relationship(back_populates="orders")

    full_name: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str] = mapped_column(String(320), index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(40))
    organisation: Mapped[str | None] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status", values_callable=lambda e: [m.value for m in e]),
        default=OrderStatus.NEW,
        nullable=False,
        index=True,
    )
    internal_notes: Mapped[str | None] = mapped_column(Text)

    source_page: Mapped[str | None] = mapped_column(String(255))
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(512))
    idempotency_key: Mapped[str | None] = mapped_column(String(64), unique=True)

    def __repr__(self) -> str:
        return f"<Order {self.email} ({self.status})>"
