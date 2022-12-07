"""v0.21.3.

Revision ID: 9d94f3b9566d
Revises: 4b4005b7841c
Create Date: 2022-12-07 00:12:51.485117

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9d94f3b9566d"
down_revision = "4b4005b7841c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    with op.batch_alter_table(f"{prefix}dobject", schema=schema) as batch_op:
        batch_op.alter_column(
            "size",
            existing_type=sa.FLOAT(),
            type_=sa.BigInteger(),
            existing_nullable=True,
        )


def downgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    with op.batch_alter_table(f"{prefix}dobject", schema=schema) as batch_op:
        batch_op.alter_column(
            "size",
            existing_type=sa.BigInteger(),
            type_=sa.FLOAT(),
            existing_nullable=True,
        )
