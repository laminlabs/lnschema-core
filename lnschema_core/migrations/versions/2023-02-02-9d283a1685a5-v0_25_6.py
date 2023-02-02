"""v0.25.6.

Revision ID: 9d283a1685a5
Revises: f6b6b85cdffc
Create Date: 2023-02-02 21:22:35.229193

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9d283a1685a5"
down_revision = "f6b6b85cdffc"
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
        with op.batch_alter_table(f"{prefix}dobject", schema=schema) as batch_op:
            batch_op.add_column(sa.Column("_filekey", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
            batch_op.create_index(batch_op.f("ix_core.dobject__filekey"), ["_filekey"], unique=False)
    else:
        op.add_column(
            f"{prefix}dobject",
            sa.Column("_filekey", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            schema=schema,
        )
        op.create_index(
            op.f("ix_core_dobject__filekey"),
            "dobject",
            ["_filekey"],
            unique=False,
            schema=schema,
        )


def downgrade() -> None:
    pass
