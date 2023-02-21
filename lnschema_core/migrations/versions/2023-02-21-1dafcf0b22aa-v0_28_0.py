"""v0.28.0."""
from alembic import op
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa

revision = '1dafcf0b22aa'
down_revision = '8280855a5064'


def upgrade() -> None:
    op.alter_column("core.dobject", column_name="run_id", new_column_name="source_id")


def downgrade() -> None:
    pass
