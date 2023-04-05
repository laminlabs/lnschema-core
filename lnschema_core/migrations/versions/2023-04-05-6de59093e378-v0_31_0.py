"""v0.31.0."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "6de59093e378"
down_revision = "5846a15d9241"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    op.alter_column(f"{prefix}file", column_name="_objectkey", new_column_name="key", schema=schema)
    with op.batch_alter_table(f"{prefix}file", schema=schema) as batch_op:
        batch_op.drop_index("ix_core.file__objectkey")
        batch_op.drop_constraint("uq_storage__objectkey_suffix", type_="unique")
        batch_op.create_index(batch_op.f(f"ix_core{delim}file_key"), ["key"], unique=False)
        batch_op.create_unique_constraint("uq_storage_key", ["storage_id", "key"])


def downgrade() -> None:
    pass
