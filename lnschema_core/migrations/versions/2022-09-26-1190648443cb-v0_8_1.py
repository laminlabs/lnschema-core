"""v0.8.1.

Revision ID: 1190648443cb
Revises: 7e8f7b30792e
Create Date: 2022-09-26 13:39:13.069980
"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1190648443cb"
down_revision = "7e8f7b30792e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("jupynb", schema=None) as batch_op:
        batch_op.alter_column("name", existing_type=sa.VARCHAR(), nullable=False)


def downgrade() -> None:
    with op.batch_alter_table("jupynb", schema=None) as batch_op:
        batch_op.alter_column("name", existing_type=sa.VARCHAR(), nullable=True)
