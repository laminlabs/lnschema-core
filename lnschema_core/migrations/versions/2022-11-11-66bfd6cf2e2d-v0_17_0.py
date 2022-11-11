"""v0.17.0.

Revision ID: 66bfd6cf2e2d
Revises: 4ee426b656bb
Create Date: 2022-11-11 22:05:39.865585

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "66bfd6cf2e2d"
down_revision = "4ee426b656bb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("PRAGMA foreign_keys=OFF")
    with op.batch_alter_table("core.dtransform") as batch_op:
        batch_op.add_column(
            sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("pipeline_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("pipeline_v", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
        )
        batch_op.create_index(
            batch_op.f("ix_core.dtransform_pipeline_id"), ["pipeline_id"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_core.dtransform_pipeline_v"), ["pipeline_v"], unique=False
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_core.dtransform_pipeline_id_pipeline"),
            "core.pipeline",
            ["pipeline_id", "pipeline_v"],
            ["id", "v"],
        )
        batch_op.add_column(
            sa.Column(
                "created_by",
                sqlmodel.sql.sqltypes.AutoString(),
                nullable=False,
                default="9ypQ1yrW",
            )
        )
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.create_index(
            batch_op.f("ix_core.dtransform_created_at"), ["created_at"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_core.dtransform_created_by"), ["created_by"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_core.dtransform_name"), ["name"], unique=False
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_core.dtransform_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
        )

    op.execute(
        """
    update core.dtransform
    set core.dtransform.created_by = core.run.created_by,
    core.dtransform.created_at = core.dtransform.created_at,
    core.dtransform.name = core.run.name,
    core.dtransform.pipeline_id = core.run.pipeline_id,
    core.dtransform.pipeline_v = core.run.pipeline_v,
    from core.run
    where core.dtransform.run_id = core.run.id
    """
    )

    op.drop_table("core.run")

    op.rename_table(old_table_name="core.dtransform", new_table_name="core.run")
    op.rename_table(old_table_name="core.dtransform_in", new_table_name="core.run_in")
    op.alter_column(
        "core.dobject", column_name="dtransform_id", new_column_name="run_id"
    )
    op.execute("PRAGMA foreign_keys=ON")


def downgrade() -> None:
    pass
