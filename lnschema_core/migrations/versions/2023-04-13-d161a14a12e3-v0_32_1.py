"""v0.32.1."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op

from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic
from lnschema_core.dev.type import TransformType

revision = "d161a14a12e3"
down_revision = "6de59093e378"

# this type got added in v0.30rc2, now we're updating it
SATransformType = sa.Enum(TransformType)


# see https://medium.com/makimo-tech-blog/upgrading-postgresqls-enum-type-with-sqlalchemy-using-alembic-migration-881af1e30abe
def upgrade() -> None:
    sqlite, _, _, _ = get_sqlite_prefix_schema_delim_from_alembic()
    if not sqlite:
        with op.get_context().autocommit_block():
            op.execute("ALTER TYPE transformtype ADD VALUE 'app'")


def downgrade() -> None:
    pass
