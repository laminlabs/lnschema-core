"""v0.10.0.

Revision ID: 0c819d33ca9b
Revises: 439c4ee0a22a
Create Date: 2022-10-07 12:47:10.583291

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0c819d33ca9b"
down_revision = "439c4ee0a22a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("jupynb", sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString()))
    op.execute("update jupynb set created_by = user_id")
    with op.batch_alter_table("jupynb", schema=None) as batch_op:
        batch_op.drop_index("ix_jupynb_user_id")
        batch_op.create_index(batch_op.f("ix_jupynb_created_by"), ["created_by"], unique=False)
        batch_op.create_foreign_key("fk_created_by", "user", ["created_by"], ["id"])
        batch_op.drop_column("user_id")

    with op.batch_alter_table("pipeline", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString()))
        batch_op.create_index(batch_op.f("ix_pipeline_created_by"), ["created_by"], unique=False)
        batch_op.create_foreign_key("fk_created_by", "user", ["created_by"], ["id"])

    with op.batch_alter_table("pipeline_run", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString()))
        batch_op.create_index(batch_op.f("ix_pipeline_run_created_by"), ["created_by"], unique=False)
        batch_op.create_foreign_key("fk_created_by", "user", ["created_by"], ["id"])

    with op.batch_alter_table("version_yvzi", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_version_yvzi_user_id"), ["user_id"], unique=False)


def downgrade() -> None:
    pass
