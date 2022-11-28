from sqlmodel import Field

from lnschema_core.dev.sqlmodel import schema_sqlmodel

from . import _name as schema_name

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class DObjectFeatures(SQLModel, table=True):  # type: ignore
    """Links `DObject` and `Features`."""

    __tablename__ = f"{prefix}dobjects_features"

    dobject_id: str = Field(foreign_key="core.dobject.id", primary_key=True)
    features_id: str = Field(foreign_key="core.features.id", primary_key=True)
