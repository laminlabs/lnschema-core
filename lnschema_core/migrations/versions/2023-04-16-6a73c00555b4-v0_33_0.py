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
    op.drop_index(f"ix_core{delim}file_source_id", table_name="file", schema=schema)
    op.create_index(op.f(f"ix_core{delim}file_run_id"), "file", ["run_id"], unique=False, schema=schema)

    op.alter_column(f"{prefix}folder", column_name="created_by", new_column_name="created_by_id", schema=schema)
    op.alter_column(f"{prefix}run", column_name="created_by", new_column_name="created_by_id", schema=schema)
    op.alter_column(f"{prefix}features", column_name="created_by", new_column_name="created_by_id", schema=schema)
    op.alter_column(f"{prefix}transform", column_name="created_by", new_column_name="created_by_id", schema=schema)
    op.alter_column(f"{prefix}project", column_name="created_by", new_column_name="created_by_id", schema=schema)
    op.add_column(f"{prefix}file", sa.Column("created_by_id", sqm.sql.sqltypes.AutoString(), nullable=True))
    op.add_column(f"{prefix}storage", sa.Column("created_by_id", sqm.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    pass
