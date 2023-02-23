"""v0.28.3."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

revision = "3dd9f8d41861"
down_revision = "24e55331f27c"


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    op.rename_table(f"{prefix}dobjects_features", f"{prefix}dobject_features", schema=schema)


def downgrade() -> None:
    pass
