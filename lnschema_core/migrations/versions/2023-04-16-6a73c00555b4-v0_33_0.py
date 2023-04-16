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
    op.drop_index(f"ix_core{delim}features_created_by", table_name="features", schema="core")
    op.create_index(op.f(f"ix_core{delim}features_created_by_id"), "features", ["created_by_id"], unique=False, schema=schema)

    op.alter_column(f"{prefix}transform", column_name="created_by", new_column_name="created_by_id", schema=schema)
    op.alter_column(f"{prefix}project", column_name="created_by", new_column_name="created_by_id", schema=schema)
    op.add_column(f"{prefix}file", sa.Column("created_by_id", sqm.sql.sqltypes.AutoString(), nullable=True), schema=schema)
    op.add_column(f"{prefix}file", sa.Column("transform_id", sqm.sql.sqltypes.AutoString(), nullable=True), schema=schema)
    op.add_column(f"{prefix}file", sa.Column("transform_version", sqm.sql.sqltypes.AutoString(), nullable=True), schema=schema)
    op.alter_column("file", "run_id", existing_type=sqm.sql.sqltypes.AutoString(), nullable=True, schema="core")
    op.create_index(op.f(f"ix_core{delim}file_created_by_id"), "file", ["created_by_id"], unique=False, schema="core")
    # op.add_column(f"{prefix}storage", sa.Column("created_by_id", sqm.sql.sqltypes.AutoString(), nullable=True), schema=schema)

    with op.batch_alter_table(f"{prefix}file", schema=schema) as batch_op:
        batch_op.create_foreign_key(op.f(f"fk_file{delim}created_by_id_user"), "user", ["created_by_id"], ["id"], referent_schema=schema)

    op.drop_index(f"ix_core{delim}project_created_by", table_name="project", schema="core")
    op.create_index(op.f(f"ix_core{delim}project_created_by_id"), "project", ["created_by_id"], unique=False, schema="core")
    op.drop_index(f"ix_core{delim}run_created_by", table_name="run", schema="core")
    op.create_index(op.f(f"ix_core{delim}run_created_by_id"), "run", ["created_by_id"], unique=False, schema="core")
    op.drop_index(f"ix_core{delim}transform_created_by", table_name="transform", schema="core")
    op.create_index(op.f(f"ix_core{delim}transform_created_by_id"), "transform", ["created_by_id"], unique=False, schema="core")
    op.drop_index(f"ix_core{delim}folder_created_by", table_name="folder", schema="core")
    op.create_index(op.f(f"ix_core{delim}folder_created_by_id"), "folder", ["created_by_id"], unique=False, schema="core")
    op.create_index(op.f(f"ix_core{delim}file_transform_id"), "file", ["transform_id"], unique=False, schema=schema)

    op.alter_column(f"{prefix}transform", column_name="v", new_column_name="version", schema=schema)
    op.alter_column(f"{prefix}run", column_name="transform_v", new_column_name="transform_version", schema=schema)

    with op.batch_alter_table(f"{prefix}file", schema=schema) as batch_op:
        batch_op.create_foreign_key(
            op.f("fk_file_transform_id_version_transform"), "transform", ["transform_id", "transform_version"], ["id", "version"], referent_schema=schema
        )


def downgrade() -> None:
    pass
