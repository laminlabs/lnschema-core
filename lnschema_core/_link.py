from sqlmodel import Field

from lnschema_core.dev.sqlmodel import schema_sqlmodel

from . import _name as schema_name

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class RunIn(SQLModel, table=True):  # type: ignore
    """Inputs of runs.

    This is a many-to-many link table for `run` and `dobject` storing the
    inputs of data transformations.

    A data transformation can have an arbitrary number of data objects as inputs.

    - The same `dobject` can be used as input in many different `runs`.
    - One `run` can have several `dobjects` as inputs.
    """

    __tablename__ = f"{prefix}run_in"

    run_id: str = Field(foreign_key="core.run.id", primary_key=True)
    dobject_id: str = Field(foreign_key="core.dobject.id", primary_key=True)


class DObjectFeatures(SQLModel, table=True):  # type: ignore
    """Links `DObject` and `Features`."""

    __tablename__ = f"{prefix}dobjects_features"

    dobject_id: str = Field(foreign_key="core.dobject.id", primary_key=True)
    features_id: str = Field(foreign_key="core.features.id", primary_key=True)


class ProjectDSet(SQLModel, table=True):  # type: ignore
    """Link table of project and dset."""

    __tablename__ = f"{prefix}project_dset"

    project_id: str = Field(foreign_key="core.project.id", primary_key=True)
    dset_id: str = Field(foreign_key="core.dset.id", primary_key=True)


class DSetDObject(SQLModel, table=True):  # type: ignore
    """Link table of dset and dobject."""

    __tablename__ = f"{prefix}dset_dobject"

    dset_id: str = Field(foreign_key="core.dset.id", primary_key=True)
    dobject_id: str = Field(foreign_key="core.dobject.id", primary_key=True)
