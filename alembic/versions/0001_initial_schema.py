"""initial schema: users and leads

Revision ID: 0001
Revises:
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

user_role = sa.Enum("superadmin", "editor", "viewer", name="user_role")
service_area = sa.Enum(
    "web-platforms",
    "mobile-applications",
    "saas-architecture",
    "ui-ux-design",
    "business-automation",
    "e-commerce",
    name="service_area",
)
lead_timeline = sa.Enum("asap", "1-3-months", "3-6-months", "exploring", name="lead_timeline")
lead_status = sa.Enum("new", "contacted", "qualified", "won", "lost", "spam", name="lead_status")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "leads",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("organisation", sa.String(length=200), nullable=True),
        sa.Column("service_area", service_area, nullable=True),
        sa.Column("timeline", lead_timeline, nullable=True),
        sa.Column("brief", sa.Text(), nullable=False),
        sa.Column("status", lead_status, nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_leads")),
        sa.UniqueConstraint("idempotency_key", name=op.f("uq_leads_idempotency_key")),
    )
    op.create_index(op.f("ix_leads_email"), "leads", ["email"], unique=False)
    op.create_index(op.f("ix_leads_status"), "leads", ["status"], unique=False)
    op.create_index("ix_leads_status_created_at", "leads", ["status", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_leads_status_created_at", table_name="leads")
    op.drop_index(op.f("ix_leads_status"), table_name="leads")
    op.drop_index(op.f("ix_leads_email"), table_name="leads")
    op.drop_table("leads")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    for enum in (lead_status, lead_timeline, service_area, user_role):
        enum.drop(bind, checkfirst=True)
