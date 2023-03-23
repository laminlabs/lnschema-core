"""v0.30rc2."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

from lnschema_core.dev.sqlmodel import get_prefix_schema_delim_from_alembic
from lnschema_core.dev.type import TransformType

revision = "ebafd37fd6e1"
down_revision = "9640062eefee"


move_pipeline_to_notebook = """\
insert into core.notebook (id, v, name, title, created_by, created_at, updated_at)
select id, v, name, title, created_by, created_at, updated_at from core.pipeline
"""

update_pipeline_references_and_make_them_notebook_references = """\
update core.run
set notebook_id = pipeline_id, notebook_v = pipeline_v, type = "pipeline"
where notebook_id is null
"""


def upgrade() -> None:
    prefix, schema, delim = get_prefix_schema_delim_from_alembic()

    op.execute(move_pipeline_to_notebook)
    op.add_column(table_name=f"{prefix}run", column=sa.Column("type", sa.Enum(TransformType), schema=schema))
    op.execute(update_pipeline_references_and_make_them_notebook_references)


def downgrade() -> None:
    pass
