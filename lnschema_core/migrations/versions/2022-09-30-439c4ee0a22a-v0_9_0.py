"""v0.9.0.

Revision ID: 439c4ee0a22a
Revises: 1190648443cb
Create Date: 2022-09-30 08:13:39.190602

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "439c4ee0a22a"
down_revision = "1190648443cb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("dobject", schema=None) as batch_op:
        batch_op.drop_column("v")

    with op.batch_alter_table("dtransform_in", schema=None) as batch_op:
        batch_op.drop_constraint("dtransform_in_dobject", type_="foreignkey")
        batch_op.create_foreign_key("fk_dobject_id", "dobject", ["dobject_id"], ["id"])
        batch_op.drop_column("dobject_v")

    with op.batch_alter_table("usage", schema=None) as batch_op:
        batch_op.drop_index("ix_usage_dobject_v")
        batch_op.drop_constraint("usage_dobject", type_="foreignkey")
        batch_op.create_foreign_key("fk_dobject_id", "dobject", ["dobject_id"], ["id"])
        batch_op.drop_column("dobject_v")


def downgrade() -> None:
    pass
