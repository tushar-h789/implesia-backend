from enum import StrEnum
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.service import Service


class OrderStatus(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A request to buy or start a published service."""

    __tablename__ = "orders"
    __table_args__ = (Index("ix_orders_status_created_at", "status", "created_at"),)

    service_id: Mapped[UUID] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    service: Mapped[Service] = relationship(back_populates="orders")

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
