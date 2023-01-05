"""v0.5.1.

Revision ID: d1b3e5da6391
Revises: 3badf20f18c8
Create Date: 2022-08-29 19:35:13.905660

"""
import sqlalchemy as sa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d1b3e5da6391"
down_revision = "3badf20f18c8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("dobject") as batch_op:
        batch_op.drop_column("storage_root")
    op.add_column("pipeline", sa.Column("time_created", sa.DateTime(), nullable=False))
    op.add_column("pipeline_run", sa.Column("time_created", sa.DateTime(), nullable=False))
    with op.batch_alter_table("pipeline") as batch_op:
        batch_op.create_foreign_key("pipeline_run", "pipeline", ["pipeline_id", "pipeline_v"], ["id", "v"])


def downgrade() -> None:
    pass
