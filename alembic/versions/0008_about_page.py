"""about-us page

Revision ID: 0008
Revises: 0007
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0008"
down_revision: str | None = "0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "about_pages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("hero_kicker", sa.String(length=120), nullable=False),
        sa.Column("hero_heading", sa.String(length=200), nullable=False),
        sa.Column("hero_body", sa.Text(), nullable=False),
        sa.Column("hero_primary_label", sa.String(length=80), nullable=False),
        sa.Column("hero_secondary_label", sa.String(length=80), nullable=False),
        sa.Column("hero_highlights", sa.JSON(), nullable=False),
        sa.Column("hero_metrics", sa.JSON(), nullable=False),
        sa.Column("quote_kicker", sa.String(length=120), nullable=False),
        sa.Column("quote_text", sa.Text(), nullable=False),
        sa.Column("quote_attribution", sa.String(length=160), nullable=False),
        sa.Column("story_kicker", sa.String(length=120), nullable=False),
        sa.Column("story_heading", sa.String(length=200), nullable=False),
        sa.Column("story_body", sa.Text(), nullable=False),
        sa.Column("story_emphasis", sa.String(length=280), nullable=False),
        sa.Column("story_body_secondary", sa.Text(), nullable=False),
        sa.Column("pillars", sa.JSON(), nullable=False),
        sa.Column("operating_principles_heading", sa.String(length=120), nullable=False),
        sa.Column("operating_principles", sa.JSON(), nullable=False),
        sa.Column("founder_name", sa.String(length=120), nullable=False),
        sa.Column("founder_role", sa.String(length=120), nullable=False),
        sa.Column("founder_org", sa.String(length=120), nullable=False),
        sa.Column("founder_kicker", sa.String(length=120), nullable=False),
        sa.Column("founder_heading", sa.String(length=200), nullable=False),
        sa.Column("founder_lede", sa.Text(), nullable=False),
        sa.Column("founder_body", sa.Text(), nullable=False),
        sa.Column("founder_close", sa.Text(), nullable=False),
        sa.Column("founder_signoff", sa.String(length=80), nullable=False),
        sa.Column("founder_location", sa.String(length=120), nullable=False),
        sa.Column("founder_cta_label", sa.String(length=80), nullable=False),
        sa.Column("founder_highlights", sa.JSON(), nullable=False),
        sa.Column("purpose_kicker", sa.String(length=120), nullable=False),
        sa.Column("purpose_heading", sa.String(length=200), nullable=False),
        sa.Column("purpose_body", sa.Text(), nullable=False),
        sa.Column("commitments", sa.JSON(), nullable=False),
        sa.Column("tenets_kicker", sa.String(length=120), nullable=False),
        sa.Column("tenets_heading", sa.String(length=200), nullable=False),
        sa.Column("tenets_body", sa.Text(), nullable=False),
        sa.Column("tenets", sa.JSON(), nullable=False),
        sa.Column("stability_kicker", sa.String(length=120), nullable=False),
        sa.Column("stability_heading", sa.String(length=200), nullable=False),
        sa.Column("stability_body", sa.Text(), nullable=False),
        sa.Column("stability_quote_kicker", sa.String(length=120), nullable=False),
        sa.Column("stability_quote", sa.Text(), nullable=False),
        sa.Column("foundations", sa.JSON(), nullable=False),
        sa.Column("culture_kicker", sa.String(length=120), nullable=False),
        sa.Column("culture_heading", sa.String(length=200), nullable=False),
        sa.Column("culture_body", sa.Text(), nullable=False),
        sa.Column("culture_items", sa.JSON(), nullable=False),
        sa.Column("culture_cta_label", sa.String(length=80), nullable=False),
        sa.Column("cta_heading", sa.String(length=200), nullable=False),
        sa.Column("cta_body", sa.Text(), nullable=False),
        sa.Column("cta_highlights", sa.JSON(), nullable=False),
        sa.Column("cta_primary_label", sa.String(length=80), nullable=False),
        sa.Column("cta_secondary_label", sa.String(length=80), nullable=False),
        sa.Column("seo_title", sa.String(length=80), nullable=True),
        sa.Column("seo_description", sa.String(length=200), nullable=True),
        sa.Column("internal_notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_about_pages")),
    )
    op.create_index(op.f("ix_about_pages_slug"), "about_pages", ["slug"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_about_pages_slug"), table_name="about_pages")
    op.drop_table("about_pages")
