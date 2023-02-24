"""v0.28.7."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

revision = "873683a29806"
down_revision = "3dd9f8d41861"


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    with op.batch_alter_table(f"{prefix}dobject", schema=schema) as batch_op:
        batch_op.create_unique_constraint("uq_storage__objectkey_suffix", ["storage_id", "_objectkey", "suffix"])


def downgrade() -> None:
    pass
