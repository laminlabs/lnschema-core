from datetime import datetime as datetime
from pathlib import Path, PurePosixPath
from typing import Any, List, Optional, TypeVar, Union, overload  # noqa

import anndata as ad
import pandas as pd
import sqlalchemy as sa
from lamin_logger import logger
from lndb.dev.upath import UPath
from nbproject._is_run_from_ipython import is_run_from_ipython
from pydantic.fields import PrivateAttr
from sqlmodel import Field, ForeignKeyConstraint, Relationship

from . import __name__ as module_name
from . import _name as schema_name
from ._link import FileFeatures, FolderFile, ProjectFolder, RunInput  # noqa
from ._timestamps import CreatedAt, UpdatedAt
from ._users import CreatedBy
from .dev import id as idg
from .dev.sqlmodel import get_orm, schema_sqlmodel
from .types import DataLike, ListLike, PathLike, SQLModelField, TransformType

# this is for backward compat
schema_sqlmodel(schema_name)

# this is the current way
SQLModel = get_orm(module_name)


class User(SQLModel, table=True):  # type: ignore
    """User accounts.

    All data in this table is synched from the cloud user account to ensure a
    globally unique user identity.
    """

    id: str = Field(primary_key=True)
    email: str = Field(index=True, unique=True)
    handle: str = Field(nullable=False, index=True, unique=True)
    name: Optional[str] = Field(index=True)
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Storage(SQLModel, table=True):  # type: ignore
    """Storage locations, often object storage buckets.

    A file or run-associated file can be stored in any desired S3,
    GCP bucket or local storage location.

    This table tracks these locations along with metadata.
    """

    id: str = Field(default_factory=idg.storage, primary_key=True)
    root: str = Field(index=True)
    """Semantic identifier to the root of the storage location, like an s3 path, a local path, etc."""  # noqa
    type: Optional[str] = None
    """Local vs. s3 vs. gcp etc."""
    region: Optional[str] = None
    """Cloud storage region, if applicable."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
    created_by: User = Relationship()
    created_by_id: Optional[str] = CreatedBy  # make non-optional over time


class Project(SQLModel, table=True):  # type: ignore
    """Projects."""

    id: str = Field(default_factory=idg.project, primary_key=True)
    name: str = Field(index=True)
    created_by: User = Relationship()
    created_by_id: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Transform(SQLModel, table=True):  # type: ignore
    """Data transformations.

    Jupyter notebooks, pipelines, and apps.

    A pipeline is typically versioned software that can perform a data
    transformation/processing workflow. This can be anything from typical
    workflow tools (Nextflow, Snakemake, Prefect, Apache Airflow, etc.) to
    simple (versioned) scripts.

    Data can also be ingested & transformed through an app.
    """

    id: Optional[str] = Field(sa_column=sa.Column(sa.String, primary_key=True, default=idg.transform))
    version: Optional[str] = Field(sa_column=sa.Column(sa.String, primary_key=True, default="0"))
    """Version identifier, defaults to `"1"`.

    Use this to label different versions of the same transform.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    name: str = Field(index=True)
    """A name for the transform, a pipeline name, or a file name of a notebook or script.
    """
    type: TransformType = Field(
        index=True,
        default=(TransformType.notebook if is_run_from_ipython else TransformType.pipeline),
    )
    """Transform type. Defaults to `notebook` if run from IPython, otherwise to `pipeline`.
    """
    title: Optional[str] = Field(index=True)
    """An additional title, like a notebook title.
    """
    reference: Optional[str] = Field(index=True)
    """Reference for the transform, e.g., a URL.
    """
    created_by: User = Relationship()
    created_by_id: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Run(SQLModel, table=True):  # type: ignore
    """Runs of data transforms.

    A `run` is any transform of a `file`.

    Args:
        id: Optional[str] = None
        name: Optional[str] = None
        load_latest: bool = False - Load latest run for given notebook or pipeline.
        transform: Optional[Transform] = None
        inputs: List[File] = None
        outputs: List[File] = None

    It typically has inputs and outputs:

    - References to outputs are stored in the `file` table in the
      `run_id` column as a foreign key the `run`
      table. This is possible as every given `file` has a unique data run:
      the `run` that produced the `file`. However, note that a given
      `run` may output several `files`.
    - References to inputs are stored in the `run_in` table, a
      many-to-many link table between the `file` and `run` tables. Any
      `file` might serve as an input for many `runs`. Similarly, any
      `run` might have many `files` as inputs.
    """

    __table_args__ = (
        ForeignKeyConstraint(
            ["transform_id", "transform_version"],
            ["lnschema_core_transform.id", "lnschema_core_transform.version"],
        ),
    )
    id: Optional[str] = Field(default_factory=idg.run, primary_key=True)
    name: Optional[str] = Field(default=None, index=True)
    external_id: Optional[str] = Field(default=None, index=True)
    transform_id: Optional[str] = Field(default=None, index=True)
    transform_version: Optional[str] = Field(default=None, index=True)
    transform: Transform = Relationship(sa_relationship_kwargs=dict(lazy="joined"))
    """Transform that is being run [pre-joined]."""
    outputs: List["File"] = Relationship(back_populates="run")
    inputs: List["File"] = Relationship(
        back_populates="input_of",
        sa_relationship_kwargs=dict(secondary=RunInput.__table__),
    )
    created_by: User = Relationship()
    created_by_id: str = CreatedBy
    created_at: datetime = CreatedAt

    _ln_identity_key: Optional[str] = PrivateAttr(default=None)
    # simulate query result

    def __init__(  # type: ignore
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        load_latest: bool = False,
        external_id: Optional[str] = None,
        transform: Optional[Transform] = None,
        inputs: List["File"] = None,
        outputs: List["File"] = None,
    ):
        kwargs = {k: v for k, v in locals().items() if v and k != "self"}

        import lamindb as ln

        global_context = False
        if transform is None:
            if ln.context.transform is not None:
                global_context = True
                transform = ln.context.transform
            else:
                raise ValueError("Either call `ln.Run(transform=transform)` or `ln.track(transform=...)`.")

        if not isinstance(transform, Transform):
            raise TypeError("transform needs to be of type Transform")

        run = None
        if load_latest:
            run = (
                ln.select(
                    ln.Run,
                    transform_id=transform.id,
                    transform_version=transform.version,
                )
                .order_by(ln.Run.created_at.desc())
                .first()
            )
            if run is not None:
                logger.info(f"Loaded: {run}")
        elif id is not None:
            run = ln.select(ln.Run, id=id).one_or_none()
            if run is None:
                raise NotImplementedError("You can currently only pass existing ids")

        if run is None:
            kwargs.update(dict(transform_id=transform.id, transform_version=transform.version))
            super().__init__(**kwargs)
            self._ln_identity_key = None
        else:
            super().__init__(**run.dict())
            self._ln_identity_key = run.id  # simulate query result

        if global_context:
            if run is None:
                added_self = ln.add(self)
                self._ln_identity_key = added_self.id
                logger.success(f"Added: {self}")
            ln.context.run = self


class Features(SQLModel, table=True):  # type: ignore
    """Feature sets.

    A feature set is represented by the hash of the set of primary keys and the feature type.

    The current supported feature types are lnschema_bionty.Gene,
    lnschema_bionty.Protein & lnschema_bionty.CellMarker.

    Guides:

    - :doc:`/guide/scrna`
    - :doc:`guide/flow`

    Examples:

    >>> import lnschema_bionty as bt
    >>> reference = bt.Gene(species="mouse")
    >>> features = ln.Features(adata, reference=reference)
    >>> file = ln.File(adata, name="Mouse Lymph Node scRNA-seq", features=features)

    Args:
        data: [Path, str, pd.DataFrame, ad.AnnData] - DataFrame or AnnData to parse.
        reference: Any = None - Reference for mapping features.
        id: str = None - Primary key.
        type: Any = None - Type of reference.
        files: List[File] - Files to link against.
    """

    id: str = Field(primary_key=True)  # use a hash
    type: str  # was called entity_type
    created_by: User = Relationship()
    created_by_id: str = CreatedBy
    created_at: datetime = CreatedAt
    files: List["File"] = Relationship(
        back_populates="features",
        sa_relationship_kwargs=dict(secondary=FileFeatures.__table__),
    )

    @overload
    def __init__(
        self,
        iterable: ListLike = None,
        field: SQLModelField = None,
        **map_kwargs,
    ):
        """Initialize from data."""
        ...

    @overload
    def __init__(
        self,
        id: Optional[str] = None,
        type: Optional[str] = None,
        files: List["File"] = [],
    ):
        """Initialize from fields."""
        ...

    def __init__(  # type: ignore
        self,
        iterable: ListLike = None,
        field: SQLModelField = None,
        *,
        id: str = None,
        type: Any = None,
        # continue with fields
        files: List["File"] = [],
        # deprecated
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        **map_kwargs,
    ):
        kwargs = locals()

        # needed for erroring when passing pd.index
        if kwargs["data"] is not None:
            kwargs.pop("data")
        if kwargs["iterable"] is not None:
            kwargs.pop("iterable")

        kwargs = {k: v for k, v in kwargs.items() if v and k != "self"}
        super().__init__(**kwargs)

    def __new__(
        cls,
        iterable: ListLike = None,
        field: SQLModelField = None,
        *,
        id: str = None,
        type: Any = None,
        # continue with fields
        files: List["File"] = [],
        # deprecated
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        **map_kwargs,
    ):
        if data is not None or iterable is not None:
            from lamindb._file import get_features_from_data

            features = get_features_from_data(
                iterable=iterable,
                field=field,
                data=data,  # deprecated
                **map_kwargs,
            )
        else:
            features = super().__new__(cls)
        return features


class Folder(SQLModel, table=True):  # type: ignore
    """See lamindb for docstring."""

    __table_args__ = (sa.UniqueConstraint("storage_id", "key", name="uq_folder_storage_key"),)

    id: str = Field(default_factory=idg.folder, primary_key=True)
    name: str = Field(index=True)
    key: Optional[str] = Field(default=None, index=True)
    storage_id: Optional[str] = Field(default=None, foreign_key="lnschema_core_storage.id", index=True)
    """Storage root id."""
    files: List["File"] = Relationship(  # type: ignore  # noqa
        back_populates="folders",
        sa_relationship_kwargs=dict(secondary=FolderFile.__table__),
    )
    """:class:`~lamindb.File`."""
    created_by: User = Relationship()
    created_by_id: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt

    # private attributes are needed here to prevent sqlalchemy error
    _local_filepath: Optional[Path] = PrivateAttr()
    _cloud_filepath: Optional[UPath] = PrivateAttr()

    @property
    def __name__(cls) -> str:
        return "Folder"

    def path(self) -> Union[Path, UPath]:
        """Path on storage."""
        return filepath_from_file_or_folder(self)

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

    @overload
    def __init__(
        self,
        path: Union[Path, UPath, str] = None,
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
        files: List["File"] = [],
    ):
        """Initialize from fields."""
        ...

    def __init__(  # type: ignore
        self,
        path: Optional[Union[Path, UPath, str]] = None,
        *,
        # continue with fields
        id: Optional[str] = None,
        name: Optional[str] = None,
        key: Optional[str] = None,
        storage_id: Optional[str] = None,
        files: List["File"] = [],
    ):
        if path is not None:
            from lamindb._folder import get_folder_kwargs_from_data

            kwargs, privates = get_folder_kwargs_from_data(
                path=path,
                name=name,
                key=key,
            )
            if id is not None:
                kwargs["id"] = id
        else:
            kwargs = {k: v for k, v in locals().items() if v and k != "self"}

        super().__init__(**kwargs)
        if path is not None:
            self._local_filepath = privates["local_filepath"]
            self._cloud_filepath = privates["cloud_filepath"]


class File(SQLModel, table=True):  # type: ignore
    """See lamindb for docstring."""

    __table_args__ = (
        sa.UniqueConstraint("storage_id", "key", name="uq_file_storage_key"),
        ForeignKeyConstraint(
            ["transform_id", "transform_version"],
            ["lnschema_core_transform.id", "lnschema_core_transform.version"],
            name="fk_file_transform_id_version_transform",
        ),
    )

    id: str = Field(default_factory=idg.file, primary_key=True)
    name: Optional[str] = Field(index=True)
    suffix: Optional[str] = Field(default=None, index=True)
    """Suffix to construct the storage key. Defaults to `None`.

    This is a file extension if the `file` is stored in a file format.
    It's `None` if the storage format doesn't have a canonical extension.
    """

    size: Optional[int] = Field(default=None, sa_column=sa.Column(sa.BigInteger(), index=True))
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    hash: Optional[str] = Field(default=None, index=True)
    """Hash (md5)."""
    key: Optional[str] = Field(default=None, index=True)
    """Storage key, the relative path within the storage location."""
    run: Optional[Run] = Relationship(back_populates="outputs")  # type: ignore
    """:class:`~lamindb.Run` that created the `file`."""
    run_id: Optional[str] = Field(foreign_key="lnschema_core_run.id", index=True)
    """Source run id."""
    transform: Transform = Relationship(sa_relationship_kwargs=dict(lazy="joined"))  # type: ignore
    """:class:`~lamindb.Transform` whose run created the `file` [pre-joined]."""
    transform_id: Optional[str] = Field(index=True)
    """Source transform id."""
    transform_version: Optional[str] = Field(index=True)
    """Source transform version."""
    storage: Storage = Relationship(sa_relationship_kwargs=dict(lazy="joined"))  # type: ignore
    """:class:`~lamindb.Storage` location of `file` [pre-joined], see `.path()` for full path."""
    storage_id: str = Field(foreign_key="lnschema_core_storage.id", index=True)
    """Storage root id."""
    features: List[Features] = Relationship(
        back_populates="files",
        sa_relationship_kwargs=dict(secondary=FileFeatures.__table__),
    )
    """Feature sets indexing this file."""
    folders: List[Folder] = Relationship(
        back_populates="files",
        sa_relationship_kwargs=dict(secondary=FolderFile.__table__),
    )
    """Folders that contain this file."""
    input_of: List[Run] = Relationship(  # type: ignore
        back_populates="inputs",
        sa_relationship_kwargs=dict(secondary=RunInput.__table__),
    )
    """Runs that use this file as input."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
    created_by: User = Relationship(sa_relationship_kwargs=dict(lazy="joined"))
    """User who created the file [pre-joined]."""
    created_by_id: Optional[str] = CreatedBy  # make non-optional over time

    # private attributes are needed here to prevent sqlalchemy error
    _local_filepath: Optional[Path] = PrivateAttr()
    _cloud_filepath: Optional[UPath] = PrivateAttr()
    _clear_storagekey: Optional[str] = PrivateAttr()
    _memory_rep: Any = PrivateAttr()
    _to_store: bool = PrivateAttr()  # indicate whether upload needed

    def path(self) -> Union[Path, UPath]:
        """Path on storage."""
        return filepath_from_file_or_folder(self)

    # likely needs an arg `key`
    def replace(
        self,
        data: Union[PathLike, DataLike],
        run: Optional[Run] = None,
        format: Optional[str] = None,
    ) -> None:
        """Replace data object."""
        from lamindb._file import get_file_kwargs_from_data

        if isinstance(data, (Path, str)):
            name_to_pass = None
        else:
            name_to_pass = self.name

        kwargs, privates = get_file_kwargs_from_data(
            data=data,
            name=name_to_pass,
            run=run,
            format=format,
        )

        if kwargs["name"] != self.name:
            logger.warning(f"Your new filename '{kwargs['name']}' does not match the previous filename '{self.name}': to update the name, set file.name = '{kwargs['name']}'")

        if self.key is not None:
            key_path = PurePosixPath(self.key)
            if isinstance(data, (Path, str)):
                new_name = kwargs["name"]  # use the name from the data filepath
            else:
                # do not change the key stem to file.name
                new_name = key_path.stem  # use the stem of the key for in-memory data
            if PurePosixPath(new_name).suffixes == []:
                new_name = f"{new_name}{kwargs['suffix']}"
            if key_path.name != new_name:
                self._clear_storagekey = self.key
                self.key = str(key_path.with_name(new_name))
                logger.warning(f"Replacing the file will also replace the key from '{key_path}' to '{self.key}', and delete '{key_path}' upon `ln.add`")
        else:
            self.key = kwargs["key"]
            old_storage = f"{self.id}{self.suffix}"
            new_storage = self.key if self.key is not None else f"{self.id}{kwargs['suffix']}"
            if old_storage != new_storage:
                self._clear_storagekey = old_storage

        self.suffix = kwargs["suffix"]
        self.size = kwargs["size"]
        self.hash = kwargs["hash"]
        self.run = kwargs["run"]
        self._local_filepath = privates["local_filepath"]
        self._cloud_filepath = privates["cloud_filepath"]
        self._memory_rep = privates["memory_rep"]
        self._to_store = not privates["check_path_in_storage"]  # no need to upload if new file is already in storage

    @property
    def __name__(cls) -> str:
        return "File"

    def __init__(  # type: ignore
        self,
        data: Union[PathLike, DataLike] = None,
        *,
        key: Optional[str] = None,
        name: Optional[str] = None,
        run: Optional[Run] = None,
        format: Optional[str] = None,
        features: List[Features] = None,
        id: Optional[str] = None,
        input_of: List[Run] = None,
    ):
        if features is None:
            features = []
        if input_of is None:
            input_of = []
        if not isinstance(features, List):
            features = [features]

        def log_hint(*, check_path_in_storage: bool, key: str, id: str, suffix: str) -> None:
            hint = ""
            if check_path_in_storage:
                hint += "file in storage ✓"
            else:
                hint += "file will be copied to storage upon `ln.add()`"
            if key is None:
                hint += f" using storage key = {id}{suffix}"
            else:
                hint += f" using storage key = {key}"
            logger.hint(hint)

        from lamindb._file import get_file_kwargs_from_data

        kwargs, privates = get_file_kwargs_from_data(
            data=data,
            name=name,
            key=key,
            run=run,
            format=format,
        )
        kwargs["id"] = idg.file() if id is None else id
        if features is not None:
            kwargs["features"] = features
        log_hint(
            check_path_in_storage=privates["check_path_in_storage"],
            key=kwargs["key"],
            id=kwargs["id"],
            suffix=kwargs["suffix"],
        )

        # transform cannot be directly passed, just via run
        # it's directly stored in the file table to avoid another join
        # mediate by the run table
        if kwargs["run"] is not None:
            if kwargs["run"].transform_id is not None:
                kwargs["transform_id"] = kwargs["run"].transform_id
                assert kwargs["run"].transform_version is not None
                kwargs["transform_version"] = kwargs["run"].transform_version
            else:
                # accessing the relationship should always be possible if
                # the above if clause was false as then, we should have a fresh
                # Transform object that is not queried from the DB
                assert kwargs["run"].transform is not None
                kwargs["transform"] = kwargs["run"].transform

        super().__init__(**kwargs)
        if data is not None:
            self._local_filepath = privates["local_filepath"]
            self._cloud_filepath = privates["cloud_filepath"]
            self._memory_rep = privates["memory_rep"]
            self._to_store = not privates["check_path_in_storage"]


# add type annotations back asap when re-organizing the module
def storage_key_from_file(file: File):
    if file.key is None:
        return f"{file.id}{file.suffix}"
    else:
        return file.key


# add type annotations back asap when re-organizing the module
def filepath_from_file_or_folder(file_or_folder: Union[File, Folder]):
    from lndb.dev import StorageSettings

    from lndb import settings

    # using __name__ for type check to avoid need of
    # dynamically importing the type
    if file_or_folder.__name__ == "File":
        storage_key = storage_key_from_file(file_or_folder)
    else:
        storage_key = file_or_folder.key
        if storage_key is None:
            raise ValueError("Only real folders have a path!")
    if file_or_folder.storage_id == settings.storage.id:
        path = settings.storage.key_to_filepath(storage_key)
    else:
        logger.warning(
            "file.path() is slow for files outside the currently configured storage"
            " location\nconsider joining for the set of files you're interested in:"
            " ln.select(ln.File, ln.Storage)the path is storage.root / file.key if"
            " file.key is not None\notherwise storage.root / (file.id + file.suffix)"
        )
        import lamindb as ln

        storage = ln.select(ln.Storage, id=file_or_folder.storage_id).one()
        # find a better way than passing None to instance_settings in the future!
        storage_settings = StorageSettings(storage.root, instance_settings=None)
        path = storage_settings.key_to_filepath(storage_key)
    return path
