"""v0.11.0.

Revision ID: 3d244a8d3148
Revises: 0c819d33ca9b
Create Date: 2022-10-10 11:23:16.199020

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3d244a8d3148"
down_revision = "0c819d33ca9b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("name", sqlmodel.sql.sqltypes.AutoString()))
        batch_op.create_index(batch_op.f("ix_user_name"), ["name"], unique=False)


def downgrade() -> None:
    pass
