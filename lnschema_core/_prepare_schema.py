import sqlmodel as sqm
from sqlalchemy.orm import declared_attr


def schema_sqlmodel(schema_name: str):
    try:
        from lndb_setup._settings_load import load_or_create_instance_settings

        isettings = load_or_create_instance_settings()
        sqlite_true = isettings._dbconfig == "sqlite"
    except ImportError:
        sqlite_true = True

    if sqlite_true:

        class SQLModel(sqm.SQLModel):
            @declared_attr
            def __table_args__(cls) -> str:
                return dict(schema=schema_name)  # type: ignore

    else:

        class SQLModel(sqm.SQLModel):  # type: ignore
            @declared_attr
            def __tablename__(cls) -> str:  # type: ignore
                return f"{schema_name}.{cls.__name__.lower()}"

    return SQLModel
