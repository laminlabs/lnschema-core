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

    op.drop_index(f"ix_core{delim}usage_dobject_id", table_name="usage", schema=schema)
    op.drop_index(f"ix_core{delim}usage_time", table_name="usage", schema=schema)
    op.drop_index(f"ix_core{delim}usage_type", table_name="usage", schema=schema)
    op.drop_index(f"ix_core{delim}usage_user_id", table_name="usage", schema=schema)
    op.drop_table(f"{prefix}usage", schema=schema)


def downgrade() -> None:
    pass
