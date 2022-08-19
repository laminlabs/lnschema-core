"""Add storage table.

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
        sa.Column("id", sa.BIGINT, nullable=False),
        sa.Column("root", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("region", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.Column("time_updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    pass
