"""v0.4.0.

Revision ID: 01fcb82dafd4
Revises: 1c531ea346cf
Create Date: 2022-08-22 16:01:42.592859

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "01fcb82dafd4"
down_revision = "1c531ea346cf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the new pipeline_run table
    op.create_table(
        "pipeline_run",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("pipeline")

    # Update the dtransform table

    # Drop the redundant dtransform_out table
    op.drop_table("dtransform_out")

    # Rename the dsource_id column to dtransform_id and add indexes
    op.create_table(
        "dobject_tmp",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "name", sqlmodel.sql.sqltypes.AutoString(), nullable=True, index=True
        ),
        sa.Column(
            "file_suffix",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
            index=True,
        ),
        sa.Column("dtransform_id", sqlmodel.sql.sqltypes.AutoString(), index=True),
        sa.Column("storage_root", sqlmodel.sql.sqltypes.AutoString(), index=True),
        sa.Column("time_created", sa.DateTime(), nullable=False, index=True),
        sa.Column("time_updated", sa.DateTime(), nullable=False, index=True),
        sa.ForeignKeyConstraint(
            ["dsource_id"],
            ["dtransform.id"],
        ),
        sa.ForeignKeyConstraint(
            ["storage_root"],
            ["storage.root"],
        ),
        sa.PrimaryKeyConstraint("id", "v"),
    )
    op.execute(
        "insert into dobject_tmp(id, v, name, file_suffix, dtransform_id,"
        " time_created, time_updated) select id, v, name, file_suffix, dsource_id,"
        " time_created, time_updated from dobject"
    )
    op.drop_table("dobject")
    op.rename_table("dobject_tmp", "dobject")

    op.create_index(op.f("ix_jupynb_name"), "jupynb", ["name"], unique=False)
    op.create_index(
        op.f("ix_jupynb_time_created"), "jupynb", ["time_created"], unique=False
    )
    op.create_index(
        op.f("ix_jupynb_time_updated"), "jupynb", ["time_updated"], unique=False
    )
    op.create_index(op.f("ix_jupynb_user_id"), "jupynb", ["user_id"], unique=False)
    op.create_index(op.f("ix_usage_dobject_id"), "usage", ["dobject_id"], unique=False)
    op.create_index(op.f("ix_usage_dobject_v"), "usage", ["dobject_v"], unique=False)
    op.create_index(op.f("ix_usage_time"), "usage", ["time"], unique=False)
    op.create_index(op.f("ix_usage_type"), "usage", ["type"], unique=False)
    op.create_index(op.f("ix_usage_user_id"), "usage", ["user_id"], unique=False)
    op.alter_column("user", "handle", existing_type=sa.VARCHAR(), nullable=False)
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=False)
    op.create_index(op.f("ix_user_handle"), "user", ["handle"], unique=False)
    op.create_unique_constraint(None, "user", ["handle"])


def downgrade() -> None:
    pass
