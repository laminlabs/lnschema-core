"""v0.17.0.

Revision ID: 66bfd6cf2e2d
Revises: 4ee426b656bb
Create Date: 2022-11-11 22:05:39.865585

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "66bfd6cf2e2d"
down_revision = "4ee426b656bb"
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

    with op.batch_alter_table(f"{prefix}dtransform", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("pipeline_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("pipeline_v", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(batch_op.f("ix_core.dtransform_pipeline_id"), ["pipeline_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dtransform_pipeline_v"), ["pipeline_v"], unique=False)
        batch_op.add_column(
            sa.Column(
                "created_by",
                sqlmodel.sql.sqltypes.AutoString(),
                nullable=False,
                default="9ypQ1yrW",
            )
        )
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.create_index(batch_op.f("ix_core.dtransform_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dtransform_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f("ix_core.dtransform_name"), ["name"], unique=False)
        if sqlite:
            batch_op.create_foreign_key(
                batch_op.f("fk_core.dtransform_pipeline_id_pipeline"),
                f"{prefix}pipeline",
                ["pipeline_id", "pipeline_v"],
                ["id", "v"],
            )
            batch_op.create_foreign_key(
                batch_op.f("fk_core.dtransform_created_by_user"),
                f"{prefix}user",
                ["created_by"],
                ["id"],
            )

    if not sqlite:
        op.create_foreign_key(
            "fk_core.dtransform_pipeline_id_pipeline",
            f"{prefix}dtransform",
            f"{prefix}pipeline",
            ["pipeline_id", "pipeline_v"],
            ["id", "v"],
            source_schema=schema,
            referent_schema=schema,
        )
        op.create_foreign_key(
            "fk_core.dtransform_created_by_user",
            f"{prefix}dtransform",
            f"{prefix}user",
            ["created_by"],
            ["id"],
            source_schema=schema,
            referent_schema=schema,
        )

    if sqlite:
        op.execute(
            """
        update "core.dtransform"
        set created_by = "core.run".created_by,
        created_at = "core.run".created_at,
        name = "core.run".name,
        pipeline_id = "core.run".pipeline_id,
        pipeline_v = "core.run".pipeline_v
        from "core.run"
        where run_id = "core.run".id;
        """
        )
    else:
        op.execute(
            """
        update core.dtransform
        set created_by = core.run.created_by,
        created_at = core.run.created_at,
        name = core.run.name,
        pipeline_id = core.run.pipeline_id,
        pipeline_v = core.run.pipeline_v
        from core.run
        where run_id = core.run.id;
        """
        )

    try:
        op.drop_index("ix_core.dtransform_run_id")
        op.drop_constraint("bfx_run_id_fkey", "run", schema="bfx")
        op.drop_constraint("dtransform_pipeline_run_id_fkey", "dtransform", schema="core")
    except Exception:
        pass
    op.drop_column(f"{prefix}dtransform", "run_id", schema=schema)
    op.drop_table(f"{prefix}run", schema=schema)

    op.rename_table(
        old_table_name=f"{prefix}dtransform",
        new_table_name=f"{prefix}run",
        schema=schema,
    )
    op.rename_table(
        old_table_name=f"{prefix}dtransform_in",
        new_table_name=f"{prefix}run_in",
        schema=schema,
    )
    op.alter_column(
        f"{prefix}dobject",
        column_name="dtransform_id",
        new_column_name="run_id",
        schema=schema,
    )
    op.alter_column(
        f"{prefix}run_in",
        column_name="dtransform_id",
        new_column_name="run_id",
        schema=schema,
    )

    if bind.engine.name == "sqlite":
        op.execute("PRAGMA foreign_keys=ON")


def downgrade() -> None:
    pass
