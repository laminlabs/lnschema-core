"""SQLModel children.

.. autosummary::
   :toctree: .

   SQLModelModule
   SQLModelPrefix
"""

import sqlmodel as sqm
from sqlalchemy.orm import declared_attr

# it's tricky to deal with class variables in SQLModel children
# hence, we're using a global variable, here
SCHEMA_NAME = None


class SQLModelModule(sqm.SQLModel):
    """SQLModel for schema module."""

    # this here is problematic for those tables that overwrite
    # __table_args__; we currently need to treat them manually
    @declared_attr
    def __table_args__(cls) -> str:
        """Update table args with schema module."""
        return dict(schema=f"{SCHEMA_NAME}")  # type: ignore


class SQLModelPrefix(sqm.SQLModel):  # type: ignore
    """SQLModel prefixed by schema module name."""

    @declared_attr
    def __tablename__(cls) -> str:  # type: ignore
        """Prefix table name with schema module."""
        return f"{SCHEMA_NAME}.{cls.__name__.lower()}"


def is_sqlite():
    try:
        from lndb_setup._settings_load import load_or_create_instance_settings

        isettings = load_or_create_instance_settings()
        sqlite_true = isettings._dbconfig == "sqlite"
    except ImportError:
        sqlite_true = True

    return sqlite_true


def schema_sqlmodel(schema_name: str):
    global SCHEMA_NAME
    SCHEMA_NAME = schema_name

    if is_sqlite():
        prefix = f"{schema_name}."
        schema_arg = None
        return SQLModelPrefix, prefix, schema_arg
    else:
        prefix = None
        schema_arg = schema_name
        return SQLModelModule, prefix, schema_arg
