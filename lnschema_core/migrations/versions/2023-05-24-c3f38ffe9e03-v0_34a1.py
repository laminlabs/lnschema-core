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
        op.rename_table(old_table_name="user", new_table_name="lnschema_core_user", schema="core")
        op.rename_table(old_table_name="project", new_table_name="lnschema_core_project", schema="core")
        op.rename_table(old_table_name="storage", new_table_name="lnschema_core_storage", schema="core")
        op.rename_table(old_table_name="transform", new_table_name="lnschema_core_transform", schema="core")
        op.rename_table(old_table_name="run", new_table_name="lnschema_core_run", schema="core")
        op.rename_table(old_table_name="file", new_table_name="lnschema_core_file", schema="core")
        op.rename_table(old_table_name="folder", new_table_name="lnschema_core_folder", schema="core")
        op.rename_table(old_table_name="features", new_table_name="lnschema_core_features", schema="core")
        op.rename_table(old_table_name="run_in", new_table_name="lnschema_core_runinput", schema="core")
        op.rename_table(old_table_name="file_features", new_table_name="lnschema_core_filefeatures", schema="core")
        op.rename_table(old_table_name="project_folder", new_table_name="lnschema_core_projectfolder", schema="core")
        op.rename_table(old_table_name="folder_file", new_table_name="lnschema_core_folderfile", schema="core")
        # there seems to be a bug in alembic autogenerate that doesn't pick this up
        op.execute("alter table core.lnschema_core_user set schema public")
        op.execute("alter table core.lnschema_core_project set schema public")
        op.execute("alter table core.lnschema_core_storage set schema public")
        op.execute("alter table core.lnschema_core_transform set schema public")
        op.execute("alter table core.lnschema_core_run set schema public")
        op.execute("alter table core.lnschema_core_file set schema public")
        op.execute("alter table core.lnschema_core_folder set schema public")
        op.execute("alter table core.lnschema_core_features set schema public")
        op.execute("alter table core.lnschema_core_runinput set schema public")
        op.execute("alter table core.lnschema_core_filefeatures set schema public")
        op.execute("alter table core.lnschema_core_projectfolder set schema public")
        op.execute("alter table core.lnschema_core_folderfile set schema public")


def downgrade() -> None:
    pass
