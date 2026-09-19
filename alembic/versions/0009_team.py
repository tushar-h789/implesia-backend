"""team page and members

Revision ID: 0009
Revises: 0008
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0009"
down_revision: str | None = "0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "team_pages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("hero_kicker", sa.String(length=120), nullable=False),
        sa.Column("hero_heading", sa.String(length=200), nullable=False),
        sa.Column("hero_body", sa.Text(), nullable=False),
        sa.Column("hero_metrics", sa.JSON(), nullable=False),
        sa.Column("hero_highlights", sa.JSON(), nullable=False),
        sa.Column("members_kicker", sa.String(length=120), nullable=False),
        sa.Column("members_heading", sa.String(length=200), nullable=False),
        sa.Column("members_body", sa.Text(), nullable=False),
        sa.Column("practices_kicker", sa.String(length=120), nullable=False),
        sa.Column("practices_heading", sa.String(length=200), nullable=False),
        sa.Column("practices_body", sa.Text(), nullable=False),
        sa.Column("practices_highlights", sa.JSON(), nullable=False),
        sa.Column("practices", sa.JSON(), nullable=False),
        sa.Column("principles_kicker", sa.String(length=120), nullable=False),
        sa.Column("principles_heading", sa.String(length=200), nullable=False),
        sa.Column("principles_body", sa.Text(), nullable=False),
        sa.Column("principles", sa.JSON(), nullable=False),
        sa.Column("principles_cta_label", sa.String(length=80), nullable=False),
        sa.Column("principles_cta_secondary", sa.String(length=80), nullable=False),
        sa.Column("meet_heading", sa.String(length=200), nullable=False),
        sa.Column("meet_body", sa.Text(), nullable=False),
        sa.Column("meet_highlights", sa.JSON(), nullable=False),
        sa.Column("meet_cta_label", sa.String(length=80), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_team_pages")),
    )
    op.create_index(op.f("ix_team_pages_slug"), "team_pages", ["slug"], unique=True)

    op.create_table(
        "team_members",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("role", sa.String(length=120), nullable=False),
        sa.Column("bio", sa.Text(), nullable=False),
        sa.Column("skills", sa.JSON(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_team_members")),
    )
    op.create_index(op.f("ix_team_members_slug"), "team_members", ["slug"], unique=True)
    op.create_index(op.f("ix_team_members_is_published"), "team_members", ["is_published"])


def downgrade() -> None:
    op.drop_index(op.f("ix_team_members_is_published"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_slug"), table_name="team_members")
    op.drop_table("team_members")
    op.drop_index(op.f("ix_team_pages_slug"), table_name="team_pages")
    op.drop_table("team_pages")
