"""v0.26.1.

Revision ID: ff3b5b3ec913
Revises: 8bf788467d0a
Create Date: 2023-02-10 11:27:41.135864

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ff3b5b3ec913"
down_revision = "8bf788467d0a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        op.rename_table("storage", "core.storage")
    else:
        op.execute("alter table public.storage set schema core")


def downgrade() -> None:
    pass
