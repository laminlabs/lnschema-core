"""v0.12.0.

Revision ID: 2ddcb037e3ea
Revises: 3d244a8d3148
Create Date: 2022-10-11 17:33:37.731501

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2ddcb037e3ea"
down_revision = "3d244a8d3148"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("dobject", schema=None) as batch_op:
        batch_op.add_column(sa.Column("checksum", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(batch_op.f("ix_dobject_checksum"), ["checksum"], unique=False)


def downgrade() -> None:
    pass
