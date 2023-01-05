"""v0.3.0.

Revision ID: 8c78543d1c5b
Revises: 0560ee3d73dc
Create Date: 2022-08-08 15:45:42.737438

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "8c78543d1c5b"
down_revision = "0560ee3d73dc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Completely new table
    op.create_table(
        "pipeline",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id", "v"),
    )

    # New table where we can insert one row from the old schema_version
    op.create_table(
        "version_yvzi",
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("v"),
    )
    op.execute("insert into version_yvzi select id, user_id, time_created from schema_version")
    op.drop_table("schema_version")

    # New table where we need to insert a link to dobject and to jupynb
    op.create_table(
        "dtransform",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("jupynb_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("jupynb_v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("pipeline_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("pipeline_v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["jupynb_id", "jupynb_v"],
            ["jupynb.id", "jupynb.v"],
            name="dtransform_jupynb",
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id", "pipeline_v"],
            ["pipeline.id", "pipeline.v"],
            name="dtransform_pipeline",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dtransform_in",
        sa.Column("dtransform_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dobject_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dobject_v", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dobject_id", "dobject_v"],
            ["dobject.id", "dobject.v"],
            name="dtransform_in_dobject",
        ),
        sa.ForeignKeyConstraint(
            ["dtransform_id"],
            ["dtransform.id"],
        ),
        sa.PrimaryKeyConstraint("dtransform_id", "dobject_id", "dobject_v"),
    )
    op.create_table(
        "dtransform_out",
        sa.Column("dtransform_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dobject_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dobject_v", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dobject_id", "dobject_v"],
            ["dobject.id", "dobject.v"],
            name="dtransform_out_dobject",
        ),
        sa.ForeignKeyConstraint(
            ["dtransform_id"],
            ["dtransform.id"],
        ),
        sa.PrimaryKeyConstraint("dtransform_id", "dobject_id", "dobject_v"),
    )
    op.execute("insert into dtransform (id, jupynb_id, jupynb_v) select id, id, v from jupynb")

    # Add the dsouce_id column and insert data
    op.create_table(
        "dobject_",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("file_suffix", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dsource_id", sqlmodel.sql.sqltypes.AutoString()),
        sa.Column("jupynb_id", sqlmodel.sql.sqltypes.AutoString()),
        sa.Column("jupynb_v", sqlmodel.sql.sqltypes.AutoString()),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.Column("time_updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dsource_id"],
            ["dtransform.id"],
        ),
        sa.PrimaryKeyConstraint("id", "v"),
    )
    op.execute(
        "insert into dobject_(id, v, name, file_suffix, jupynb_id, jupynb_v,"
        " time_created, time_updated) select id, v, name, file_suffix, jupynb_id,"
        " jupynb_v, time_created, time_updated from dobject"
    )
    op.drop_table("dobject")
    op.rename_table("dobject_", "dobject")
    op.execute("update dobject set dsource_id = (select id from dtransform where (dtransform.jupynb_id, dtransform.jupynb_v) = (dobject.jupynb_id, dobject.jupynb_v))")
    # now we don't need these two columns anymore on dobject
    op.drop_column("dobject", "jupynb_v")
    op.drop_column("dobject", "jupynb_id")

    # Populate dtransform_out
    op.execute("insert into dtransform_out (dtransform_id, dobject_id, dobject_v) select dsource_id, id, v from dobject")

    # This is a rename from track_do, so we got to insert all data from track_do
    op.create_table(
        "usage",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("dobject_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dobject_v", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dobject_id", "dobject_v"],
            ["dobject.id", "dobject.v"],
            name="usage_dobject",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute("insert into usage (id, type, user_id, time, dobject_id, dobject_v) select id, type, user_id, time, dobject_id, dobject_v from track_do")
    op.drop_table("track_do")

    # jupynb table no longer has type
    op.drop_column("jupynb", "type")

    # User table gets a handle now
    op.add_column("user", sa.Column("handle", sqlmodel.sql.sqltypes.AutoString()))
    op.execute("update user set handle = 'falexwolf' where id = 'FBa7SHjn'")


def downgrade() -> None:
    pass
