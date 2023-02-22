"""v0.28.1."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

revision = "6952574e2d49"
down_revision = "1dafcf0b22aa"


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    if sqlite:
        with op.batch_alter_table(f"{prefix}dfolder", schema=schema) as batch_op:
            batch_op.add_column(sa.Column("_folderkey", sqm.sql.sqltypes.AutoString(), nullable=True))
            batch_op.create_index(batch_op.f("ix_core.dfolder__folderkey"), ["_folderkey"], unique=False)
    else:
        op.add_column(
            f"{prefix}dfolder",
            sa.Column("_folderkey", sqm.sql.sqltypes.AutoString(), nullable=True),
            schema=schema,
        )
        op.create_index(
            op.f("ix_core_dfolder__folderkey"),
            "dfolder",
            ["_folderkey"],
            unique=False,
            schema=schema,
        )


def downgrade() -> None:
    pass
