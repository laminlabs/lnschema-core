"""v0.6.0.

Revision ID: 5fa54c55c3bf
Revises: d1b3e5da6391
Create Date: 2022-09-15 16:46:41.338263

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "5fa54c55c3bf"
down_revision = "d1b3e5da6391"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("alembic_version")
    op.add_column(
        "version_yvzi",
        sa.Column("migration", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )


def downgrade() -> None:
    pass
