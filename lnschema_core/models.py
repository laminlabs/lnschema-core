import builtins
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, NamedTuple, Optional, Union

from django.db import models
from django.db.models import PROTECT, Manager
from lamin_logger import logger
from upath import UPath

from . import ids
from ._lookup import lookup as _lookup
from ._queryset import QuerySet
from .types import DataLike, PathLike, TransformType
from .users import current_user_id

is_run_from_ipython = getattr(builtins, "__IPYTHON__", False)
TRANSFORM_TYPE_DEFAULT = TransformType.notebook if is_run_from_ipython else TransformType.pipeline


def validate_required_fields(orm, kwargs):
    required_fields = {k.name for k in orm._meta.fields if not k.null and k.default is None}
    required_fields_not_passed = {k: None for k in required_fields if k not in kwargs}
    kwargs.update(required_fields_not_passed)
    missing_fields = [k for k, v in kwargs.items() if v is None and k in required_fields]
    if missing_fields:
        raise TypeError(f"{missing_fields} are required.")


# todo, make a CreatedUpdated Mixin, but need to figure out docs
class BaseORM(models.Model):
    """Base data model.

    Is essentially equal to the Django Model base class, but adds the following
    methods.
    """

    def __repr__(self) -> str:
        fields = [field.name for field in self._meta.fields if not isinstance(field, models.ForeignKey)]
        fields += [f"{field.name}_id" for field in self._meta.fields if isinstance(field, models.ForeignKey)]
        fields_str = ", ".join([f"{k}={getattr(self, k)}" for k in fields if hasattr(self, k)])
        return f"{self.__class__.__name__}({fields_str})"

    def __str__(self) -> str:
        return self.__repr__()

    def __init__(self, *args, **kwargs):
        if not args:  # object is loaded from DB
            validate_required_fields(self, kwargs)
        super().__init__(*args, **kwargs)

    @classmethod
    def lookup(cls, field: Optional[str] = None) -> NamedTuple:
        """Lookup object for auto-completing field values."""
        return _lookup(cls, field)

    @classmethod
    def select(cls, **expressions) -> Union[QuerySet, Manager]:
        """Query the ORM."""
        from lamindb._select import select

        return select(cls, **expressions)

    class Meta:
        abstract = True


# A note on required fields at the ORM level
#
# As Django does most of its validation on the Form-level, it doesn't offer functionality
# for validating the integrity of an ORM object upon instantation (similar to pydantic)
#
# For required fields, we define them as commonly done on the SQL level together
# with a validator in BaseORM (validate_required_fields)
#
# This goes against the Django convention, but goes with the SQLModel convention
# (Optional fields can be null on the SQL level, non-optional fields cannot)
#
# Due to Django's convention where CharField has pre-configured (null=False, default=""), marking
# a required field necessitates passing `default=None`. Without the validator it would trigger
# an error at the SQL-level, with it, it triggers it at instantiation


class User(BaseORM):
    """User accounts.

    All data in this table is synched from the cloud user account to ensure a
    universal user identity, valid across DB instances, email & handle changes.
    """

    id = models.CharField(max_length=8, primary_key=True, default=None)
    """Universal id, valid across DB instances."""
    handle = models.CharField(max_length=30, unique=True, db_index=True, default=None)
    """Universal handle, valid across DB instances."""
    email = models.CharField(max_length=255, unique=True, db_index=True, default=None)
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
    """Storage locations, typically cloud storage buckets.

    A file can be stored in S3 and GCP buckets or local storage locations.

    This ORM tracks these locations along with metadata.
    """

    id = models.CharField(max_length=8, default=ids.storage, db_index=True, primary_key=True)
    """Universal id, valid across DB instances."""
    root = models.CharField(max_length=255, db_index=True, default=None)
    """Path to the root of the storage location (an s3 path, a local path, etc.)."""
    type = models.CharField(max_length=30, db_index=True)
    """Local vs. s3 vs. gcp etc."""
    region = models.CharField(max_length=63, db_index=True, null=True, default=None)
    """Cloud storage region, if applicable."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        PROTECT,
        default=current_user_id,
        related_name="created_storages",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        managed = True


class Project(BaseORM):
    """Projects."""

    id = models.CharField(max_length=8, default=ids.project, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, unique=True, default=None)
    """Project name or title."""
    external_id = models.CharField(max_length=255, db_index=True, null=True, default=None)
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
        PROTECT,
        default=current_user_id,
        related_name="created_projects",
    )
    """Creator of record, a :class:`~lamindb.User`."""

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

    id = models.CharField(max_length=14, db_index=True, primary_key=True, default=None)
    """Universal id, composed of stem_id and version suffix."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Transform name or title, a pipeline name, notebook title, etc..
    """
    short_name = models.CharField(max_length=30, db_index=True, null=True, default=None)
    """A short name.
    """
    stem_id = models.CharField(max_length=12, default=ids.transform, db_index=True)
    """Stem of id, identifying transform up to version."""
    version = models.CharField(max_length=10, default="0", db_index=True)
    """Version, defaults to `"0"`.

    Use this to label different versions of the same pipeline, notebook, etc.

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

    Defaults to `notebook` if run from ipython and to `pipeline` if run from python.

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
        PROTECT,
        default=current_user_id,
        related_name="created_transforms",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        managed = True
        unique_together = (("stem_id", "version"),)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:  # initialize with all fields from db as args
            super().__init__(*args, **kwargs)
            return None
        else:  # user-facing calling signature
            # set default ids
            if "id" not in kwargs and "stem_id" not in kwargs:
                kwargs["id"] = ids.base62(n_char=14)
                kwargs["stem_id"] = kwargs["id"][:12]
            elif "stem_id" in kwargs:
                assert isinstance(kwargs["stem_id"], str) and len(kwargs["stem_id"]) == 12
                kwargs["id"] = kwargs["stem_id"] + ids.base62(n_char=2)
            elif "id" in kwargs:
                assert isinstance(kwargs["id"], str) and len(kwargs["id"]) == 14
                kwargs["stem_id"] = kwargs["id"][:12]
            super().__init__(**kwargs)


class Run(BaseORM):
    """Runs of data transformations.

    Typically, a run has inputs and outputs:

    - References to outputs are stored in the `File` ORM in the `run` field.
      This is possible as every given file has a unique run that created it. Any
      given `Run` can output multiple `files`: `run.outputs`.
    - References to inputs are stored in the `RunInput` ORM, a many-to-many link
      ORM between `File` and `Run`. Any `file` might serve as an input for
      multiple `runs`: `file.input_of`. Similarly, any `run` might have many
      `files` as inputs: `run.inputs`.
    """

    id = models.CharField(max_length=20, default=ids.run, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Name or title of run."""
    external_id = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """External id (such as from a workflow tool)."""
    transform = models.ForeignKey(Transform, PROTECT, related_name="runs")
    """The transform :class:`~lamindb.Transform` that is being run."""
    inputs = models.ManyToManyField("File", through="RunInput", related_name="input_of")
    """The input files for the run."""
    # outputs on File
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    run_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_runs")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        managed = True


class Featureset(BaseORM):
    """Feature sets.

    A feature set is represented by the hash of the set of primary keys and the feature type.

    The current supported feature types are `lnschema_bionty.Gene`,
    `lnschema_bionty.Protein`, and `lnschema_bionty.CellMarker`.

    Guides:

    - :doc:`/biology/scrna`
    - :doc:`/biology/flow`

    Examples:

    >>> import lnschema_bionty as bt
    >>> reference = bt.Gene(species="mouse")
    >>> features = ln.Features.from_iterable(adata.var["ensemble_id"], Gene.ensembl_gene_id)
    >>> features.save()
    >>> file = ln.File(adata, name="Mouse Lymph Node scRNA-seq")
    >>> file.save()
    >>> file.featuresets.add(featureset)

    """

    id = models.CharField(max_length=64, primary_key=True, default=None)
    """A universal id, valid across DB instances, a hash of the linked set of features."""
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
        PROTECT,
        default=current_user_id,
        related_name="created_featuresets",
    )
    """Creator of record, a :class:`~lamindb.User`."""

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
        related_names = [i.related_name for i in self.__class__._meta.related_objects]

        relationships: Dict = {}
        for related_name in related_names:
            if related_name in kwargs:
                relationships[related_name] = kwargs.pop(related_name)
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
    name = models.CharField(max_length=255, db_index=True, default=None)
    """Name or title of folder."""
    # below is one of the few cases with null=True, default=None
    key = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Storage key of folder."""
    storage = models.ForeignKey(Storage, PROTECT, related_name="folders", null=True)
    """:class:`~lamindb.Storage` location of folder, see `.path()` for full path."""
    files = models.ManyToManyField("File", related_name="folders")
    """:class:`~lamindb.File` records in folder."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_folders")
    """Creator of record, a :class:`~lamindb.User`."""

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
    # below is one of the few cases with null=True, default=None
    key = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Storage key, the relative path within the storage location."""
    run = models.ForeignKey(Run, PROTECT, related_name="outputs", null=True)
    """:class:`~lamindb.Run` that created the `file`."""
    transform = models.ForeignKey(Transform, PROTECT, related_name="files", null=True)
    """:class:`~lamindb.Transform` whose run created the `file`."""
    storage: "Storage" = models.ForeignKey(Storage, PROTECT, related_name="files")
    """:class:`~lamindb.Storage` location of `file`, see `.path()` for full path."""
    # folders from Folders.files
    # features from Features.files
    # input_of from Run.inputs
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_files")
    """Creator of record, a :class:`~lamindb.User`."""

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
                logger.warning(f"Replacing the file will replace key '{key_path}' with '{self.key}' and delete '{key_path}' upon `save()`")
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
                hint += "file will be copied to storage upon `save()`"
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

    def save(self, *args, **kwargs) -> None:
        """Save the file to database & storage."""
        if self.transform is not None:
            self.transform.save()
        if self.run is not None:
            self.run.save()
        super().save(*args, **kwargs)


class RunInput(BaseORM):
    run = models.ForeignKey("Run", on_delete=models.CASCADE)
    file = models.ForeignKey("File", on_delete=models.CASCADE)

    class Meta:
        managed = True


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
