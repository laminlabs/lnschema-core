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
    op.create_table(
        "dtransform_tmp",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("jupynb_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("jupynb_v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("pipeline_run_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["jupynb_id", "jupynb_v"],
            ["jupynb.id", "jupynb.v"],
            name="dtransform_jupynb",
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_run_id"],
            ["pipeline_run.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute("insert into dtransform_tmp (id, jupynb_id, jupynb_v) select id, jupynb_id, jupynb_v from dtransform")
    op.drop_table("dtransform")
    op.rename_table("dtransform_tmp", "dtransform")
    op.create_index(op.f("ix_dtransform_jupynb_id"), "dtransform", ["jupynb_id"], unique=False)
    op.create_index(op.f("ix_dtransform_jupynb_v"), "dtransform", ["jupynb_v"], unique=False)
    op.create_index(
        op.f("ix_dtransform_pipeline_run_id"),
        "dtransform",
        ["pipeline_run_id"],
        unique=False,
    )

    # Drop the redundant dtransform_out table
    op.drop_table("dtransform_out")

    # Rename the dsource_id column to dtransform_id and add indexes
    op.create_table(
        "dobject_tmp",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True, index=True),
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
            ["dtransform_id"],
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

    # Create indexes on jupynb
    op.create_index(op.f("ix_jupynb_name"), "jupynb", ["name"], unique=False)
    op.create_index(op.f("ix_jupynb_time_created"), "jupynb", ["time_created"], unique=False)
    op.create_index(op.f("ix_jupynb_time_updated"), "jupynb", ["time_updated"], unique=False)
    op.create_index(op.f("ix_jupynb_user_id"), "jupynb", ["user_id"], unique=False)

    # Create indexes on usage
    op.create_index(op.f("ix_usage_dobject_id"), "usage", ["dobject_id"], unique=False)
    op.create_index(op.f("ix_usage_dobject_v"), "usage", ["dobject_v"], unique=False)
    op.create_index(op.f("ix_usage_time"), "usage", ["time"], unique=False)
    op.create_index(op.f("ix_usage_type"), "usage", ["type"], unique=False)
    op.create_index(op.f("ix_usage_user_id"), "usage", ["user_id"], unique=False)

    # Create indexes on user
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=False)
    op.create_index(op.f("ix_user_handle"), "user", ["handle"], unique=False)


def downgrade() -> None:
    pass
