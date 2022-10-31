from typing import Optional

from sqlmodel import Field, SQLModel


class migration_yvzi(SQLModel, table=True):  # type: ignore
    """Latest migration.

    This stores the reference to the latest migration script deployed.
    """

    version_num: Optional[str] = Field(primary_key=True)
    """Reference to the last-run migration script."""
