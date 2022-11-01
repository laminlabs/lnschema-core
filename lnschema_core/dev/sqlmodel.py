"""SQLModel children.

.. autosummary::
   :toctree: .

   SQLModelModule
   SQLModelPrefix
"""

from typing import Optional

import sqlmodel as sqm
from sqlalchemy.orm import declared_attr


class SQLModelModule(sqm.SQLModel):
    """SQLModel for schema module."""

    schema_name: Optional[str] = None

    @declared_attr
    def __table_args__(cls) -> str:
        """Update table args with schema module."""
        return dict(schema=cls.schema_name)  # type: ignore


class SQLModelPrefix(sqm.SQLModel):  # type: ignore
    """SQLModel prefixed by schema module name."""

    schema_name: Optional[str] = None

    @declared_attr
    def __tablename__(cls) -> str:  # type: ignore
        """Prefix table name with schema module."""
        return f"{cls.schema_name}.{cls.__name__.lower()}"


def schema_sqlmodel(schema_name: str):
    try:
        from lndb_setup._settings_load import load_or_create_instance_settings

        isettings = load_or_create_instance_settings()
        sqlite_true = isettings._dbconfig == "sqlite"
    except ImportError:
        sqlite_true = True

    if sqlite_true:
        SQLModelPrefix.schema_name = schema_name
        return SQLModelPrefix
    else:
        SQLModelModule.schema_name = schema_name
        return SQLModelModule
