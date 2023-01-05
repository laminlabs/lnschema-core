"""v0.14.0.

Revision ID: cf5913791674
Revises: 2ddcb037e3ea
Create Date: 2022-10-19 19:21:27.015737

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cf5913791674"
down_revision = "2ddcb037e3ea"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dset",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("dset", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_dset_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_dset_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_dset_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_dset_updated_at"), ["updated_at"], unique=False)

    op.create_table(
        "project",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_project_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_project_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_project_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_project_updated_at"), ["updated_at"], unique=False)

    op.create_table(
        "project_dset",
        sa.Column("project_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dset_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dset_id"],
            ["dset.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("project_id", "dset_id"),
    )

    op.create_table(
        "dset_dobject",
        sa.Column("dset_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dobject_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dobject_id"],
            ["dobject.id"],
        ),
        sa.ForeignKeyConstraint(
            ["dset_id"],
            ["dset.id"],
        ),
        sa.PrimaryKeyConstraint("dset_id", "dobject_id"),
    )


def downgrade() -> None:
    pass
