"""v0.3.3.

Revision ID: 1c531ea346cf
Revises: 8c78543d1c5b
Create Date: 2022-08-19 15:51:31.185793

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "1c531ea346cf"
down_revision = "8c78543d1c5b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Completely new table
    op.create_table(
        "storage",
        sa.Column("root", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("region", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.Column("time_updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("root"),
    )

    # Add storage_root column
    op.create_table(
        "dobject_tmp",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("file_suffix", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dsource_id", sqlmodel.sql.sqltypes.AutoString()),
        sa.Column("storage_root", sqlmodel.sql.sqltypes.AutoString()),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.Column("time_updated", sa.DateTime(), nullable=False),
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
        "insert into dobject_tmp(id, v, name, file_suffix, dsource_id,"
        " time_created, time_updated) select id, v, name, file_suffix, dsource_id,"
        " time_created, time_updated from dobject"
    )
    op.drop_table("dobject")
    op.rename_table("dobject_tmp", "dobject")


def downgrade() -> None:
    pass
