"""Rename table interface to jupynb.

Revision ID: 0560ee3d73dc
Revises:
Create Date: 2022-07-21 22:25:40.022247

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "0560ee3d73dc"
down_revision = None
branch_labels = None
depends_on = None


# the whole migration strategy relies on copy so heavily
# because SQLite doesn't support altering constraints


def upgrade() -> None:
    # rename interface to jupynb
    op.create_table(
        "jupynb",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.Column("time_updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id", "v"),
    )
    op.execute("insert into jupynb select * from interface")
    op.drop_table("interface")

    # fix references in dobject
    op.create_table(
        "dobject_",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("file_suffix", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("jupynb_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("jupynb_v", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.Column("time_updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["jupynb_id", "jupynb_v"], ["jupynb.id", "jupynb.v"], name="dobject_jupynb"),
        sa.PrimaryKeyConstraint("id", "v"),
    )
    op.execute("insert into dobject_ select * from dobject")
    op.drop_table("dobject")
    op.rename_table("dobject_", "dobject")

    # fix references in track_do
    op.create_table(
        "track_do_",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("jupynb_id", sqlmodel.sql.sqltypes.AutoString()),
        sa.Column("jupynb_v", sqlmodel.sql.sqltypes.AutoString()),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("dobject_id", sqlmodel.sql.sqltypes.AutoString()),
        sa.Column("dobject_v", sqlmodel.sql.sqltypes.AutoString()),
        sa.ForeignKeyConstraint(
            ["dobject_id", "dobject_v"],
            ["dobject.id", "dobject.v"],
            name="track_do_dobject",
        ),
        sa.ForeignKeyConstraint(["jupynb_id", "jupynb_v"], ["jupynb.id", "jupynb.v"], name="track_do_jupynb"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute("insert into track_do_ (id, type, user_id, jupynb_id, time, dobject_id) select id, type, user_id, interface_id, time, dobject_id from track_do")
    op.execute("update track_do_ SET jupynb_v = '1'")
    op.execute("update track_do_ SET dobject_v = '1'")
    op.drop_table("track_do")
    op.rename_table("track_do_", "track_do")


def downgrade() -> None:
    pass
