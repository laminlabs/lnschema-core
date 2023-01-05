"""v0.7.0.

Revision ID: 3b60b87450c0
Revises: 5fa54c55c3bf
Create Date: 2022-09-18 15:57:25.104305
"""
import sqlalchemy as sa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3b60b87450c0"
down_revision = "5fa54c55c3bf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("dobject", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=True,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.alter_column("id", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("v", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("dtransform_id", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("storage_id", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.drop_index("ix_dobject_time_created")
        batch_op.drop_index("ix_dobject_time_updated")
        batch_op.create_index(batch_op.f("ix_dobject_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_dobject_updated_at"), ["updated_at"], unique=False)
        batch_op.create_foreign_key("fk_object_storage_id_storage", "storage", ["storage_id"], ["id"])
        batch_op.drop_column("time_created")
        batch_op.drop_column("time_updated")

    with op.batch_alter_table("dtransform", schema=None) as batch_op:
        batch_op.alter_column("id", existing_type=sa.VARCHAR(), nullable=False)

    with op.batch_alter_table("jupynb", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=True,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.alter_column("id", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("v", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.drop_index("ix_jupynb_time_created")
        batch_op.drop_index("ix_jupynb_time_updated")
        batch_op.create_index(batch_op.f("ix_jupynb_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_jupynb_updated_at"), ["updated_at"], unique=False)
        batch_op.drop_column("time_created")
        batch_op.drop_column("time_updated")

    with op.batch_alter_table("pipeline", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=True,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.alter_column("id", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("v", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.create_index(batch_op.f("ix_pipeline_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_pipeline_updated_at"), ["updated_at"], unique=False)
        batch_op.drop_column("time_created")

    with op.batch_alter_table("pipeline_run", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=True,
            )
        )
        batch_op.alter_column("id", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.create_index(batch_op.f("ix_pipeline_run_created_at"), ["created_at"], unique=False)
        batch_op.create_foreign_key("pipeline", "pipeline", ["pipeline_id", "pipeline_v"], ["id", "v"])
        batch_op.drop_column("time_created")

    with op.batch_alter_table("storage", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=True,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.alter_column("id", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.create_index(batch_op.f("ix_storage_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_storage_updated_at"), ["updated_at"], unique=False)
        batch_op.drop_column("time_created")
        batch_op.drop_column("time_updated")

    with op.batch_alter_table("usage", schema=None) as batch_op:
        batch_op.alter_column("id", existing_type=sa.VARCHAR(), nullable=False)

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=True,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.alter_column("id", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("handle", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.create_index(batch_op.f("ix_user_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_user_updated_at"), ["updated_at"], unique=False)
        batch_op.drop_column("time_created")
        batch_op.drop_column("time_updated")

    with op.batch_alter_table("version_yvzi", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=True,
            )
        )
        batch_op.alter_column("v", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.create_index(batch_op.f("ix_version_yvzi_created_at"), ["created_at"], unique=False)
        batch_op.drop_column("time_created")


def downgrade() -> None:
    pass
