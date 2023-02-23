"""v0.28.2."""
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
        new_column_name="_objectkey",
        schema=schema,
    )
    op.alter_column(
        f"{prefix}dfolder",
        column_name="_folderkey",
        new_column_name="_objectkey",
        schema=schema,
    )

    if sqlite:
        drop_index_filekey = "ix_core.dobject__filekey"
        drop_index_folderkey = "ix_core.dfolder__folderkey"
        create_index_objectkey_dobject = "ix_core.dobject__objectkey"
        create_index_objectkey_dfolder = "ix_core.dfolder__objectkey"
    else:
        drop_index_filekey = "ix_core_dobject__filekey"
        drop_index_folderkey = "ix_core_dfolder__folderkey"
        create_index_objectkey_dobject = "ix_core_dobject__objectkey"
        create_index_objectkey_dfolder = "ix_core_dfolder__objectkey"

        with op.batch_alter_table(f"{prefix}dobject", schema=schema) as batch_op:
            batch_op.drop_index(drop_index_filekey)
            batch_op.create_index(batch_op.f(create_index_objectkey_dobject), ["_objectkey"], unique=False)
        with op.batch_alter_table(f"{prefix}dfolder", schema=schema) as batch_op:
            batch_op.drop_index(drop_index_folderkey)
            batch_op.create_index(batch_op.f(create_index_objectkey_dfolder), ["_objectkey"], unique=False)


def downgrade() -> None:
    pass
