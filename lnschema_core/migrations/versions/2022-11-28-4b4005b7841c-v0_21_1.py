"""v0.21.1.

Revision ID: 4b4005b7841c
Revises: 66bfd6cf2e2d
Create Date: 2022-11-28 00:38:59.653534

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4b4005b7841c"
down_revision = "66bfd6cf2e2d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "core.", None
        op.execute("PRAGMA foreign_keys=OFF")
    else:
        prefix, schema = "", "core"

    if sqlite:
        op.rename_table("core.storage", "storage")
        op.create_table(
            "core.features",
            sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(
                ["created_by"],
                ["core.user.id"],
                name=op.f("fk_core.features_created_by_user"),
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_core.features")),
        )
        with op.batch_alter_table("core.features", schema=None) as batch_op:
            batch_op.create_index(batch_op.f("ix_core.features_created_at"), ["created_at"], unique=False)
            batch_op.create_index(batch_op.f("ix_core.features_created_by"), ["created_by"], unique=False)

        op.create_table(
            "core.dobject_features",
            sa.Column("dobject_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("features_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.ForeignKeyConstraint(
                ["dobject_id"],
                ["core.dobject.id"],
                name=op.f("fk_core.dobject_features_dobject_id_dobject"),
            ),
            sa.ForeignKeyConstraint(
                ["features_id"],
                ["core.features.id"],
                name=op.f("fk_core.dobject_features_features_id_features"),
            ),
            sa.PrimaryKeyConstraint("dobject_id", "features_id", name=op.f("pk_core.dobject_features")),
        )
        with op.batch_alter_table("core.storage", schema=None) as batch_op:
            batch_op.drop_index("ix_core.storage_created_at")
            batch_op.drop_index("ix_core.storage_root")
            batch_op.drop_index("ix_core.storage_updated_at")

    op.alter_column(
        f"{prefix}dobject",
        column_name="checksum",
        new_column_name="hash",
        schema=schema,
    )

    with op.batch_alter_table("core.run", schema=None) as batch_op:
        batch_op.drop_index("ix_core.dtransform_created_at")
        batch_op.drop_index("ix_core.dtransform_created_by")
        batch_op.drop_index("ix_core.dtransform_jupynb_id")
        batch_op.drop_index("ix_core.dtransform_jupynb_v")
        batch_op.drop_index("ix_core.dtransform_name")
        batch_op.drop_index("ix_core.dtransform_pipeline_id")
        batch_op.drop_index("ix_core.dtransform_pipeline_v")
        batch_op.create_index(batch_op.f("ix_core.run_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_jupynb_id"), ["jupynb_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_jupynb_v"), ["jupynb_v"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_name"), ["name"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_pipeline_id"), ["pipeline_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.run_pipeline_v"), ["pipeline_v"], unique=False)
        batch_op.create_foreign_key(
            batch_op.f("fk_core.run_pipeline_id_pipeline"),
            "core.pipeline",
            ["pipeline_id", "pipeline_v"],
            ["id", "v"],
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_core.run_jupynb_id_jupynb"),
            "core.jupynb",
            ["jupynb_id", "jupynb_v"],
            ["id", "v"],
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_core.run_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
        )


def downgrade() -> None:
    pass
