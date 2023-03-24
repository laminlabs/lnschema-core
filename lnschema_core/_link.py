from sqlmodel import Field

from lnschema_core.dev.sqlmodel import schema_sqlmodel

from . import _name as schema_name

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class RunIn(SQLModel, table=True):  # type: ignore
    """Inputs of runs.

    This is a many-to-many link table for `run` and `file` storing the
    inputs of data transformations.

    A data transformation can have an arbitrary number of data objects as inputs.

    - The same `file` can be used as input in many different `runs`.
    - One `run` can have several `files` as inputs.
    """

    __tablename__ = f"{prefix}run_in"

    run_id: str = Field(foreign_key="core.run.id", primary_key=True)
    file_id: str = Field(foreign_key="core.file.id", primary_key=True)


class FileFeatures(SQLModel, table=True):  # type: ignore
    """Links `File` and `Features`."""

    __tablename__ = f"{prefix}file_features"

    file_id: str = Field(foreign_key="core.file.id", primary_key=True)
    features_id: str = Field(foreign_key="core.features.id", primary_key=True)


class ProjectFolder(SQLModel, table=True):  # type: ignore
    """Link table of project and folder."""

    __tablename__ = f"{prefix}project_folder"

    project_id: str = Field(foreign_key="core.project.id", primary_key=True)
    folder_id: str = Field(foreign_key="core.folder.id", primary_key=True)


class FolderFile(SQLModel, table=True):  # type: ignore
    """Link table of folder and file."""

    __tablename__ = f"{prefix}folder_file"

    folder_id: str = Field(foreign_key="core.folder.id", primary_key=True)
    file_id: str = Field(foreign_key="core.file.id", primary_key=True)
