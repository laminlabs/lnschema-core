"""vX.X.X."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

revision = "24e55331f27c"
down_revision = "6952574e2d49"


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    op.alter_column(
        f"{prefix}dobject",
        column_name="_filekey",
        new_column_name="_dobjectkey",
        schema=schema,
    )
    op.alter_column(
        f"{prefix}dfolder",
        column_name="_folderkey",
        new_column_name="_dobjectkey",
        schema=schema,
    )


def downgrade() -> None:
    pass
