"""v0.30rc2."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

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


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    core_notebook = "core.notebook"
    core_pipeline = "core.pipeline"
    core_run = "core.run"
    if sqlite:  # sqlite needs quotes
        core_notebook, core_pipeline, core_run = f"'{core_notebook}'", f"'{core_pipeline}'", f"'{core_run}'"

    op.add_column(table_name=f"{prefix}notebook", column=sa.Column("type", sa.Enum(TransformType)), schema=schema)
    op.execute(f"update {core_notebook} set type = 'notebook'")
    op.execute(copy_pipeline_to_notebook.format(core_notebook=core_notebook, core_pipeline=core_pipeline))
    op.execute(f"update {core_notebook} set type = 'pipeline' where type is null")
    op.execute(make_pipeline_references_notebook_references_in_run.format(core_run=core_run))
    op.drop_index(index_name=f"ix_core{delim}run_pipeline_id")
    op.drop_column(table_name=f"{prefix}run", column_name="pipeline_id", schema=schema)
    op.drop_index(index_name=f"ix_core{delim}run_pipeline_v")
    op.drop_column(table_name=f"{prefix}run", column_name="pipeline_v", schema=schema)
    op.drop_table(table_name=f"{prefix}pipeline", schema=schema)
    op.rename_table(old_table_name=f"{prefix}notebook", new_table_name=f"{prefix}transform", schema=schema)


def downgrade() -> None:
    pass
