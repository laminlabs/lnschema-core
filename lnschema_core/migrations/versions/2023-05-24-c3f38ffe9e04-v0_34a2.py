"""v0.34a2."""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

revision = "c3f38ffe9e04"
down_revision = "c3f38ffe9e03"


def upgrade() -> None:
    bind = op.get_bind()
    if not bind.engine.name == "sqlite":
        op.rename_table(old_table_name="user", new_table_name="lnschema_core_user", schema="public")
        op.rename_table(old_table_name="project", new_table_name="lnschema_core_project", schema="public")
        op.rename_table(old_table_name="storage", new_table_name="lnschema_core_storage", schema="public")
        op.rename_table(old_table_name="transform", new_table_name="lnschema_core_transform", schema="public")
        op.rename_table(old_table_name="run", new_table_name="lnschema_core_run", schema="public")
        op.rename_table(old_table_name="file", new_table_name="lnschema_core_file", schema="public")
        op.rename_table(old_table_name="folder", new_table_name="lnschema_core_folder", schema="public")
        op.rename_table(old_table_name="features", new_table_name="lnschema_core_features", schema="public")
        op.rename_table(old_table_name="run_in", new_table_name="lnschema_core_runinput", schema="public")
        op.rename_table(old_table_name="file_features", new_table_name="lnschema_core_filefeatures", schema="public")
        op.rename_table(old_table_name="project_folder", new_table_name="lnschema_core_projectfolder", schema="public")
        op.rename_table(old_table_name="folder_file", new_table_name="lnschema_core_folderfile", schema="public")


def downgrade() -> None:
    pass
