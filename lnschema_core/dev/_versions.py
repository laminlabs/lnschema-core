from datetime import datetime as datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from .._timestamps import CreatedAt
from .._users import CreatedBy


class version_yvzi(SQLModel, table=True):  # type: ignore
    """Core schema module versions deployed in a given instance.

    Migrations of the schema module add rows to this table, storing the schema
    module version to which we migrated along with the user who performed the
    migration.
    """

    v: Optional[str] = Field(primary_key=True)
    """Python package version of `lnschema_core`."""
    migration: Optional[str] = None
    """Migration script reference of the latest migration leading up to the Python package version."""  # noqa
    user_id: str = CreatedBy
    """Link to :class:`~lnschema_core.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""


class migration_yvzi(SQLModel, table=True):  # type: ignore
    """Latest migration.

    This stores the reference to the latest migration script deployed.
    """

    version_num: Optional[str] = Field(primary_key=True)
    """Reference to the last-run migration script."""
