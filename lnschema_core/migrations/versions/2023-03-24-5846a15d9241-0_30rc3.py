"""v0.30rc3."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "5846a15d9241"
down_revision = "ebafd37fd6e1"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    op.rename_table(old_table_name=f"{prefix}dobject", new_table_name=f"{prefix}file", schema=schema)
    op.rename_table(old_table_name=f"{prefix}dfolder", new_table_name=f"{prefix}folder", schema=schema)


def downgrade() -> None:
    pass
