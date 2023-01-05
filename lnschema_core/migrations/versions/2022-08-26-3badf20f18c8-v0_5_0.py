"""v0.5.0.

Revision ID: 3badf20f18c8
Revises: 01fcb82dafd4
Create Date: 2022-08-26 14:17:51.167740
"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "3badf20f18c8"
down_revision = "01fcb82dafd4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pipeline",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("reference", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id", "v"),
    )
    op.create_index(op.f("ix_pipeline_name"), "pipeline", ["name"], unique=False)
    op.create_index(op.f("ix_pipeline_reference"), "pipeline", ["reference"], unique=False)
    op.add_column("dobject", sa.Column("storage_id", sqlmodel.sql.sqltypes.AutoString()))
    op.alter_column("dobject", "dtransform_id", existing_type=sa.VARCHAR())
    op.drop_index("ix_dobject_tmp_dtransform_id", table_name="dobject")
    op.drop_index("ix_dobject_tmp_file_suffix", table_name="dobject")
    op.drop_index("ix_dobject_tmp_name", table_name="dobject")
    op.drop_index("ix_dobject_tmp_storage_root", table_name="dobject")
    op.drop_index("ix_dobject_tmp_time_created", table_name="dobject")
    op.drop_index("ix_dobject_tmp_time_updated", table_name="dobject")
    op.create_index(op.f("ix_dobject_dtransform_id"), "dobject", ["dtransform_id"], unique=False)
    op.create_index(op.f("ix_dobject_file_suffix"), "dobject", ["file_suffix"], unique=False)
    op.create_index(op.f("ix_dobject_name"), "dobject", ["name"], unique=False)
    op.create_index(op.f("ix_dobject_storage_id"), "dobject", ["storage_id"], unique=False)
    op.create_index(op.f("ix_dobject_time_created"), "dobject", ["time_created"], unique=False)
    op.create_index(op.f("ix_dobject_time_updated"), "dobject", ["time_updated"], unique=False)
    op.add_column(
        "pipeline_run",
        sa.Column("pipeline_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    )
    op.add_column(
        "pipeline_run",
        sa.Column("pipeline_v", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    )
    op.add_column(
        "pipeline_run",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.create_index(op.f("ix_pipeline_run_name"), "pipeline_run", ["name"], unique=False)
    op.create_index(
        op.f("ix_pipeline_run_pipeline_id"),
        "pipeline_run",
        ["pipeline_id"],
        unique=False,
    )
    op.create_index(op.f("ix_pipeline_run_pipeline_v"), "pipeline_run", ["pipeline_v"], unique=False)
    with op.batch_alter_table("pipeline") as batch_op:
        batch_op.create_foreign_key("pipeline_run", "pipeline", ["pipeline_id", "pipeline_v"], ["id", "v"])
    op.add_column("storage", sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.create_index(op.f("ix_storage_root"), "storage", ["root"], unique=False)
    op.alter_column("user", "handle", existing_type=sa.VARCHAR())
    with op.batch_alter_table("user") as batch_op:
        batch_op.create_unique_constraint("user", ["handle"])


def downgrade() -> None:
    pass
