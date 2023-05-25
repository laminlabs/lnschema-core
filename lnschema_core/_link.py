from sqlmodel import Field

from lnschema_core.dev.sqlmodel import get_orm

from . import __name__ as module_name

SQLModel = get_orm(module_name)


class RunInput(SQLModel, table=True):  # type: ignore
    """Inputs of runs.

    This is a many-to-many link table for `run` and `file` storing the
    inputs of data transformations.

    A data transformation can have an arbitrary number of data objects as inputs.

    - The same `file` can be used as input in many different `runs`.
    - One `run` can have several `files` as inputs.
    """

    run_id: str = Field(foreign_key="lnschema_core_run.id", primary_key=True)
    file_id: str = Field(foreign_key="lnschema_core_file.id", primary_key=True)


class FileFeatures(SQLModel, table=True):  # type: ignore
    """Links `File` and `Features`."""

    file_id: str = Field(foreign_key="lnschema_core_file.id", primary_key=True)
    features_id: str = Field(foreign_key="lnschema_core_features.id", primary_key=True)


class ProjectFolder(SQLModel, table=True):  # type: ignore
    """Link table of project and folder."""

    project_id: str = Field(foreign_key="lnschema_core_project.id", primary_key=True)
    folder_id: str = Field(foreign_key="lnschema_core_folder.id", primary_key=True)


class FolderFile(SQLModel, table=True):  # type: ignore
    """Link table of folder and file."""

    folder_id: str = Field(foreign_key="lnschema_core_folder.id", primary_key=True)
    file_id: str = Field(foreign_key="lnschema_core_file.id", primary_key=True)
