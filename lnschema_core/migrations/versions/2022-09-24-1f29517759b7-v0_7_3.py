"""v0.7.3.

Revision ID: 1f29517759b7
Revises: 049d7dfc80a8
Create Date: 2022-09-24 10:32:37.801549

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1f29517759b7"
down_revision = "049d7dfc80a8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("dobject", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DATETIME(),
            nullable=False,
            existing_server_default=sa.text("(CURRENT_TIMESTAMP)"),
        )

    with op.batch_alter_table("jupynb", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DATETIME(),
            nullable=False,
            existing_server_default=sa.text("(CURRENT_TIMESTAMP)"),
        )

    with op.batch_alter_table("pipeline", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DATETIME(),
            nullable=False,
            existing_server_default=sa.text("(CURRENT_TIMESTAMP)"),
        )

    with op.batch_alter_table("pipeline_run", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DATETIME(),
            nullable=False,
            existing_server_default=sa.text("(CURRENT_TIMESTAMP)"),
        )

    with op.batch_alter_table("storage", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DATETIME(),
            nullable=False,
            existing_server_default=sa.text("(CURRENT_TIMESTAMP)"),
        )

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DATETIME(),
            nullable=False,
            existing_server_default=sa.text("(CURRENT_TIMESTAMP)"),
        )
        # batch_op.drop_constraint("user", type_="unique")  # seems not needed
        batch_op.drop_index("ix_user_email")
        batch_op.create_index(batch_op.f("ix_user_email"), ["email"], unique=True)
        batch_op.drop_index("ix_user_handle")
        batch_op.create_index(batch_op.f("ix_user_handle"), ["handle"], unique=True)

    with op.batch_alter_table("version_yvzi", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DATETIME(),
            nullable=False,
            existing_server_default=sa.text("(CURRENT_TIMESTAMP)"),
        )

    with op.batch_alter_table("usage", schema=None) as batch_op:
        batch_op.alter_column(
            "time",
            existing_type=sa.DATETIME(),
            nullable=False,
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
        )


def downgrade() -> None:
    pass
