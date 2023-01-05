"""v0.22.0.

Revision ID: db1df7b2aaad
Revises: 9d94f3b9566d
Create Date: 2022-12-07 01:40:35.071647

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "db1df7b2aaad"
down_revision = "9d94f3b9566d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
    else:
        prefix, schema = "", "core"

    op.rename_table(f"{prefix}jupynb", f"{prefix}notebook", schema=schema)

    with op.batch_alter_table(f"{prefix}notebook", schema=schema) as batch_op:
        batch_op.create_index(batch_op.f("ix_core.notebook_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.notebook_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.notebook_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.notebook_updated_at"), ["updated_at"], unique=False)
        batch_op.drop_index("ix_core.jupynb_created_at")
        batch_op.drop_index("ix_core.jupynb_created_by")
        batch_op.drop_index("ix_core.jupynb_name")
        batch_op.drop_index("ix_core.jupynb_updated_at")

    op.alter_column(
        f"{prefix}run",
        column_name="jupynb_id",
        new_column_name="notebook_id",
        schema=schema,
    )
    op.alter_column(
        f"{prefix}run",
        column_name="jupynb_v",
        new_column_name="notebook_v",
        schema=schema,
    )
    with op.batch_alter_table(f"{prefix}run", schema=schema) as batch_op:
        batch_op.drop_index("ix_core.run_jupynb_id")
        batch_op.drop_index("ix_core.run_jupynb_v")
        batch_op.create_index(batch_op.f("ix_core.run_notebook_id"), ["notebook_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_notebook_v"), ["notebook_v"], unique=False)
        batch_op.create_foreign_key(
            batch_op.f("fk_core.run_notebook_id_notebook"),
            "core.notebook",
            ["notebook_id", "notebook_v"],
            ["id", "v"],
        )


def downgrade() -> None:
    pass
