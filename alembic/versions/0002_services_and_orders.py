"""services and orders

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

order_status = sa.Enum(
    "new",
    "contacted",
    "in_progress",
    "completed",
    "cancelled",
    name="order_status",
)


def upgrade() -> None:
    op.create_table(
        "services",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("tagline", sa.String(length=280), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("icon", sa.String(length=80), nullable=True),
        sa.Column("tech_stack", sa.JSON(), nullable=False),
        sa.Column("deliverables", sa.JSON(), nullable=False),
        sa.Column("process_steps", sa.JSON(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_services")),
    )
    op.create_index(op.f("ix_services_slug"), "services", ["slug"], unique=True)
    op.create_index(op.f("ix_services_is_published"), "services", ["is_published"], unique=False)

    op.create_table(
        "orders",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("service_id", sa.Uuid(), nullable=False),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("organisation", sa.String(length=200), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("status", order_status, nullable=False),
        sa.Column("internal_notes", sa.Text(), nullable=True),
        sa.Column("source_page", sa.String(length=255), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("idempotency_key", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            name=op.f("fk_orders_service_id_services"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
        sa.UniqueConstraint("idempotency_key", name=op.f("uq_orders_idempotency_key")),
    )
    op.create_index(op.f("ix_orders_service_id"), "orders", ["service_id"], unique=False)
    op.create_index(op.f("ix_orders_email"), "orders", ["email"], unique=False)
    op.create_index(op.f("ix_orders_status"), "orders", ["status"], unique=False)
    op.create_index("ix_orders_status_created_at", "orders", ["status", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_orders_status_created_at", table_name="orders")
    op.drop_index(op.f("ix_orders_status"), table_name="orders")
    op.drop_index(op.f("ix_orders_email"), table_name="orders")
    op.drop_index(op.f("ix_orders_service_id"), table_name="orders")
    op.drop_table("orders")
    order_status.drop(op.get_bind(), checkfirst=True)

    op.drop_index(op.f("ix_services_is_published"), table_name="services")
    op.drop_index(op.f("ix_services_slug"), table_name="services")
    op.drop_table("services")
