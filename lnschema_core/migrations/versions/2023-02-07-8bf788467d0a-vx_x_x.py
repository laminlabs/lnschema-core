"""v0.26.0.

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

    if sqlite:
        op.create_table(
            f"{prefix}dfolder",
            sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(
                ["created_by"],
                ["core.user.id"],
                name=op.f("fk_core.dfolder_created_by_user"),
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_core.dfolder")),
            schema=schema,
        )
        with op.batch_alter_table(f"{prefix}dfolder", schema=schema) as batch_op:
            batch_op.create_index(batch_op.f("ix_core.dfolder_created_at"), ["created_at"], unique=False)
            batch_op.create_index(batch_op.f("ix_core.dfolder_created_by"), ["created_by"], unique=False)
            batch_op.create_index(batch_op.f("ix_core.dfolder_name"), ["name"], unique=False)
            batch_op.create_index(batch_op.f("ix_core.dfolder_updated_at"), ["updated_at"], unique=False)

        op.create_table(
            f"{prefix}project_dfolder",
            sa.Column("project_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("dfolder_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.ForeignKeyConstraint(
                ["dfolder_id"],
                ["core.dfolder.id"],
                name=op.f("fk_core.project_dfolder_dfolder_id_dfolder"),
            ),
            sa.ForeignKeyConstraint(
                ["project_id"],
                ["core.project.id"],
                name=op.f("fk_core.project_dfolder_project_id_project"),
            ),
            sa.PrimaryKeyConstraint("project_id", "dfolder_id", name=op.f("pk_core.project_dfolder")),
            schema=schema,
        )
        op.create_table(
            f"{prefix}dfolder_dobject",
            sa.Column("dfolder_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("dobject_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.ForeignKeyConstraint(
                ["dfolder_id"],
                ["core.dfolder.id"],
                name=op.f("fk_core.dfolder_dobject_dfolder_id_dfolder"),
            ),
            sa.ForeignKeyConstraint(
                ["dobject_id"],
                ["core.dobject.id"],
                name=op.f("fk_core.dfolder_dobject_dobject_id_dobject"),
            ),
            sa.PrimaryKeyConstraint("dfolder_id", "dobject_id", name=op.f("pk_core.dfolder_dobject")),
            schema=schema,
        )
        with op.batch_alter_table(f"{prefix}dset", schema=schema) as batch_op:
            batch_op.drop_index("ix_core.dset_created_at")
            batch_op.drop_index("ix_core.dset_created_by")
            batch_op.drop_index("ix_core.dset_name")
            batch_op.drop_index("ix_core.dset_updated_at")
    else:
        op.create_table(
            f"{prefix}dfolder",
            sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(
                ["created_by"],
                ["core.user.id"],
                name=op.f("fk_core_dfolder_created_by_user"),
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_core_dfolder")),
            schema=schema,
        )
        with op.batch_alter_table(f"{prefix}dfolder", schema=schema) as batch_op:
            batch_op.create_index(batch_op.f("ix_core_dfolder_created_at"), ["created_at"], unique=False)
            batch_op.create_index(batch_op.f("ix_core_dfolder_created_by"), ["created_by"], unique=False)
            batch_op.create_index(batch_op.f("ix_core_dfolder_name"), ["name"], unique=False)
            batch_op.create_index(batch_op.f("ix_core_dfolder_updated_at"), ["updated_at"], unique=False)

        op.create_table(
            f"{prefix}project_dfolder",
            sa.Column("project_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("dfolder_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.ForeignKeyConstraint(
                ["dfolder_id"],
                ["core.dfolder.id"],
                name=op.f("fk_core_project_dfolder_dfolder_id_dfolder"),
            ),
            sa.ForeignKeyConstraint(
                ["project_id"],
                ["core.project.id"],
                name=op.f("fk_core.project_dfolder_project_id_project"),
            ),
            sa.PrimaryKeyConstraint("project_id", "dfolder_id", name=op.f("pk_core_project_dfolder")),
            schema=schema,
        )
        op.create_table(
            f"{prefix}dfolder_dobject",
            sa.Column("dfolder_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("dobject_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.ForeignKeyConstraint(
                ["dfolder_id"],
                ["core.dfolder.id"],
                name=op.f("fk_core_dfolder_dobject_dfolder_id_dfolder"),
            ),
            sa.ForeignKeyConstraint(
                ["dobject_id"],
                ["core.dobject.id"],
                name=op.f("fk_core_dfolder_dobject_dobject_id_dobject"),
            ),
            sa.PrimaryKeyConstraint("dfolder_id", "dobject_id", name=op.f("pk_core_dfolder_dobject")),
            schema=schema,
        )
        with op.batch_alter_table(f"{prefix}dset", schema=schema) as batch_op:
            batch_op.drop_index("ix_core_dset_created_at")
            batch_op.drop_index("ix_core_dset_created_by")
            batch_op.drop_index("ix_core_dset_name")
            batch_op.drop_index("ix_core_dset_updated_at")

    op.drop_table("core.dset")
    op.drop_table("core.dset_dobject")
    op.drop_table("core.project_dset")


def downgrade() -> None:
    pass
