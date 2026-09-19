"""drop one-time server defaults from service page columns

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-19

"""

from collections.abc import Sequence

from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

COLUMNS = (
    "engagement_status",
    "hero_metrics",
    "deliver_heading",
    "deliver_body",
    "capabilities",
    "deliverables_heading",
    "deliverables_kicker",
    "process_heading",
    "process_body",
    "outcomes_heading",
    "outcomes_body",
    "outcomes_disclaimer",
    "outcomes",
    "related_heading",
    "related_slugs",
    "faqs_heading",
    "faqs_body",
    "faqs",
    "cta_heading",
    "cta_body",
    "cta_highlights",
)


def upgrade() -> None:
    for column in COLUMNS:
        op.alter_column("services", column, server_default=None)


def downgrade() -> None:
    return
