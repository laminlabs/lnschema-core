"""v0.26.2.

Revision ID: 8280855a5064
Revises: ff3b5b3ec913
Create Date: 2023-02-14 22:21:20.501993

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8280855a5064"
down_revision = "ff3b5b3ec913"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    with op.batch_alter_table(f"{prefix}run", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("external_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        if sqlite:
            batch_op.create_index(batch_op.f("ix_core.run_external_id"), ["external_id"], unique=False)
        else:
            batch_op.create_index(batch_op.f("ix_core_run_external_id"), ["external_id"], unique=False)


def downgrade() -> None:
    pass
