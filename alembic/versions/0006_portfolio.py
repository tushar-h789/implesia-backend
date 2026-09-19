"""portfolio page and projects

Revision ID: 0006
Revises: 0005
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "portfolio_pages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("hero_heading", sa.String(length=200), nullable=False),
        sa.Column("hero_body", sa.Text(), nullable=False),
        sa.Column("hero_metrics", sa.JSON(), nullable=False),
        sa.Column("hero_highlights", sa.JSON(), nullable=False),
        sa.Column("featured_kicker", sa.String(length=120), nullable=False),
        sa.Column("featured_heading", sa.String(length=200), nullable=False),
        sa.Column("featured_body", sa.Text(), nullable=False),
        sa.Column("archive_kicker", sa.String(length=120), nullable=False),
        sa.Column("archive_heading", sa.String(length=200), nullable=False),
        sa.Column("archive_body", sa.Text(), nullable=False),
        sa.Column("categories", sa.JSON(), nullable=False),
        sa.Column("impact_kicker", sa.String(length=120), nullable=False),
        sa.Column("impact_heading", sa.String(length=200), nullable=False),
        sa.Column("impact_body", sa.Text(), nullable=False),
        sa.Column("impact_stats", sa.JSON(), nullable=False),
        sa.Column("pillars_kicker", sa.String(length=120), nullable=False),
        sa.Column("pillars_heading", sa.String(length=200), nullable=False),
        sa.Column("pillars_body", sa.Text(), nullable=False),
        sa.Column("pillars", sa.JSON(), nullable=False),
        sa.Column("engagement_highlights", sa.JSON(), nullable=False),
        sa.Column("cta_heading", sa.String(length=200), nullable=False),
        sa.Column("cta_body", sa.Text(), nullable=False),
        sa.Column("cta_highlights", sa.JSON(), nullable=False),
        sa.Column("cta_primary_label", sa.String(length=80), nullable=False),
        sa.Column("cta_secondary_label", sa.String(length=80), nullable=False),
        sa.Column("seo_title", sa.String(length=80), nullable=True),
        sa.Column("seo_description", sa.String(length=200), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_portfolio_pages")),
    )
    op.create_index(op.f("ix_portfolio_pages_slug"), "portfolio_pages", ["slug"], unique=True)

    op.create_table(
        "portfolio_projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("tagline", sa.String(length=200), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("tech_stack", sa.JSON(), nullable=False),
        sa.Column("live_url", sa.String(length=255), nullable=True),
        sa.Column("live_label", sa.String(length=120), nullable=True),
        sa.Column("outcomes", sa.JSON(), nullable=False),
        sa.Column("icon", sa.String(length=80), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("internal_notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_portfolio_projects")),
    )
    op.create_index(op.f("ix_portfolio_projects_slug"), "portfolio_projects", ["slug"], unique=True)
    op.create_index(
        op.f("ix_portfolio_projects_category"), "portfolio_projects", ["category"], unique=False
    )
    op.create_index(
        op.f("ix_portfolio_projects_is_published"),
        "portfolio_projects",
        ["is_published"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_portfolio_projects_is_published"), table_name="portfolio_projects")
    op.drop_index(op.f("ix_portfolio_projects_category"), table_name="portfolio_projects")
    op.drop_index(op.f("ix_portfolio_projects_slug"), table_name="portfolio_projects")
    op.drop_table("portfolio_projects")
    op.drop_index(op.f("ix_portfolio_pages_slug"), table_name="portfolio_pages")
    op.drop_table("portfolio_pages")
