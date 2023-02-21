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
        with op.batch_alter_table("core.dobject", schema=None) as batch_op:
            # batch_op.drop_index("ix_core.dobject_run_id")  # this errors probably on old instances
            batch_op.create_index(batch_op.f("ix_core.dobject_source_id"), ["source_id"], unique=False)
            batch_op.create_foreign_key(batch_op.f("fk_core.dobject_source_id_run"), "core.run", ["source_id"], ["id"])
    else:
        op.drop_index("ix_core_dobject_run_id", table_name="dobject", schema="core")
        op.create_index(op.f("ix_core_dobject_source_id"), "dobject", ["source_id"], unique=False, schema="core")


def downgrade() -> None:
    pass
