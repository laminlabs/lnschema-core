"""v0.16.0.

Revision ID: 4ee426b656bb
Revises: 98da12fc80a8
Create Date: 2022-11-10 15:09:46.416764

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4ee426b656bb"
down_revision = "98da12fc80a8"
branch_labels = None
depends_on = None


def upgrade_sqlite() -> None:
    op.rename_table("core.pipeline_run", "core.run")
    op.alter_column("core.dtransform", column_name="pipeline_run_id", new_column_name="run_id")

    # clean up names
    with op.batch_alter_table("core.dobject", schema=None) as batch_op:
        batch_op.drop_index("ix_dobject_checksum")
        batch_op.drop_index("ix_dobject_created_at")
        batch_op.drop_index("ix_dobject_dtransform_id")
        batch_op.drop_index("ix_dobject_name")
        batch_op.drop_index("ix_dobject_size")
        batch_op.drop_index("ix_dobject_storage_id")
        batch_op.drop_index("ix_dobject_suffix")
        batch_op.drop_index("ix_dobject_updated_at")
        batch_op.create_index(batch_op.f("ix_core.dobject_checksum"), ["checksum"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dobject_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dobject_dtransform_id"), ["dtransform_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dobject_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dobject_size"), ["size"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dobject_storage_id"), ["storage_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dobject_suffix"), ["suffix"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dobject_updated_at"), ["updated_at"], unique=False)

    with op.batch_alter_table("core.dset", schema=None) as batch_op:
        batch_op.drop_index("ix_dset_created_at")
        batch_op.drop_index("ix_dset_created_by")
        batch_op.drop_index("ix_dset_name")
        batch_op.drop_index("ix_dset_updated_at")
        batch_op.create_index(batch_op.f("ix_core.dset_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dset_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dset_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dset_updated_at"), ["updated_at"], unique=False)

    with op.batch_alter_table("core.dtransform", schema=None) as batch_op:
        batch_op.drop_index("ix_dtransform_jupynb_id")
        batch_op.drop_index("ix_dtransform_jupynb_v")
        batch_op.drop_index("ix_dtransform_pipeline_run_id")
        batch_op.create_index(batch_op.f("ix_core.dtransform_jupynb_id"), ["jupynb_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dtransform_jupynb_v"), ["jupynb_v"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dtransform_run_id"), ["run_id"], unique=False)
        # the following line should be built in already into the alter_column in l. 21
        # batch_op.create_foreign_key(
        #    batch_op.f('fk_core.dtransform_run_id_run'), 'core.run', ['run_id'], ['id']
        # )

    with op.batch_alter_table("core.jupynb", schema=None) as batch_op:
        batch_op.drop_index("ix_jupynb_created_at")
        batch_op.drop_index("ix_jupynb_created_by")
        batch_op.drop_index("ix_jupynb_name")
        batch_op.drop_index("ix_jupynb_updated_at")
        batch_op.create_index(batch_op.f("ix_core.jupynb_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.jupynb_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.jupynb_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.jupynb_updated_at"), ["updated_at"], unique=False)

    with op.batch_alter_table("core.pipeline", schema=None) as batch_op:
        batch_op.drop_index("ix_pipeline_created_at")
        batch_op.drop_index("ix_pipeline_created_by")
        batch_op.drop_index("ix_pipeline_name")
        batch_op.drop_index("ix_pipeline_reference")
        batch_op.drop_index("ix_pipeline_updated_at")
        batch_op.create_index(batch_op.f("ix_core.pipeline_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.pipeline_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.pipeline_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.pipeline_reference"), ["reference"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.pipeline_updated_at"), ["updated_at"], unique=False)

    with op.batch_alter_table("core.project", schema=None) as batch_op:
        batch_op.drop_index("ix_project_created_at")
        batch_op.drop_index("ix_project_created_by")
        batch_op.drop_index("ix_project_name")
        batch_op.drop_index("ix_project_updated_at")
        batch_op.create_index(batch_op.f("ix_core.project_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.project_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.project_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.project_updated_at"), ["updated_at"], unique=False)

    with op.batch_alter_table("core.run", schema=None) as batch_op:
        batch_op.drop_index("ix_pipeline_run_created_at")
        batch_op.drop_index("ix_pipeline_run_created_by")
        batch_op.drop_index("ix_pipeline_run_name")
        batch_op.drop_index("ix_pipeline_run_pipeline_id")
        batch_op.drop_index("ix_pipeline_run_pipeline_v")
        batch_op.create_index(batch_op.f("ix_core.run_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_pipeline_id"), ["pipeline_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_pipeline_v"), ["pipeline_v"], unique=False)

    with op.batch_alter_table("core.storage", schema=None) as batch_op:
        batch_op.drop_index("ix_storage_created_at")
        batch_op.drop_index("ix_storage_root")
        batch_op.drop_index("ix_storage_updated_at")
        batch_op.create_index(batch_op.f("ix_core.storage_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.storage_root"), ["root"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.storage_updated_at"), ["updated_at"], unique=False)

    with op.batch_alter_table("core.usage", schema=None) as batch_op:
        batch_op.drop_index("ix_usage_dobject_id")
        batch_op.drop_index("ix_usage_time")
        batch_op.drop_index("ix_usage_type")
        batch_op.drop_index("ix_usage_user_id")
        batch_op.create_index(batch_op.f("ix_core.usage_dobject_id"), ["dobject_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.usage_time"), ["time"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.usage_type"), ["type"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.usage_user_id"), ["user_id"], unique=False)

    with op.batch_alter_table("core.user", schema=None) as batch_op:
        batch_op.drop_index("ix_user_created_at")
        batch_op.drop_index("ix_user_email")
        batch_op.drop_index("ix_user_handle")
        batch_op.drop_index("ix_user_name")
        batch_op.drop_index("ix_user_updated_at")
        batch_op.create_index(batch_op.f("ix_core.user_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.user_email"), ["email"], unique=True)
        batch_op.create_index(batch_op.f("ix_core.user_handle"), ["handle"], unique=True)
        batch_op.create_index(batch_op.f("ix_core.user_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.user_updated_at"), ["updated_at"], unique=False)


def upgrade_postgres():
    op.rename_table("pipeline_run", "run", schema="core")
    op.alter_column(
        "dtransform",
        column_name="pipeline_run_id",
        new_column_name="run_id",
        schema="core",
    )


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        upgrade_sqlite()
    else:
        upgrade_postgres()


def downgrade() -> None:
    pass
