from datetime import datetime as datetime
from pathlib import Path
from typing import Any, List, Optional, Union, overload  # noqa

import anndata as ad
import pandas as pd
import sqlalchemy as sa
import sqlmodel
from cloudpathlib import CloudPath
from lamin_logger import logger
from nbproject._is_run_from_ipython import is_run_from_ipython
from pydantic.fields import PrivateAttr
from sqlmodel import Field, ForeignKeyConstraint, Relationship

from . import _name as schema_name
from ._link import DFolderDObject, DObjectFeatures, ProjectDFolder, RunIn  # noqa
from ._timestamps import CreatedAt, UpdatedAt
from ._users import CreatedBy
from .dev import id as idg
from .dev._storage import filepath_from_dfolder, filepath_from_dobject
from .dev.sqlmodel import schema_sqlmodel
from .dev.type import TransformType

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
        x: List["DObject"] = [],
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
    """Link to :class:`~lamindb.Run` that generated the `dobject`."""
    source_id: str = Field(foreign_key="core.run.id", index=True)
    """The source run id."""
    storage_id: str = Field(foreign_key="core.storage.id", index=True)
    """The id of :class:`~lamindb.schema.Storage` location that stores the `dobject`."""
    features: List["Features"] = Relationship(
        back_populates="dobjects",
        sa_relationship_kwargs=dict(secondary=DObjectFeatures.__table__),
    )
    """Link to feature sets :class:`~lamindb.Features`"""
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
        features: List["Features"] = [],
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
        features: List["Features"] = [],
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
        targets: List["Run"] = [],
        # backward compat
        features_ref: Optional[Any] = None,
    ):
        if data is not None:
            from lamindb._record import get_dobject_kwargs_from_data

            kwargs, privates = get_dobject_kwargs_from_data(
                data=data,
                name=name,
                source=source,
                format=format,
                features_ref=features_ref,
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
            # when features are passed with data
            if not isinstance(features, List):
                features = [features]
            self.features += features


DObject._objectkey = sa.Column("_objectkey", sqlmodel.sql.sqltypes.AutoString(), index=True)
DObject.__table__.append_constraint(sa.UniqueConstraint("storage_id", "_objectkey", "suffix", name="uq_storage__objectkey_suffix"))


class Transform(SQLModel, table=True):  # type: ignore
    """Data transformations.

    Jupyter notebooks.

    Jupyter notebooks (`notebooks`) represent one type of data transformation
    (`run`) and have a unique correspondence in `run`.

    IDs for Jupyter notebooks are generated through nbproject.

    Pipelines.

    A pipeline is typically versioned software that can perform a data
    transformation/processing workflow. This can be anything from typical
    workflow tools (Nextflow, Snakemake, Prefect, Apache Airflow, etc.) to
    simple (versioned) scripts.
    """

    id: str = Field(default_factory=idg.pipeline, primary_key=True)
    """Id."""  # noqa
    v: str = Field(default="1", primary_key=True)
    """Version identifier, defaults to `"1"`.

    Use this to label different versions of the same transform.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    name: str = Field(index=True)
    """File name of the transform.
    """
    type: TransformType = Field(index=True, default=TransformType.pipeline)
    """File name of the transform.
    """
    title: Optional[str] = Field(index=True)
    """Title of the transform as generated by `nbproject.meta.title
    <https://lamin.ai/docs/nbproject/nbproject.dev.metalive#nbproject.dev.MetaLive.title>`__.
    """
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lamindb.schema.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""
    updated_at: Optional[datetime] = UpdatedAt
    """Time of last update."""


class Run(SQLModel, table=True):  # type: ignore
    """Code runs that transform data.

    A `run` is any transformation of a `dobject`.

    Args:
        global_context: bool = None - Define a global run. False when run in a non-notebooks, True when run from notebook.
        pipeline_name: Optional[str] = None
        load_latest: bool = None - Load latest run for given notebook or pipeline. False when run in a non-notebooks, True when run from notebook.
        id: Optional[str] = None
        name: Optional[str] = None
        transform: Optional[Transform] = None
        inputs: List[DObject] = None
        outputs: List[DObject] = None

    For instance:

    - Jupyter notebooks (`notebook`)
    - Pipeline runs of software (workflows) and scripts (`run`).

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
            ["transform_id", "transform_v"],
            ["core.transform.id", "core.transform.v"],
        ),
        {"schema": schema_arg},
    )
    id: Optional[str] = Field(default_factory=idg.run, primary_key=True)
    """Base62 char ID & primary key, generated through :func:`~lamindb.schema.dev.id.run`."""  # noqa
    name: Optional[str] = Field(default=None, index=True)
    external_id: Optional[str] = Field(default=None, index=True)
    transform_id: Optional[str] = Field(default=None, index=True)
    transform_v: Optional[str] = Field(default=None, index=True)
    transform: Transform = Relationship()
    """Link to :class:`~lamindb.schema.Notebook`."""
    outputs: List["DObject"] = Relationship(back_populates="source")
    """Output data :class:`~lamindb.DObject`."""
    inputs: List["DObject"] = Relationship(back_populates="targets", sa_relationship_kwargs=dict(secondary=RunIn.__table__))
    """Input data :class:`~lamindb.DObject`."""
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lamindb.schema.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""

    _ln_identity_key: Optional[str] = PrivateAttr(default=None)
    # simulate query result

    def __init__(  # type: ignore
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        global_context: Optional[bool] = None,
        load_latest: Optional[bool] = None,
        pipeline_name: Optional[str] = None,
        external_id: Optional[str] = None,
        transform: Optional[Transform] = None,
        inputs: List[DObject] = None,
        outputs: List[DObject] = None,
    ):
        kwargs = {k: v for k, v in locals().items() if v and k != "self"}

        import lamindb as ln
        import lamindb.schema as lns
        from lamindb import context

        if global_context is None:
            # am I being run from a notebook? if yes, global_context = True, else False
            global_context = is_run_from_ipython and pipeline_name is None

        if load_latest is None:
            # am I being run from a notebook? if yes, load_latest = True, else False
            load_latest = is_run_from_ipython and pipeline_name is None

        if global_context:
            context._track_notebook_pipeline(pipeline_name=pipeline_name, load_latest=load_latest)
            transform = context.transform

        if transform is None:
            if global_context:
                raise RuntimeError("Please set notebook or pipeline global context.")
            else:
                raise RuntimeError("Please pass notebook or pipeline.")
        elif not isinstance(transform, Transform):
            raise TypeError("transform needs to be of type Transform")

        run = None
        if load_latest:
            run = ln.select(lns.Run, transform_id=transform.id, transform_v=transform.v).order_by(lns.Run.created_at.desc()).first()
            if run is not None:
                logger.info("Loaded run:")  # colon is on purpose!
        elif id is not None:
            run = ln.select(lns.Run, id=id).one_or_none()
            if run is None:
                raise NotImplementedError("You can currently only pass existing IDs.")

        if run is None:
            kwargs.update(dict(transform_id=transform.id, transform_v=transform.v))
            super().__init__(**kwargs)
            self._ln_identity_key = None
        else:
            super().__init__(**run.dict())
            self._ln_identity_key = run.id  # simulate query result

        if global_context:
            if run is None:
                added_self = ln.add(self)
                self._ln_identity_key = added_self.id
                logger.info("Added run:")  # colon is on purpose!
            context.run = self


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

    @overload
    def __init__(
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        reference: Any = None,
    ):
        """Initialize from data."""
        ...

    @overload
    def __init__(
        self,
        id: Optional[str] = None,
        type: Optional[str] = None,
        dobjects: List["DObject"] = [],
    ):
        """Initialize from fields."""
        ...

    def __init__(  # type: ignore
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        reference: Any = None,
        *,
        id: str = None,
        type: Any = None,
        # continue with fields
        dobjects: List["DObject"] = [],
    ):
        kwargs = {k: v for k, v in locals().items() if v and k != "self"}
        super().__init__(**kwargs)

    def __new__(
        cls,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        reference: Any = None,
        *,
        id: str = None,
        type: Any = None,
        # continue with fields
        dobjects: List["DObject"] = [],
    ):
        if data is not None:
            from lamindb._record import get_features_from_data

            features = get_features_from_data(
                data=data,
                reference=reference,
            )
        else:
            features = super().__new__(cls)
        return features
