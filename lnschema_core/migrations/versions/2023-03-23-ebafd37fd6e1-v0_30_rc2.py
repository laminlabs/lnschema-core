"""v0.30rc2."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op
from sqlalchemy.engine.reflection import Inspector

from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic
from lnschema_core.dev.type import TransformType

revision = "ebafd37fd6e1"
down_revision = "9640062eefee"


copy_pipeline_to_notebook = """\
insert into {core_notebook} (id, v, name, created_by, created_at, updated_at)
select id, v, name, created_by, created_at, updated_at from {core_pipeline}
"""

make_pipeline_references_notebook_references_in_run = """\
update {core_run}
set notebook_id = pipeline_id, notebook_v = pipeline_v
where notebook_id is null
"""

SATransformType = sa.Enum(TransformType)


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    engine = op.get_bind().engine
    inspector = Inspector.from_engine(engine)

    core_notebook = "core.notebook"
    core_pipeline = "core.pipeline"
    core_run = "core.run"
    if sqlite:  # sqlite needs quotes
        core_notebook, core_pipeline, core_run = f"'{core_notebook}'", f"'{core_pipeline}'", f"'{core_run}'"

    # add the type column to the existing notebook table
    SATransformType.create(op.get_bind(), checkfirst=True)
    op.add_column(f"{prefix}notebook", sa.Column("type", SATransformType), schema=schema)

    op.execute(f"update {core_notebook} set type = 'notebook'")
    op.execute(copy_pipeline_to_notebook.format(core_notebook=core_notebook, core_pipeline=core_pipeline))
    op.execute(f"update {core_notebook} set type = 'pipeline' where type is null")
    op.execute(make_pipeline_references_notebook_references_in_run.format(core_run=core_run))

    op.drop_index(f"ix_core{delim}pipeline_created_at", table_name=f"{prefix}pipeline", schema=schema)
    op.drop_index(f"ix_core{delim}pipeline_created_by", table_name=f"{prefix}pipeline", schema=schema)
    op.drop_index(f"ix_core{delim}pipeline_name", table_name=f"{prefix}pipeline", schema=schema)
    op.drop_index(f"ix_core{delim}pipeline_reference", table_name=f"{prefix}pipeline", schema=schema)
    op.drop_index(f"ix_core{delim}pipeline_updated_at", table_name=f"{prefix}pipeline", schema=schema)

    op.drop_index(f"ix_core{delim}run_pipeline_id", table_name=f"{prefix}run", schema=schema)
    op.drop_index(f"ix_core{delim}run_pipeline_v", table_name=f"{prefix}run", schema=schema)
    op.drop_index(f"ix_core{delim}run_notebook_id", table_name=f"{prefix}run", schema=schema)
    op.drop_index(f"ix_core{delim}run_notebook_v", table_name=f"{prefix}run", schema=schema)

    with op.batch_alter_table(f"{prefix}run", schema=schema) as batch_op:
        for constraint in inspector.get_foreign_keys(f"{prefix}run", schema=schema):
            if constraint["name"] == "fk_run_notebook_id_notebook":
                batch_op.drop_constraint("fk_run_notebook_id_notebook", type_="foreignkey")
            if constraint["name"] == "fk_run_pipeline_id_pipeline":
                batch_op.drop_constraint("fk_run_pipeline_id_pipeline", type_="foreignkey")

        batch_op.drop_column(column_name="pipeline_id")
        batch_op.drop_column(column_name="pipeline_v")

    op.drop_table(table_name=f"{prefix}pipeline", schema=schema)
    op.rename_table(old_table_name=f"{prefix}notebook", new_table_name=f"{prefix}transform", schema=schema)

    with op.batch_alter_table(f"{prefix}run", schema=schema) as batch_op:
        batch_op.alter_column(column_name="notebook_id", new_column_name="transform_id")
        batch_op.alter_column(column_name="notebook_v", new_column_name="transform_v")

    # need another batch_op as the rename is not yet complete up there
    with op.batch_alter_table(f"{prefix}run", schema=schema) as batch_op:
        batch_op.create_index(op.f("ix_core_run_transform_id"), ["transform_id"], unique=False)
        batch_op.create_index(op.f("ix_core_run_transform_v"), ["transform_v"], unique=False)

        batch_op.create_foreign_key(op.f("fk_run_transform_id_transform"), f"{prefix}transform", ["transform_id", "transform_v"], ["id", "v"], referent_schema=schema)

    with op.batch_alter_table(f"{prefix}transform", schema=schema) as batch_op:
        batch_op.drop_index(f"ix_core{delim}notebook_created_at")
        batch_op.drop_index(f"ix_core{delim}notebook_created_by")
        batch_op.drop_index(f"ix_core{delim}notebook_name")
        batch_op.drop_index(f"ix_core{delim}notebook_title")
        batch_op.drop_index(f"ix_core{delim}notebook_updated_at")
        batch_op.create_index(op.f(f"ix_core{delim}transform_created_at"), ["created_at"], unique=False)
        batch_op.create_index(op.f(f"ix_core{delim}transform_created_by"), ["created_by"], unique=False)
        batch_op.create_index(op.f(f"ix_core{delim}transform_name"), ["name"], unique=False)
        batch_op.create_index(op.f(f"ix_core{delim}transform_title"), ["title"], unique=False)
        batch_op.create_index(op.f(f"ix_core{delim}transform_type"), ["type"], unique=False)
        batch_op.create_index(op.f(f"ix_core{delim}transform_updated_at"), ["updated_at"], unique=False)
        batch_op.alter_column("type", nullable=False)


def downgrade() -> None:
    pass
