"""articles page and posts

Revision ID: 0007
Revises: 0006
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0007"
down_revision: str | None = "0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "articles_pages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("hero_heading", sa.String(length=200), nullable=False),
        sa.Column("hero_body", sa.Text(), nullable=False),
        sa.Column("hero_metrics", sa.JSON(), nullable=False),
        sa.Column("hero_highlights", sa.JSON(), nullable=False),
        sa.Column("topics_heading", sa.String(length=200), nullable=False),
        sa.Column("topics", sa.JSON(), nullable=False),
        sa.Column("featured_kicker", sa.String(length=120), nullable=False),
        sa.Column("library_kicker", sa.String(length=120), nullable=False),
        sa.Column("library_heading", sa.String(length=200), nullable=False),
        sa.Column("library_body", sa.Text(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_articles_pages")),
    )
    op.create_index(op.f("ix_articles_pages_slug"), "articles_pages", ["slug"], unique=True)

    op.create_table(
        "articles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=220), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("excerpt", sa.String(length=400), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("topic", sa.String(length=40), nullable=False),
        sa.Column("topic_label", sa.String(length=40), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("author_name", sa.String(length=120), nullable=False),
        sa.Column("author_role", sa.String(length=120), nullable=False),
        sa.Column("reading_minutes", sa.Integer(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("seo_title", sa.String(length=80), nullable=True),
        sa.Column("seo_description", sa.String(length=200), nullable=True),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_articles")),
    )
    op.create_index(op.f("ix_articles_slug"), "articles", ["slug"], unique=True)
    op.create_index(op.f("ix_articles_topic"), "articles", ["topic"], unique=False)
    op.create_index(op.f("ix_articles_is_published"), "articles", ["is_published"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_articles_is_published"), table_name="articles")
    op.drop_index(op.f("ix_articles_topic"), table_name="articles")
    op.drop_index(op.f("ix_articles_slug"), table_name="articles")
    op.drop_table("articles")
    op.drop_index(op.f("ix_articles_pages_slug"), table_name="articles_pages")
    op.drop_table("articles_pages")
