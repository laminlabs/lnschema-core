"""v0.34a1.

Reverts migration 0.15.0.
"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

revision = "c3f38ffe9e03"
down_revision = "6a73c00555b4"


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.rename_table(old_table_name="core.user", new_table_name="lnschema_core_user")
        op.rename_table(old_table_name="core.project", new_table_name="lnschema_core_project")
        op.rename_table(old_table_name="core.storage", new_table_name="lnschema_core_storage")
        op.rename_table(old_table_name="core.transform", new_table_name="lnschema_core_transform")
        op.rename_table(old_table_name="core.run", new_table_name="lnschema_core_run")
        op.rename_table(old_table_name="core.file", new_table_name="lnschema_core_file")
        op.rename_table(old_table_name="core.folder", new_table_name="lnschema_core_folder")
        op.rename_table(old_table_name="core.features", new_table_name="lnschema_core_features")
        op.rename_table(old_table_name="core.run_in", new_table_name="lnschema_core_runinput")
        op.rename_table(old_table_name="core.file_features", new_table_name="lnschema_core_filefeatures")
        op.rename_table(old_table_name="core.project_folder", new_table_name="lnschema_core_projectfolder")
        op.rename_table(old_table_name="core.folder_file", new_table_name="lnschema_core_folderfile")
    else:
        op.execute("alter table core.user set schema public")
        op.execute("alter table core.project set schema public")
        op.execute("alter table core.storage set schema public")
        op.execute("alter table core.transform set schema public")
        op.execute("alter table core.run set schema public")
        op.execute("alter table core.file set schema public")
        op.execute("alter table core.folder set schema public")
        op.execute("alter table core.features set schema public")
        op.execute("alter table core.run_in set schema public")
        op.execute("alter table core.file_features set schema public")
        op.execute("alter table core.project_folder set schema public")
        op.execute("alter table core.folder_file set schema public")


def downgrade() -> None:
    pass
