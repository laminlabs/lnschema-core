import builtins
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, List, NamedTuple, Optional, Union

import pandas as pd
from django.db import models
from lamin_logger import logger
from upath import UPath

from . import ids
from ._lookup import lookup as _lookup
from ._users import current_user_id
from .types import DataLike, PathLike, TransformType

is_run_from_ipython = getattr(builtins, "__IPYTHON__", False)
TRANSFORM_TYPE_DEFAULT = TransformType.notebook if is_run_from_ipython else TransformType.pipeline


class NoResultFound(Exception):
    pass


class MultipleResultsFound(Exception):
    pass


class LaminQuerySet(models.QuerySet):
    """Extension of Django QuerySet.

    This brings some of the SQLAlchemy/SQLModel/SQL-inspired calls.

    As LaminDB was based on SQLAlchemy/SQLModel in the beginning, and might
    support it again in the future, these calls will be supported longtime.
    """

    def df(self):
        columns = [field.name for field in self.model._meta.fields]
        df = pd.DataFrame(self.values(), columns=columns)
        if "id" in df.columns:
            df = df.set_index("id")
        return df

    def list(self) -> List:
        return list(self)

    def first(self):
        if len(self) == 0:
            return None
        return self[0]

    def one(self):
        if len(self) == 0:
            raise NoResultFound
        elif len(self) > 1:
            raise MultipleResultsFound
        else:
            return self[0]

    def one_or_none(self):
        if len(self) == 0:
            return None
        elif len(self) == 1:
            return self[0]
        else:
            raise MultipleResultsFound


# todo, make a CreatedUpdated Mixin, but need to figure out docs
class BaseORM(models.Model):
    def __repr__(self) -> str:
        fields = ", ".join([f"{k.name}={getattr(self, k.name)}" for k in self._meta.fields if hasattr(self, k.name)])
        return f"{self.__class__.__name__}({fields})"

    @classmethod
    def lookup(cls, field: Optional[str] = None) -> NamedTuple:
        return _lookup(cls, field)

    def __str__(self) -> str:
        return self.__repr__()

    class Meta:
        abstract = True


class RunInput(BaseORM):
    run = models.ForeignKey("Run", on_delete=models.CASCADE)
    file = models.ForeignKey("File", on_delete=models.CASCADE)

    class Meta:
        managed = True


class User(BaseORM):
    """User accounts.

    All data in this table is synched from the cloud user account to ensure a
    globally unique user identity.
    """

    id = models.CharField(max_length=8, primary_key=True)
    """Universal id, valid across DB instances."""
    handle = models.CharField(max_length=30, unique=True, db_index=True)
    """Universal handle, valid across DB instances."""
    email = models.CharField(max_length=255, unique=True, db_index=True)
    """Latest email address."""
    name = models.CharField(max_length=255, db_index=True)
    """Name."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""

    class Meta:
        managed = True


class Storage(BaseORM):
    """Storage locations, typically cloud buckets.

    A file or run-associated file can be stored in any desired S3,
    GCP bucket or local storage location.

    This table tracks these locations along with metadata.
    """

    id = models.CharField(max_length=8, default=ids.storage, db_index=True, primary_key=True)
    """Universal id, valid across DB instances."""
    root = models.CharField(max_length=255, db_index=True)
    """Path to the root of the storage location: an s3 path, a local path, etc."""
    type = models.CharField(max_length=63, db_index=True)
    """Local vs. s3 vs. gcp etc."""
    region = models.CharField(max_length=63, db_index=True, null=True)
    """Cloud storage region, if applicable."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        default=current_user_id,
        related_name="created_storages",
    )
    """Creator of record."""

    class Meta:
        managed = True


class Project(BaseORM):
    """Projects."""

    id = models.CharField(max_length=8, default=ids.project, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, unique=True)
    """Project name or title."""
    external_id = models.CharField(max_length=255, db_index=True)
    """External id (such as from a project management tool)."""
    folders = models.ManyToManyField("Folder", related_name="projects")
    """Project folders."""
    files = models.ManyToManyField("File", related_name="projects")
    """Project files."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        default=current_user_id,
        related_name="created_projects",
    )
    """Creator of record."""

    class Meta:
        managed = True


class Transform(BaseORM):
    """Data transformations.

    Pipelines, workflows, notebooks, app-based transforms.

    A pipeline is versioned software that transforms data.
    This can be anything from typical workflow tools (Nextflow, Snakemake,
    Prefect, Apache Airflow, etc.) to simple (versioned) scripts.

    Creating a file is a transform, too.
    """

    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """A name for the transform, a pipeline name, or a file name of a notebook or script.
    """
    title = models.TextField(db_index=True, null=True, default=None)
    """An additional title, like a notebook title.
    """
    uid = models.CharField(max_length=12, default=ids.transform, db_index=True)
    """Universal id, valid across DB instances."""
    version = models.CharField(max_length=10, default=None, db_index=True, null=True)
    """Version identifier, defaults to `"0"`.

    Use this to label different versions of the same transform.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    type = models.CharField(
        max_length=20,
        choices=TransformType.choices(),
        db_index=True,
        default=TRANSFORM_TYPE_DEFAULT,
    )
    """Transform type.

    Defaults to `notebook` if run from IPython, from a script to `pipeline`.

    If run from the app, it defaults to `app`.
    """
    reference = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Reference for the transform, e.g., a URL.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        default=current_user_id,
        related_name="created_transforms",
    )
    """Creator of record."""

    class Meta:
        managed = True
        unique_together = (("uid", "version"),)


class Run(BaseORM):
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

    id = models.CharField(max_length=20, default=ids.run, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True)
    """Name or title of run."""
    external_id = models.CharField(max_length=255, db_index=True)
    """External id (such as from a workflow tool)."""
    transform = models.ForeignKey(Transform, models.DO_NOTHING, related_name="runs")
    """The transform :class:`~lamindb.Transform` that is being run."""
    inputs = models.ManyToManyField("File", through=RunInput, related_name="input_of")
    """The input files for the run."""
    # outputs on File
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id, related_name="created_runs")
    """Creator of record."""

    class Meta:
        managed = True


class Featureset(BaseORM):
    """Feature sets.

    A feature set is represented by the hash of the set of primary keys and the feature type.

    The current supported feature types are lnschema_bionty.Gene,
    lnschema_bionty.Protein & lnschema_bionty.CellMarker.

    Guides:

    - :doc:`/biology/scrna`
    - :doc:`/biology/flow`

    Examples:

    >>> import lnschema_bionty as bt
    >>> reference = bt.Gene(species="mouse")
    >>> features = ln.Features(adata, reference=reference)
    >>> file = ln.File(adata, name="Mouse Lymph Node scRNA-seq", features=features)

    Args:
        data: [Path, str, pd.DataFrame, ad.AnnData] - DataFrame or AnnData to parse.
        reference: Any = None - Reference for mapping features.
    """

    id = models.CharField(max_length=64, primary_key=True)
    """A universal id, valid across DB instances: a hash of the linked set of features."""
    type = models.CharField(max_length=64)
    """A feature entity type."""
    files = models.ManyToManyField("File", related_name="featuresets")
    """Files linked to the featureset."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        default=current_user_id,
        related_name="created_featuresets",
    )
    """Creator of record."""

    class Meta:
        managed = True

    @classmethod
    def from_iterable(
        cls,
        iterable: Iterable,
        field: models.CharField,
        species: str = None,
    ):
        """Parse iterable & return featureset & records."""
        from lamindb._features import parse_features_from_iterable

        features = parse_features_from_iterable(
            iterable=iterable,
            field=field,
            species=species,
        )
        return features

    def __init__(self, *args, **kwargs):  # type: ignore
        relationships: Dict = {}
        if "genes" in kwargs:
            relationships["genes"] = kwargs.pop("genes")
        if "proteins" in kwargs:
            relationships["proteins"] = kwargs.pop("proteins")
        if "cell_markers" in kwargs:
            relationships["cell_markers"] = kwargs.pop("cell_markers")
        self._relationships = relationships

        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for key, records in self._relationships.items():
            [r.save() for r in records]
            getattr(self, key).set(records)


class Folder(BaseORM):
    id = models.CharField(max_length=20, default=ids.folder, primary_key=True)
    """A universal random id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True)
    """Name or title of the folder."""
    key = models.CharField(max_length=255, null=True, default=None, db_index=True)
    """Storage key of the folder."""
    storage = models.ForeignKey(Storage, models.DO_NOTHING, related_name="folders", null=True)
    """Storage location of the folder."""
    files = models.ManyToManyField("File", related_name="folders")
    """Files in folder."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id, related_name="created_folders")
    """Creator of record."""

    class Meta:
        managed = True
        unique_together = (("storage", "key"),)

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

    def __init__(self, *args, **kwargs):  # type: ignore
        if len(args) > 1 and isinstance(args[0], str) and len(args[0]) == 20:  # initialize with all fields from db as args
            super().__init__(*args, **kwargs)
            return None
        else:  # user-facing calling signature
            if len(args) != 1 and "files" not in kwargs:
                raise ValueError("Either provide path as arg or provide files as kwarg!")
            if len(args) == 1:
                path: Optional[Union[Path, UPath, str]] = args[0]
            else:
                path = None
            name: Optional[str] = kwargs.pop("name") if "name" in kwargs else None
            key: Optional[str] = kwargs.pop("key") if "key" in kwargs else None
            files: Optional[str] = kwargs.pop("files") if "files" in kwargs else None
            if len(kwargs) != 0:
                raise ValueError(f"This kwargs are not permitted: {kwargs}")

        from lamindb._folder import get_folder_kwargs_from_data

        if path is not None:
            kwargs, privates = get_folder_kwargs_from_data(
                path=path,
                name=name,
                key=key,
            )
            files = kwargs.pop("files")
        else:
            kwargs = dict(name=name)
        kwargs["id"] = ids.folder()
        super().__init__(**kwargs)
        if path is not None:
            self._local_filepath = privates["local_filepath"]
            self._cloud_filepath = privates["cloud_filepath"]
            self._files = files


class File(BaseORM):
    id = models.CharField(max_length=20, primary_key=True)
    """A universal random id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """A universal random id, valid across DB instances."""
    suffix = models.CharField(max_length=30, db_index=True, null=True, default=None)
    """File suffix.

    This is a file extension if the `file` is stored in a file format.
    It's `None` if the storage format doesn't have a canonical extension.
    """
    size = models.BigIntegerField(null=True, db_index=True)
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    hash = models.CharField(max_length=86, db_index=True, null=True, default=None)
    """Hash of file content. 86 base64 chars allow to store 64 bytes, 512 bits."""
    key = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Storage key, the relative path within the storage location."""
    run = models.ForeignKey(Run, models.DO_NOTHING, related_name="outputs", null=True)
    """:class:`~lamindb.Run` that created the `file`."""
    transform = models.ForeignKey(Transform, models.DO_NOTHING, related_name="files", null=True)
    """:class:`~lamindb.Transform` whose run created the `file`."""
    storage: "Storage" = models.ForeignKey(Storage, models.DO_NOTHING, related_name="files")
    """:class:`~lamindb.Storage` location of `file`, see `.path()` for full path."""
    # folders from Folders.files
    # features from Features.files
    # input_of from Run.inputs
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id, related_name="created_files")
    """Creator of record."""

    class Meta:
        managed = True
        unique_together = (("storage", "key"),)

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
        """Replace file content."""
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
        *args,
        **kwargs,
    ):
        if len(args) > 1 and isinstance(args[0], str) and len(args[0]) == 20:  # initialize with all fields from db as args
            super().__init__(*args, **kwargs)
            return None
        else:  # user facing calling signature
            if len(args) > 1:
                raise ValueError("Only one non-keyword arg allowed")
            if len(args) == 0:
                data: Union[PathLike, DataLike] = kwargs["data"]
            else:
                data: Union[PathLike, DataLike] = args[0]
            key: Optional[str] = kwargs["key"] if "key" in kwargs else None
            name: Optional[str] = kwargs["name"] if "name" in kwargs else None
            run: Optional[Run] = kwargs["run"] if "run" in kwargs else None
            format = kwargs["format"] if "format" in kwargs else None

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
        kwargs["id"] = ids.file()
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

    def save(self, *args, **kwargs):
        if self.transform is not None:
            self.transform.save()
        if self.run is not None:
            self.run.save()
        super().save(*args, **kwargs)


# add type annotations back asap when re-organizing the module
def storage_key_from_file(file: File):
    if file.key is None:
        return f"{file.id}{file.suffix}"
    else:
        return file.key


# add type annotations back asap when re-organizing the module
def filepath_from_file_or_folder(file_or_folder: Union[File, Folder]):
    from lamindb_setup import settings
    from lamindb_setup.dev import StorageSettings

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
