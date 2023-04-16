"""v0.33.0."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "6a73c00555b4"
down_revision = "d161a14a12e3"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    op.alter_column(f"{prefix}file", column_name="source_id", new_column_name="run_id", schema=schema)


def downgrade() -> None:
    pass
