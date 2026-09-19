"""pricing page, engagement models, packages

Revision ID: 0005
Revises: 0004
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0005"
down_revision: str | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "pricing_pages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("hero_heading", sa.String(length=200), nullable=False),
        sa.Column("hero_body", sa.Text(), nullable=False),
        sa.Column("paths_kicker", sa.String(length=120), nullable=False),
        sa.Column("paths_heading", sa.String(length=200), nullable=False),
        sa.Column("paths_body", sa.Text(), nullable=False),
        sa.Column("paths", sa.JSON(), nullable=False),
        sa.Column("models_kicker", sa.String(length=120), nullable=False),
        sa.Column("models_heading", sa.String(length=200), nullable=False),
        sa.Column("models_body", sa.Text(), nullable=False),
        sa.Column("models_currency_note", sa.String(length=200), nullable=False),
        sa.Column("models_disclaimer", sa.Text(), nullable=False),
        sa.Column("packages_kicker", sa.String(length=120), nullable=False),
        sa.Column("packages_heading", sa.String(length=200), nullable=False),
        sa.Column("packages_body", sa.Text(), nullable=False),
        sa.Column("packages_currency_note", sa.String(length=200), nullable=False),
        sa.Column("commercial_terms", sa.JSON(), nullable=False),
        sa.Column("packages_disclaimer", sa.Text(), nullable=False),
        sa.Column("process_kicker", sa.String(length=120), nullable=False),
        sa.Column("process_heading", sa.String(length=200), nullable=False),
        sa.Column("process_body", sa.Text(), nullable=False),
        sa.Column("process_steps", sa.JSON(), nullable=False),
        sa.Column("faqs_kicker", sa.String(length=120), nullable=False),
        sa.Column("faqs_heading", sa.String(length=200), nullable=False),
        sa.Column("faqs", sa.JSON(), nullable=False),
        sa.Column("cta_heading", sa.String(length=200), nullable=False),
        sa.Column("cta_body", sa.Text(), nullable=False),
        sa.Column("cta_highlights", sa.JSON(), nullable=False),
        sa.Column("cta_primary_label", sa.String(length=80), nullable=False),
        sa.Column("cta_secondary_label", sa.String(length=80), nullable=False),
        sa.Column("seo_title", sa.String(length=80), nullable=True),
        sa.Column("seo_description", sa.String(length=200), nullable=True),
        sa.Column("bdt_per_usd", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pricing_pages")),
    )
    op.create_index(op.f("ix_pricing_pages_slug"), "pricing_pages", ["slug"], unique=True)

    op.create_table(
        "engagement_models",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("icon", sa.String(length=80), nullable=True),
        sa.Column("kicker", sa.String(length=120), nullable=False),
        sa.Column("badge", sa.String(length=80), nullable=True),
        sa.Column("price_label", sa.String(length=80), nullable=False),
        sa.Column("price_amount", sa.Integer(), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("cadence", sa.String(length=20), nullable=False),
        sa.Column("subtitle", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("inclusions", sa.JSON(), nullable=False),
        sa.Column("ideal_for", sa.String(length=160), nullable=False),
        sa.Column("cta_label", sa.String(length=80), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_engagement_models")),
    )
    op.create_index(op.f("ix_engagement_models_slug"), "engagement_models", ["slug"], unique=True)
    op.create_index(
        op.f("ix_engagement_models_is_published"),
        "engagement_models",
        ["is_published"],
        unique=False,
    )

    op.create_table(
        "pricing_packages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("icon", sa.String(length=80), nullable=True),
        sa.Column("tagline", sa.String(length=200), nullable=False),
        sa.Column("badge", sa.String(length=80), nullable=True),
        sa.Column("price_label", sa.String(length=80), nullable=False),
        sa.Column("price_amount_bdt", sa.Integer(), nullable=False),
        sa.Column("timeline_label", sa.String(length=80), nullable=False),
        sa.Column("bugfix_label", sa.String(length=80), nullable=False),
        sa.Column("audience", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("dashboard_heading", sa.String(length=120), nullable=False),
        sa.Column("dashboard_body", sa.Text(), nullable=False),
        sa.Column("inclusions", sa.JSON(), nullable=False),
        sa.Column("exclusions", sa.JSON(), nullable=False),
        sa.Column("cta_label", sa.String(length=120), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pricing_packages")),
    )
    op.create_index(op.f("ix_pricing_packages_slug"), "pricing_packages", ["slug"], unique=True)
    op.create_index(
        op.f("ix_pricing_packages_is_published"),
        "pricing_packages",
        ["is_published"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_pricing_packages_is_published"), table_name="pricing_packages")
    op.drop_index(op.f("ix_pricing_packages_slug"), table_name="pricing_packages")
    op.drop_table("pricing_packages")
    op.drop_index(op.f("ix_engagement_models_is_published"), table_name="engagement_models")
    op.drop_index(op.f("ix_engagement_models_slug"), table_name="engagement_models")
    op.drop_table("engagement_models")
    op.drop_index(op.f("ix_pricing_pages_slug"), table_name="pricing_pages")
    op.drop_table("pricing_pages")
