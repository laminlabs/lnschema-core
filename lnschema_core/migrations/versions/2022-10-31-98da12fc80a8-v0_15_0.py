"""v0.15.0.

Revision ID: 98da12fc80a8
Revises: cf5913791674
Create Date: 2022-10-31
"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

revision = "98da12fc80a8"
down_revision = "cf5913791674"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.rename_table(old_table_name="dtransform", new_table_name="core.dtransform")
        op.rename_table(old_table_name="storage", new_table_name="core.storage")
        op.rename_table(old_table_name="user", new_table_name="core.user")
        op.rename_table(
            old_table_name="dtransform_in", new_table_name="core.dtransform_in"
        )
        op.rename_table(old_table_name="dobject", new_table_name="core.dobject")
        op.rename_table(old_table_name="usage", new_table_name="core.usage")
        op.rename_table(old_table_name="jupynb", new_table_name="core.jupynb")
        op.rename_table(old_table_name="pipeline", new_table_name="core.pipeline_run")
        op.rename_table(old_table_name="dset", new_table_name="core.dset")
        op.rename_table(old_table_name="project", new_table_name="core.project")
        op.rename_table(
            old_table_name="project_dset", new_table_name="core.project_dset"
        )
        op.rename_table(
            old_table_name="dset_dobject", new_table_name="core.dset_dobject"
        )
    else:
        pass


def downgrade() -> None:
    pass
