from datetime import datetime as datetime
from pathlib import Path
from typing import Any, List, Optional, Union, overload  # noqa

import anndata as ad
import pandas as pd
import sqlalchemy as sa
import sqlmodel
from cloudpathlib import CloudPath
from lamin_logger import logger
from pydantic.fields import PrivateAttr
from sqlmodel import Field, ForeignKeyConstraint, Relationship

from . import _name as schema_name
from ._link import DFolderDObject, DObjectFeatures, ProjectDFolder, RunIn  # noqa
from ._timestamps import CreatedAt, UpdatedAt
from ._users import CreatedBy
from .dev import id as idg
from .dev._storage import filepath_from_dfolder, filepath_from_dobject
from .dev.sqlmodel import schema_sqlmodel
from .dev.type import usage as usage_type

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class User(SQLModel, table=True):  # type: ignore
    """User accounts.

    All data in this table is synched from the cloud user account to ensure a
    globally unique user identity.
    """

    id: str = Field(primary_key=True)
    """User ID. Typically 8-character base64."""  # noqa
    email: str = Field(index=True, unique=True)
    """Primary user email used for logging in."""
    handle: str = Field(nullable=False, index=True, unique=True)
    """User handle."""
    name: Optional[str] = Field(index=True)
    """Long display name."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Storage(SQLModel, table=True):  # type: ignore
    """Storage locations.

    A dobject or run-associated file can be stored in any desired S3,
    GCP, Azure or local storage location. This table tracks these locations
    along with metadata.
    """

    id: str = Field(default_factory=idg.storage, primary_key=True)
    """Base62 char ID, generated by :func:`~lamindb.schema.dev.id.storage`."""
    root: str = Field(index=True)
    """Semantic identifier to the root of the storage location, like an s3 path, a local path, etc."""  # noqa
    type: Optional[str] = None
    """Local vs. s3 vs. gcp etc."""
    region: Optional[str] = None
    """Cloud storage region if applicable."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class DFolder(SQLModel, table=True):  # type: ignore
    """Data folders, collections of data objects.

    In LaminDB, a data folder is a collection of data objects (`DObject`).
    """

    id: str = Field(default_factory=idg.dfolder, primary_key=True)
    name: str = Field(index=True)
    dobjects: List["DObject"] = Relationship(  # type: ignore  # noqa
        back_populates="dfolders",
        sa_relationship_kwargs=dict(secondary=DFolderDObject.__table__),
    )
    """Collection of :class:`~lamindb.DObject`."""
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lamindb.schema.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""
    updated_at: Optional[datetime] = UpdatedAt
    """Time of last update."""

    # private attributes are needed here to prevent sqlalchemy error
    _local_filepath: Optional[Path] = PrivateAttr()
    _cloud_filepath: Optional[CloudPath] = PrivateAttr()

    def path(self) -> Union[Path, CloudPath]:
        """Path on storage."""
        return filepath_from_dfolder(self)

    def tree(
        self,
        level: int = -1,
        limit_to_directories: bool = False,
        length_limit: int = 1000,
    ) -> None:
        """Print a visual tree structure."""
        from lamindb._folder import tree

        return tree(
            dir_path=self.path(),
            level=level,
            limit_to_directories=limit_to_directories,
            length_limit=length_limit,
        )

    def get(self, relpath: Union[str, Path, List[Union[str, Path]]], **fields):
        """Get dobjects via relative path to dfolder."""
        from lamindb._folder import get_dobject

        return get_dobject(dfolder=self, relpath=relpath, **fields)

    @overload
    def __init__(
        self,
        folder: Union[Path, str] = None,
        *,
        name: Optional[str] = None,
    ):
        """Initialize from folder."""
        ...

    @overload
    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        dobjects: List["DObject"] = [],
    ):
        """Initialize from fields."""
        ...

    def __init__(  # type: ignore
        self,
        folder: Union[Path, str] = None,
        *,
        # continue with fields
        id: Optional[str] = None,
        name: Optional[str] = None,
        dobjects: List["DObject"] = [],
    ):
        if folder is not None:
            from lamindb._folder import get_dfolder_kwargs_from_data

            kwargs, privates = get_dfolder_kwargs_from_data(
                folder=folder,
                name=name,
            )
            if id is not None:
                kwargs["id"] = id
        else:
            kwargs = {k: v for k, v in locals().items() if v and k != "self"}

        super().__init__(**kwargs)
        if folder is not None:
            self._local_filepath = privates["_local_filepath"]
            self._cloud_filepath = privates["_cloud_filepath"]


DFolder._objectkey = sa.Column("_objectkey", sqlmodel.sql.sqltypes.AutoString(), index=True)


class Project(SQLModel, table=True):  # type: ignore
    """Projects."""

    id: str = Field(default_factory=idg.project, primary_key=True)
    name: str = Field(index=True)
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lamindb.schema.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""
    updated_at: Optional[datetime] = UpdatedAt
    """Time of last update."""


class DObject(SQLModel, table=True):  # type: ignore
    """See lamindb.schema for docstring."""

    id: str = Field(default_factory=idg.dobject, primary_key=True)
    """Base62 char ID, generated by :func:`~lamindb.schema.dev.id.dobject`."""
    name: Optional[str] = Field(index=True)
    """Semantic name or title. Defaults to `None`."""
    suffix: Optional[str] = Field(default=None, index=True)
    """Suffix to construct the storage key. Defaults to `None`.

    This is a file extension if the `dobject` is stored in a file format.
    It's `None` if the storage format doesn't have a canonical extension.
    """

    size: Optional[int] = Field(default=None, sa_column=sa.Column(sa.BigInteger(), index=True))
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    hash: Optional[str] = Field(default=None, index=True)
    """Hash (md5)."""

    # We need the fully module-qualified path below, as there might be more
    # schema modules with an ORM called "Run"
    source: "lnschema_core._core.Run" = Relationship(back_populates="outputs")  # type: ignore  # noqa
    """Link to :class:`~lamindb.schema.Run` that generated the `dobject`."""
    source_id: str = Field(foreign_key="core.run.id", index=True)
    """The source run id."""
    storage_id: str = Field(foreign_key="core.storage.id", index=True)
    """The id of :class:`~lamindb.schema.Storage` location that stores the `dobject`."""
    features: List["Features"] = Relationship(
        back_populates="dobjects",
        sa_relationship_kwargs=dict(secondary=DObjectFeatures.__table__),
    )
    """Link to feature sets."""
    dfolders: List[DFolder] = Relationship(
        back_populates="dobjects",
        sa_relationship_kwargs=dict(secondary=DFolderDObject.__table__),
    )
    """Collection of :class:`~lamindb.DFolder` that contain this dobject."""
    targets: List["lnschema_core._core.Run"] = Relationship(  # type: ignore  # noqa
        back_populates="inputs",
        sa_relationship_kwargs=dict(secondary=RunIn.__table__),
    )
    "Runs that use this dobject as input."
    created_at: datetime = CreatedAt
    """Time of creation."""
    updated_at: Optional[datetime] = UpdatedAt
    """Time of last update."""

    # private attributes are needed here to prevent sqlalchemy error
    _local_filepath: Optional[Path] = PrivateAttr()
    _cloud_filepath: Optional[CloudPath] = PrivateAttr()
    _memory_rep: Any = PrivateAttr()

    def path(self) -> Union[Path, CloudPath]:
        """Path on storage."""
        return filepath_from_dobject(self)

    def load(self, stream: bool = False, is_run_input: bool = False):
        """Load data object.

        Returns in-memory representation if configured (say, an `AnnData` object
        for an `h5ad` file).

        Otherwise, returns a path to a locally cached on-disk object (say, a
        `.jpg` file).
        """
        from lamindb._load import load as lnload

        return lnload(dobject=self, stream=stream, is_run_input=is_run_input)

    @overload
    def __init__(
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        *,
        name: Optional[str] = None,
        features_ref: Any = None,
        source: Optional["Run"] = None,
        id: Optional[str] = None,
        format: Optional[str] = None,
    ):
        """Initialize from data."""
        ...

    @overload
    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        source: Optional["Run"] = None,
        suffix: Optional[str] = None,
        size: Optional[int] = None,
        hash: Optional[str] = None,
        source_id: Optional[str] = None,
        storage_id: Optional[str] = None,
        features: List["Features"] = [],
        targets: List["Run"] = [],
    ):
        """Initialize from fields."""
        ...

    def __init__(  # type: ignore
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        *,
        features_ref: Any = None,
        source: Optional["Run"] = None,
        format: Optional[str] = None,
        # continue with fields
        id: Optional[str] = None,
        name: Optional[str] = None,
        suffix: Optional[str] = None,
        size: Optional[int] = None,
        hash: Optional[str] = None,
        source_id: Optional[str] = None,
        storage_id: Optional[str] = None,
        features: List["Features"] = [],
        targets: List["Run"] = [],
    ):
        if data is not None:
            from lamindb._record import get_dobject_kwargs_from_data

            kwargs, privates = get_dobject_kwargs_from_data(
                data=data,
                name=name,
                features_ref=features_ref,
                source=source,
                format=format,
            )
            if id is not None:
                kwargs["id"] = id
        else:
            kwargs = {k: v for k, v in locals().items() if v and k != "self"}

        super().__init__(**kwargs)
        if data is not None:
            self._local_filepath = privates["_local_filepath"]
            self._cloud_filepath = privates["_cloud_filepath"]
            self._memory_rep = privates["_memory_rep"]


DObject._objectkey = sa.Column("_objectkey", sqlmodel.sql.sqltypes.AutoString(), index=True)
DObject.__table__.append_constraint(sa.UniqueConstraint("storage_id", "_objectkey", "suffix", name="uq_storage__objectkey_suffix"))


class Run(SQLModel, table=True):  # type: ignore
    """Code runs that transform data.

    A `run` is any transformation of a `dobject`.

    Args:
        id: Optional[str] = None,
        name: Optional[str] = None,
        global_context: bool = False,
        load_latest: bool = False,
        pipeline: Optional["Pipeline"] = None,
        notebook: Optional["Notebook"] = None,
        outputs: List[DObject] = [],
        inputs: List[DObject] = [],

    For instance:

    - Jupyter notebooks (`notebook`)
    - Pipeline runs of software (workflows) and scripts (`run`).
    - Physical instruments making measurements (needs to be configured).
    - Human decisions based on data visualizations (needs to be configured).

    It typically has inputs and outputs:

    - References to outputs are stored in the `dobject` table in the
      `run_id` column, which stores a foreign key into the `run`
      table. This is possible as every given `dobject` has a unique data source:
      the `run` that produced the `dobject`. Note that a given
      `run` may output several `dobjects`.
    - References to input `dobjects` are stored in the `run_in` table, a
      many-to-many link table between the `dobject` and `run` tables. Any
      `dobject` might serve as an input for many `run`. Similarly, any
      `run` might have many `dobjects` as inputs.
    """

    __table_args__ = (
        ForeignKeyConstraint(
            ["pipeline_id", "pipeline_v"],
            ["core.pipeline.id", "core.pipeline.v"],
        ),
        ForeignKeyConstraint(
            ["notebook_id", "notebook_v"],
            ["core.notebook.id", "core.notebook.v"],
        ),
        {"schema": schema_arg},
    )
    id: str = Field(default_factory=idg.run, primary_key=True)
    """Base62 char ID & primary key, generated through :func:`~lamindb.schema.dev.id.run`."""  # noqa
    name: Optional[str] = Field(default=None, index=True)
    external_id: Optional[str] = Field(default=None, index=True)
    """ID to reference external tools, e.g., a redun execution ID."""
    pipeline_id: Optional[str] = Field(default=None, index=True)
    pipeline_v: Optional[str] = Field(default=None, index=True)
    pipeline: Optional["lnschema_core._core.Pipeline"] = Relationship()  # type: ignore # noqa
    """Link to :class:`~lamindb.schema.Pipeline`."""
    notebook_id: Optional[str] = Field(default=None, index=True)
    notebook_v: Optional[str] = Field(default=None, index=True)
    notebook: Optional["Notebook"] = Relationship()
    """Link to :class:`~lamindb.schema.Notebook`."""
    outputs: List["DObject"] = Relationship(back_populates="source")
    """Output data :class:`~lamindb.DObject`."""
    inputs: List["DObject"] = Relationship(back_populates="targets", sa_relationship_kwargs=dict(secondary=RunIn.__table__))
    """Input data :class:`~lamindb.DObject`."""
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lamindb.schema.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""

    def __init__(  # type: ignore
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        global_context: bool = False,
        load_latest: bool = False,
        pipeline: Optional["Pipeline"] = None,
        notebook: Optional["Notebook"] = None,
        inputs: List[DObject] = None,
        outputs: List[DObject] = None,
    ):
        import lamindb as ln
        import lamindb.schema as lns
        from lamindb import context

        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []

        if not isinstance(pipeline, Pipeline):
            raise TypeError(f"{pipeline} is no Pipeline")
        if not isinstance(notebook, Notebook):
            raise TypeError(f"{notebook} is no Notebook")

        if global_context:
            notebook = context.notebook
            pipeline = context.pipeline

        run = None
        if load_latest:
            if notebook is not None:
                select_stmt = ln.select(lns.Run, notebook_id=notebook.id, notebook_v=notebook.v)
            elif pipeline is not None:
                select_stmt = ln.select(lns.Run, pipeline_id=pipeline.id, pipeline_v=pipeline.v)
            else:
                if global_context:
                    raise RuntimeError("Please set notebook or pipeline global context.")
                else:
                    raise RuntimeError("Please pass notebook or pipeline.")
            run = select_stmt.order_by(lns.Run.created_at.desc()).first()
        if id is not None:
            run = ln.select(lns.Run, id=id).one_or_none()
            if run is None:
                raise NotImplementedError("You can currently only pass existing IDs.")
        if run is not None:
            logger.info(f"Loaded run: {run.id}")  # type: ignore
        else:
            logger.info("Did not find a latest run.")

        # create a new run if doesn't exist yet or is requested by the user
        if run is None:
            # for some reason, super isn't smart enough to translate the relationship to id and v
            if notebook is not None:
                super().__init__(name=name, notebook=notebook, notebook_id=notebook.id, notebook_v=notebook.v, inputs=inputs, outputs=outputs)
            elif pipeline is not None:
                super().__init__(name=name, pipeline=pipeline, pipeline_id=pipeline.id, pipeline_v=pipeline.v, inputs=inputs, outputs=outputs)
            else:
                if global_context:
                    raise RuntimeError("Please set notebook or pipeline global context.")
                else:
                    raise RuntimeError("Please pass notebook or pipeline.")
        else:
            self = run

        if global_context:
            context.run = self


class Notebook(SQLModel, table=True):  # type: ignore
    """Jupyter notebooks.

    Jupyter notebooks (`notebooks`) represent one type of data transformation
    (`run`) and have a unique correspondence in `run`.

    IDs for Jupyter notebooks are generated through nbproject.
    """

    id: str = Field(default=None, primary_key=True)
    """Base62 char ID & primary key, generated by :func:`~lamindb.schema.dev.id.notebook`."""  # noqa
    v: str = Field(default="1", primary_key=True)
    """Version identifier, defaults to `"1"`.

    Use this to label different versions of the same notebook.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    name: str = Field(index=True)
    """File name of the notebook.
    """
    title: Optional[str] = Field(index=True)
    """Title of the notebook as generated by `nbproject.meta.title
    <https://lamin.ai/docs/nbproject/nbproject.dev.metalive#nbproject.dev.MetaLive.title>`__.
    """
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lamindb.schema.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""
    updated_at: Optional[datetime] = UpdatedAt
    """Time of last update."""


class Pipeline(SQLModel, table=True):  # type: ignore
    """Pipelines.

    A pipeline is typically versioned software that can perform a data
    transformation/processing workflow. This can be anything from typical
    workflow tools (Nextflow, Snakemake, Prefect, Apache Airflow, etc.) to
    simple (versioned) scripts.
    """

    id: str = Field(default_factory=idg.pipeline, primary_key=True)
    v: str = Field(default="1", primary_key=True)
    name: Optional[str] = Field(default=None, index=True)
    reference: Optional[str] = Field(default=None, index=True)
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lamindb.schema.User`."""
    created_at: datetime = CreatedAt
    """Auto-populated time stamp."""
    updated_at: Optional[datetime] = UpdatedAt


class Features(SQLModel, table=True):  # type: ignore
    """Sets of features."""

    id: str = Field(primary_key=True)  # use a hash
    type: str  # was called entity_type
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    dobjects: List["DObject"] = Relationship(
        back_populates="features",
        sa_relationship_kwargs=dict(secondary=DObjectFeatures.__table__),
    )


class Usage(SQLModel, table=True):  # type: ignore
    """Data usage log.

    Any API call in the `lamindb.db` API is logged here.
    """

    id: str = Field(default_factory=idg.usage, primary_key=True)
    """Base62 char ID & primary key, generated by :func:`~lamindb.schema.dev.id.usage`."""  # noqa
    type: usage_type = Field(nullable=False, index=True)
    """Usage type."""
    user_id: str = CreatedBy
    """Link to :class:`~lamindb.schema.User`."""
    time: datetime = CreatedAt
    """Time of event."""
    dobject_id: str = Field(foreign_key="core.dobject.id", index=True)
    """Link to the affected :class:`~lamindb.DObject`."""
