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
    op.rename_table(old_table_name=f"{prefix}project_dfolder", new_table_name=f"{prefix}project_folder", schema=schema)
    op.rename_table(old_table_name=f"{prefix}dfolder_dobject", new_table_name=f"{prefix}folder_file", schema=schema)
    op.rename_table(old_table_name=f"{prefix}dobject_features", new_table_name=f"{prefix}file_features", schema=schema)

    try:
        op.drop_index(f"ix_core{delim}dobject__objectkey", table_name=f"{prefix}file", schema=schema)
        op.drop_index(f"ix_core{delim}dobject_created_at", table_name=f"{prefix}file", schema=schema)
        op.drop_index(f"ix_core{delim}dobject_hash", table_name=f"{prefix}file", schema=schema)
        op.drop_index(f"ix_core{delim}dobject_name", table_name=f"{prefix}file", schema=schema)
        op.drop_index(f"ix_core{delim}dobject_size", table_name=f"{prefix}file", schema=schema)
        op.drop_index(f"ix_core{delim}dobject_source_id", table_name=f"{prefix}file", schema=schema)
        op.drop_index(f"ix_core{delim}dobject_storage_id", table_name=f"{prefix}file", schema=schema)
        op.drop_index(f"ix_core{delim}dobject_suffix", table_name=f"{prefix}file", schema=schema)
        op.drop_index(f"ix_core{delim}dobject_updated_at", table_name=f"{prefix}file", schema=schema)
    except Exception:
        pass
    op.create_index(op.f(f"ix_core{delim}file__objectkey"), "file", ["_objectkey"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}file_created_at"), "file", ["created_at"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}file_hash"), "file", ["hash"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}file_name"), "file", ["name"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}file_size"), "file", ["size"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}file_source_id"), "file", ["source_id"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}file_storage_id"), "file", ["storage_id"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}file_suffix"), "file", ["suffix"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}file_updated_at"), "file", ["updated_at"], unique=False, schema=schema)
    try:
        op.drop_index(f"ix_core{delim}dfolder__objectkey", table_name=f"{prefix}folder", schema=schema)
        op.drop_index(f"ix_core{delim}dfolder_created_at", table_name=f"{prefix}folder", schema=schema)
        op.drop_index(f"ix_core{delim}dfolder_created_by", table_name=f"{prefix}folder", schema=schema)
        op.drop_index(f"ix_core{delim}dfolder_name", table_name=f"{prefix}folder", schema=schema)
        op.drop_index(f"ix_core{delim}dfolder_updated_at", table_name=f"{prefix}folder", schema=schema)
    except Exception:
        pass
    op.create_index(op.f(f"ix_core{delim}folder__objectkey"), "folder", ["_objectkey"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}folder_created_at"), "folder", ["created_at"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}folder_created_by"), "folder", ["created_by"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}folder_name"), "folder", ["name"], unique=False, schema=schema)
    op.create_index(op.f(f"ix_core{delim}folder_updated_at"), "folder", ["updated_at"], unique=False, schema=schema)

    with op.batch_alter_table(f"{prefix}folder_file", schema=schema) as batch_op:
        batch_op.alter_column(column_name="dobject_id", new_column_name="file_id")
        batch_op.alter_column(column_name="dfolder_id", new_column_name="folder_id")
        batch_op.drop_constraint("fk_dfolder_dobject_dobject_id_dobject", type_="foreignkey")
        batch_op.drop_constraint("fk_dfolder_dobject_dfolder_id_dfolder", type_="foreignkey")
        batch_op.create_foreign_key(op.f("fk_folder_file_file_id_file"), f"{prefix}file", ["file_id"], ["id"], referent_schema=schema)
        batch_op.create_foreign_key(op.f("fk_folder_file_folder_id_folder"), f"{prefix}folder", ["folder_id"], ["id"], referent_schema=schema)

    with op.batch_alter_table(f"{prefix}file_features", schema=schema) as batch_op:
        batch_op.alter_column(column_name="dobject_id", new_column_name="file_id")
        batch_op.drop_constraint("fk_dobject_features_dobject_id_dobject", type_="foreignkey")
        batch_op.create_foreign_key(op.f("fk_file_features_file_id_file"), f"{prefix}file", ["file_id"], ["id"], referent_schema=schema)

    with op.batch_alter_table(f"{prefix}project_folder", schema=schema) as batch_op:
        batch_op.alter_column(column_name="dfolder_id", new_column_name="folder_id")
        batch_op.drop_constraint("fk_project_dfolder_dfolder_id_dfolder", type_="foreignkey")
        batch_op.create_foreign_key(op.f("fk_project_folder_folder_id_folder"), f"{prefix}folder", ["folder_id"], ["id"], referent_schema=schema)

    with op.batch_alter_table(f"{prefix}run_in", schema=schema) as batch_op:
        batch_op.alter_column(column_name="dobject_id", new_column_name="file_id")
        batch_op.drop_constraint("fk_run_in_dobject_id_dobject", type_="foreignkey")
        batch_op.create_foreign_key(op.f("fk_run_in_file_id_file"), f"{prefix}file", ["file_id"], ["id"], referent_schema=schema)


def downgrade() -> None:
    pass
