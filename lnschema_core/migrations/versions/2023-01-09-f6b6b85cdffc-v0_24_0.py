"""v0.24.0.

Revision ID: f6b6b85cdffc
Revises: db1df7b2aaad
Create Date: 2023-01-09 12:05:35.536833

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f6b6b85cdffc"
down_revision = "db1df7b2aaad"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    if sqlite:
        with op.batch_alter_table(f"{prefix}notebook", schema=schema) as batch_op:
            batch_op.add_column(sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
            batch_op.create_index(batch_op.f("ix_core.notebook_title"), ["title"], unique=False)
    else:
        op.add_column(f"{prefix}notebook", sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=True), schema=schema)
        op.create_index(op.f("ix_core_notebook_title"), "notebook", ["title"], unique=False, schema=schema)


def downgrade() -> None:
    pass
