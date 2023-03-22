"""v0.30rc1."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

revision = "9640062eefee"
down_revision = "873683a29806"


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema, delim = "core.", None, "."
    else:
        prefix, schema, delim = "", "core", "_"

    with op.batch_alter_table(f"{prefix}usage", schema=schema) as batch_op:
        batch_op.drop_index(f"ix_core{delim}usage_dobject_id")
        batch_op.drop_index(f"ix_core{delim}usage_time")
        batch_op.drop_index(f"ix_core{delim}usage_type")
        batch_op.drop_index(f"ix_core{delim}usage_user_id")
    op.drop_table(f"{prefix}usage", schema=schema)


def downgrade() -> None:
    pass
