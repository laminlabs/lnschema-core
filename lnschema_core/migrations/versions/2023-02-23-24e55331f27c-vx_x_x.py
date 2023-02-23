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

    if sqlite:
        with op.batch_alter_table(f"{prefix}dobject", schema=schema) as batch_op:
            batch_op.drop_index("ix_core.dobject__filekey")
            batch_op.create_index(batch_op.f("ix_core.dobject__objectkey"), ["_objectkey"], unique=False)
        with op.batch_alter_table(f"{prefix}dfolder", schema=schema) as batch_op:
            batch_op.drop_index("ix_core.dfolder__folderkey")
            batch_op.create_index(batch_op.f("ix_core.dfolder__objectkey"), ["_objectkey"], unique=False)
    else:
        op.drop_index("ix_core_dobject__filekey", table_name="dobject", schema="core")
        op.create_index(
            op.f("ix_core_dobject__objectkey"),
            "dobject",
            ["_objectkey"],
            unique=False,
            schema="core",
        )
        op.drop_index("ix_core_dfolder__folderkey", table_name="dfolder", schema="core")
        op.create_index(
            op.f("ix_core_dfolder__objectkey"),
            "dfolder",
            ["_objectkey"],
            unique=False,
            schema=schema,
        )


def downgrade() -> None:
    pass
