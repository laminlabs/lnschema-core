"""v0.8.0.

Revision ID: 7e8f7b30792e
Revises: 1f29517759b7
Create Date: 2022-09-25 20:39:03.626212
"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7e8f7b30792e"
down_revision = "1f29517759b7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("dobject", schema=None) as batch_op:
        batch_op.add_column(sa.Column("size", sa.Float(), nullable=True))
        batch_op.create_index(batch_op.f("ix_dobject_size"), ["size"], unique=False)


def downgrade() -> None:
    with op.batch_alter_table("dobject", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_dobject_size"))
        batch_op.drop_column("size")
