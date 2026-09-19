"""contact page

Revision ID: 0010
Revises: 0009
Create Date: 2026-09-19

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0010"
down_revision: str | None = "0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "contact_pages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("hero_kicker", sa.String(length=120), nullable=False),
        sa.Column("hero_heading", sa.String(length=200), nullable=False),
        sa.Column("hero_body", sa.Text(), nullable=False),
        sa.Column("hero_highlights", sa.JSON(), nullable=False),
        sa.Column("hero_metrics", sa.JSON(), nullable=False),
        sa.Column("form_intro", sa.Text(), nullable=False),
        sa.Column("channels_kicker", sa.String(length=120), nullable=False),
        sa.Column("channels_heading", sa.String(length=200), nullable=False),
        sa.Column("channels_body", sa.Text(), nullable=False),
        sa.Column("channels", sa.JSON(), nullable=False),
        sa.Column("office_hours_heading", sa.String(length=120), nullable=False),
        sa.Column("office_hours", sa.JSON(), nullable=False),
        sa.Column("office_hours_note", sa.Text(), nullable=False),
        sa.Column("form_heading", sa.String(length=200), nullable=False),
        sa.Column("form_body", sa.Text(), nullable=False),
        sa.Column("form_privacy", sa.Text(), nullable=False),
        sa.Column("form_submit_label", sa.String(length=80), nullable=False),
        sa.Column("form_action", sa.String(length=120), nullable=False),
        sa.Column("service_options", sa.JSON(), nullable=False),
        sa.Column("timeline_options", sa.JSON(), nullable=False),
        sa.Column("process_kicker", sa.String(length=120), nullable=False),
        sa.Column("process_heading", sa.String(length=200), nullable=False),
        sa.Column("process_body", sa.Text(), nullable=False),
        sa.Column("process_steps", sa.JSON(), nullable=False),
        sa.Column("process_quote", sa.Text(), nullable=False),
        sa.Column("faqs_kicker", sa.String(length=120), nullable=False),
        sa.Column("faqs_heading", sa.String(length=200), nullable=False),
        sa.Column("faqs_body", sa.Text(), nullable=False),
        sa.Column("faq_highlights", sa.JSON(), nullable=False),
        sa.Column("faqs", sa.JSON(), nullable=False),
        sa.Column("faqs_cta_heading", sa.String(length=200), nullable=False),
        sa.Column("faqs_cta_body", sa.Text(), nullable=False),
        sa.Column("agreement_note", sa.Text(), nullable=False),
        sa.Column("agreement_kicker", sa.String(length=160), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_contact_pages")),
    )
    op.create_index(op.f("ix_contact_pages_slug"), "contact_pages", ["slug"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_contact_pages_slug"), table_name="contact_pages")
    op.drop_table("contact_pages")
