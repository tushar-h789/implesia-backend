"""order request targets

Revision ID: 0011
Revises: 0010
Create Date: 2026-09-20

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0011"
down_revision: str | None = "0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        with op.get_context().autocommit_block():
            op.execute("ALTER TYPE order_status ADD VALUE IF NOT EXISTS 'quoted'")

    op.add_column("orders", sa.Column("package_id", sa.Uuid(), nullable=True))
    op.add_column("orders", sa.Column("model_id", sa.Uuid(), nullable=True))
    op.alter_column("orders", "service_id", existing_type=sa.Uuid(), nullable=True)
    op.create_index(op.f("ix_orders_package_id"), "orders", ["package_id"], unique=False)
    op.create_index(op.f("ix_orders_model_id"), "orders", ["model_id"], unique=False)
    op.create_foreign_key(
        op.f("fk_orders_package_id_pricing_packages"),
        "orders",
        "pricing_packages",
        ["package_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        op.f("fk_orders_model_id_engagement_models"),
        "orders",
        "engagement_models",
        ["model_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_orders_model_id_engagement_models"), "orders", type_="foreignkey")
    op.drop_constraint(op.f("fk_orders_package_id_pricing_packages"), "orders", type_="foreignkey")
    op.drop_index(op.f("ix_orders_model_id"), table_name="orders")
    op.drop_index(op.f("ix_orders_package_id"), table_name="orders")
    op.drop_column("orders", "model_id")
    op.drop_column("orders", "package_id")
    op.alter_column("orders", "service_id", existing_type=sa.Uuid(), nullable=False)
