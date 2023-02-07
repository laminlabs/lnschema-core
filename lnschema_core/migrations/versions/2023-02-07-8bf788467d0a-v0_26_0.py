"""v0.26.0.

Revision ID: 8bf788467d0a
Revises: 9d283a1685a5
Create Date: 2023-02-07 14:56:26.461590

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8bf788467d0a"
down_revision = "9d283a1685a5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    op.rename_table(f"{prefix}dset", f"{prefix}dfolder", schema=schema)
    op.rename_table(f"{prefix}dset_dobject", f"{prefix}dfolder_dobject", schema=schema)
    op.rename_table(f"{prefix}project_dset", f"{prefix}project_dfolder", schema=schema)
    op.alter_column(f"{prefix}dfolder_dobject", "dset_id", "dfolder_id", schema=schema)
    op.alter_column(f"{prefix}project_dset", "dset_id", "dfolder_id", schema=schema)


def downgrade() -> None:
    pass
