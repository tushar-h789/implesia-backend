"""full service page fields

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

JSON_EMPTY = sa.text("'[]'")


def upgrade() -> None:
    op.add_column(
        "services",
        sa.Column(
            "engagement_status", sa.String(length=40), nullable=False, server_default="Available"
        ),
    )
    op.add_column(
        "services", sa.Column("hero_metrics", sa.JSON(), nullable=False, server_default=JSON_EMPTY)
    )
    op.add_column(
        "services",
        sa.Column(
            "deliver_heading",
            sa.String(length=160),
            nullable=False,
            server_default="What we deliver",
        ),
    )
    op.add_column(
        "services", sa.Column("deliver_body", sa.Text(), nullable=False, server_default="")
    )
    op.add_column(
        "services", sa.Column("capabilities", sa.JSON(), nullable=False, server_default=JSON_EMPTY)
    )
    op.add_column(
        "services",
        sa.Column(
            "deliverables_heading",
            sa.String(length=160),
            nullable=False,
            server_default="What You Receive",
        ),
    )
    op.add_column(
        "services",
        sa.Column(
            "deliverables_kicker",
            sa.String(length=160),
            nullable=False,
            server_default="Included in every engagement",
        ),
    )
    op.add_column(
        "services",
        sa.Column(
            "process_heading", sa.String(length=160), nullable=False, server_default="How we work"
        ),
    )
    op.add_column(
        "services", sa.Column("process_body", sa.Text(), nullable=False, server_default="")
    )
    op.add_column(
        "services",
        sa.Column(
            "outcomes_heading",
            sa.String(length=160),
            nullable=False,
            server_default="Before → After",
        ),
    )
    op.add_column(
        "services", sa.Column("outcomes_body", sa.Text(), nullable=False, server_default="")
    )
    op.add_column(
        "services",
        sa.Column("outcomes_disclaimer", sa.String(length=400), nullable=False, server_default=""),
    )
    op.add_column(
        "services", sa.Column("outcomes", sa.JSON(), nullable=False, server_default=JSON_EMPTY)
    )
    op.add_column(
        "services",
        sa.Column(
            "related_heading",
            sa.String(length=160),
            nullable=False,
            server_default="Related services",
        ),
    )
    op.add_column(
        "services", sa.Column("related_slugs", sa.JSON(), nullable=False, server_default=JSON_EMPTY)
    )
    op.add_column(
        "services",
        sa.Column(
            "faqs_heading",
            sa.String(length=160),
            nullable=False,
            server_default="Still have questions?",
        ),
    )
    op.add_column("services", sa.Column("faqs_body", sa.Text(), nullable=False, server_default=""))
    op.add_column(
        "services", sa.Column("faqs", sa.JSON(), nullable=False, server_default=JSON_EMPTY)
    )
    op.add_column(
        "services",
        sa.Column(
            "cta_heading",
            sa.String(length=160),
            nullable=False,
            server_default="Ready to architect your digital future?",
        ),
    )
    op.add_column("services", sa.Column("cta_body", sa.Text(), nullable=False, server_default=""))
    op.add_column(
        "services",
        sa.Column("cta_highlights", sa.JSON(), nullable=False, server_default=JSON_EMPTY),
    )
    op.add_column("services", sa.Column("seo_title", sa.String(length=80), nullable=True))
    op.add_column("services", sa.Column("seo_description", sa.String(length=200), nullable=True))


def downgrade() -> None:
    for column in (
        "seo_description",
        "seo_title",
        "cta_highlights",
        "cta_body",
        "cta_heading",
        "faqs",
        "faqs_body",
        "faqs_heading",
        "related_slugs",
        "related_heading",
        "outcomes",
        "outcomes_disclaimer",
        "outcomes_body",
        "outcomes_heading",
        "process_body",
        "process_heading",
        "deliverables_kicker",
        "deliverables_heading",
        "capabilities",
        "deliver_body",
        "deliver_heading",
        "hero_metrics",
        "engagement_status",
    ):
        op.drop_column("services", column)
