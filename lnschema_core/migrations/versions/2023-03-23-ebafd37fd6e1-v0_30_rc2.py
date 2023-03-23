"""v0.30rc2."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic
from lnschema_core.dev.type import TransformType

revision = "ebafd37fd6e1"
down_revision = "9640062eefee"


move_pipeline_to_notebook = """\
insert into {core_notebook} (id, v, name, title, created_by, created_at, updated_at)
select id, v, name, title, created_by, created_at, updated_at from {core_pipeline}
"""

update_pipeline_references_and_make_them_notebook_references = """\
update {core_run}
set notebook_id = pipeline_id, notebook_v = pipeline_v, type = "pipeline"
where notebook_id is null
"""


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    core_notebook = "core.notebook"
    core_pipeline = "core.pipeline"
    core_run = "core.run"
    if sqlite:  # sqlite needs quotes
        core_notebook, core_pipeline, core_run = f"'{core_notebook}'", f"'{core_pipeline}'", f"'{core_run}'"

    op.execute(move_pipeline_to_notebook.format(core_notebook, core_pipeline))
    op.add_column(table_name=f"{prefix}run", column=sa.Column("type", sa.Enum(TransformType), schema=schema))
    op.execute(update_pipeline_references_and_make_them_notebook_references.format(core_run))


def downgrade() -> None:
    pass
