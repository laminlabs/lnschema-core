"""v0.25.9.

Revision ID: 8bf788467d0a
Revises: 9d283a1685a5
Create Date: 2023-02-07 14:56:26.461590

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8bf788467d0a"
down_revision = "9d283a1685a5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    op.rename_table(old_table_name=f"{prefix}dset", new_table_name=f"{prefix}dfolder", schema=schema)
    op.rename_table(
        old_table_name=f"{prefix}dset_dobject",
        new_table_name=f"{prefix}dfolder_dobject",
        schema=schema,
    )
    op.rename_table(
        old_table_name=f"{prefix}project_dset",
        new_table_name=f"{prefix}project_dfolder",
        schema=schema,
    )
    op.alter_column(
        f"{prefix}dfolder_dobject",
        column_name="dset_id",
        new_column_name="dfolder_id",
        schema=schema,
    )
    op.alter_column(
        f"{prefix}project_dfolder",
        column_name="dset_id",
        new_column_name="dfolder_id",
        schema=schema,
    )
    if sqlite:
        op.drop_index("ix_core.dset_created_at", table_name=f"{prefix}dfolder", schema=schema)
        op.drop_index("ix_core.dset_created_by", table_name=f"{prefix}dfolder", schema=schema)
        op.drop_index("ix_core.dset_name", table_name=f"{prefix}dfolder", schema=schema)
        op.drop_index("ix_core.dset_updated_at", table_name=f"{prefix}dfolder", schema=schema)
        op.create_index(
            op.f("ix_core.dfolder_created_at"),
            f"{prefix}dfolder",
            ["created_at"],
            unique=False,
            schema=schema,
        )
        op.create_index(
            op.f("ix_core.dfolder_created_by"),
            f"{prefix}dfolder",
            ["created_by"],
            unique=False,
            schema=schema,
        )
        op.create_index(
            op.f("ix_core.dfolder_name"),
            f"{prefix}dfolder",
            ["name"],
            unique=False,
            schema=schema,
        )
        op.create_index(
            op.f("ix_core.dfolder_updated_at"),
            f"{prefix}dfolder",
            ["updated_at"],
            unique=False,
            schema=schema,
        )
    else:
        op.drop_index("ix_core_dset_created_at", table_name=f"{prefix}dfolder", schema=schema)
        op.drop_index("ix_core_dset_created_by", table_name=f"{prefix}dfolder", schema=schema)
        op.drop_index("ix_core_dset_name", table_name=f"{prefix}dfolder", schema=schema)
        op.drop_index("ix_core_dset_updated_at", table_name=f"{prefix}dfolder", schema=schema)
        op.create_index(
            op.f("ix_core_dfolder_created_at"),
            f"{prefix}dfolder",
            ["created_at"],
            unique=False,
            schema=schema,
        )
        op.create_index(
            op.f("ix_core_dfolder_created_by"),
            f"{prefix}dfolder",
            ["created_by"],
            unique=False,
            schema=schema,
        )
        op.create_index(
            op.f("ix_core_dfolder_name"),
            f"{prefix}dfolder",
            ["name"],
            unique=False,
            schema=schema,
        )
        op.create_index(
            op.f("ix_core_dfolder_updated_at"),
            f"{prefix}dfolder",
            ["updated_at"],
            unique=False,
            schema=schema,
        )


def downgrade() -> None:
    pass
