"""v0.7.1.

Revision ID: 049d7dfc80a8
Revises: 3b60b87450c0
Create Date: 2022-09-18 17:31:43.384602
"""
import sqlalchemy as sa
import sqlmodel  # noqa
from alembic import op

revision = "049d7dfc80a8"
down_revision = "3b60b87450c0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.add_column(
            "dobject",
            sa.Column("suffix", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        )
        op.create_index(op.f("ix_dobject_suffix"), "dobject", ["suffix"], unique=False)
        op.execute("update dobject set suffix = file_suffix")
        op.drop_index("ix_dobject_file_suffix", table_name="dobject")
        op.drop_column("dobject", "file_suffix")
    else:
        op.alter_column(
            "dobject",
            column_name="file_suffix",
            new_column_name="suffix",
            nullable=True,
        )


def downgrade() -> None:
    pass
