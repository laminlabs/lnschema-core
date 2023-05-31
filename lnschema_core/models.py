from pathlib import Path, PurePosixPath
from typing import Any, List, Optional, Union

from django.db import models
from django.db.models import Model as BaseORM
from lamin_logger import logger
from nbproject._is_run_from_ipython import is_run_from_ipython
from upath import UPath

from ._users import current_user_id_as_int
from .types import DataLike, ListLike, PathLike, TransformType


class RunInput(models.Model):
    run = models.ForeignKey("Run", on_delete=models.CASCADE)
    file = models.ForeignKey("File", on_delete=models.CASCADE)

    class Meta:
        managed = True


class User(BaseORM):
    email = models.CharField(max_length=64, unique=True)
    handle = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Storage(BaseORM):
    root = models.CharField(max_length=255)
    type = models.CharField(max_length=63, blank=True, null=True)
    region = models.CharField(max_length=63, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, default=current_user_id_as_int)

    class Meta:
        managed = True


class Project(BaseORM):
    name = models.CharField(max_length=64)
    folders = models.ManyToManyField("Folder")
    files = models.ManyToManyField("File")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id_as_int)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Transform(models.Model):
    name = models.CharField(max_length=63)
    version = models.CharField(max_length=63)
    type = models.CharField(max_length=63, choices=TransformType.choices(), db_index=True, default=(TransformType.notebook if is_run_from_ipython else TransformType.pipeline))
    title = models.CharField(max_length=63, blank=True, null=True)
    reference = models.CharField(max_length=63, blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "version"),)


class Run(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    transform = models.ForeignKey(Transform, models.DO_NOTHING)
    inputs = models.ManyToManyField("File", through=RunInput, related_name="input_of")
    # outputs on File
    created_by = models.ForeignKey(User, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True

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


class Features(models.Model):
    id = models.CharField(max_length=63, primary_key=True)
    type = models.CharField(max_length=63)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id_as_int)
    created_at = models.DateTimeField(auto_now=True)
    files = models.ManyToManyField("File")

    class Meta:
        managed = True

    def __init__(  # type: ignore
        self,
        iterable: ListLike = None,
        field: models.CharField = None,
        *,
        id: str = None,
        type: Any = None,
        # continue with fields
        files: List["File"] = [],
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
        field: models.CharField = None,
        *,
        id: str = None,
        type: Any = None,
        # continue with fields
        files: List["File"] = [],
        **map_kwargs,
    ):
        if iterable is not None:
            from lamindb._file import get_features_from_data

            features = get_features_from_data(
                iterable=iterable,
                field=field,
                **map_kwargs,
            )
        else:
            features = super().__new__(cls)
        return features


class Folder(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255, blank=True, null=True)
    storage = models.ForeignKey(Storage, models.DO_NOTHING)
    files = models.ManyToManyField("File")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id_as_int)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

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


class File(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    suffix = models.CharField(max_length=63, blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True)
    hash = models.CharField(max_length=63, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    run = models.ForeignKey(Run, models.DO_NOTHING, blank=True, null=True, related_name="outputs")
    transform = models.ForeignKey(Transform, models.DO_NOTHING, blank=True, null=True)
    storage = models.ForeignKey(Storage, models.DO_NOTHING)
    # folders from Folders.files
    # features from Features.files
    # input_of from Run.inputs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id_as_int)

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
