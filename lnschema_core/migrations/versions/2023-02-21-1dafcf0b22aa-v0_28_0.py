"""v0.28.0."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

revision = "1dafcf0b22aa"
down_revision = "8280855a5064"


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    op.alter_column(f"{prefix}dobject", column_name="run_id", new_column_name="source_id", schema=schema)
    if sqlite:
        op.drop_index("ix_core.dobject_run_id", table_name="dobject")
        op.create_index(op.f("ix_core.dobject_source_id"), "dobject", ["source_id"], unique=False)
    else:
        op.drop_index("ix_core_dobject_run_id", table_name="dobject", schema="core")
        op.create_index(op.f("ix_core_dobject_source_id"), "dobject", ["source_id"], unique=False, schema="core")


def downgrade() -> None:
    pass
