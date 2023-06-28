import builtins
from datetime import datetime
from typing import Any, Dict, Iterable, NamedTuple, Optional, Union, overload  # noqa

from django.db import models
from django.db.models import PROTECT, Manager

from ._queryset import QuerySet
from .ids import base62_8, base62_12, base62_20
from .types import TransformType
from .users import current_user_id

is_run_from_ipython = getattr(builtins, "__IPYTHON__", False)
TRANSFORM_TYPE_DEFAULT = TransformType.notebook if is_run_from_ipython else TransformType.pipeline


def format_datetime(dt: Union[datetime, Any]) -> str:
    if not isinstance(dt, datetime):
        return dt
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


# todo, make a CreatedUpdated Mixin, but need to figure out docs
class BaseORM(models.Model):
    """Base data model.

    Is essentially equal to the Django Model base class, but adds the following
    methods.
    """

    def __repr__(self) -> str:
        field_names = [field.name for field in self._meta.fields if not isinstance(field, (models.ForeignKey, models.DateTimeField))]
        # skip created_at
        field_names += [field.name for field in self._meta.fields if isinstance(field, models.DateTimeField) and field.name != "created_at"]
        field_names += [f"{field.name}_id" for field in self._meta.fields if isinstance(field, models.ForeignKey)]
        fields_str = {k: format_datetime(getattr(self, k)) for k in field_names if hasattr(self, k)}
        fields_joined_str = ", ".join([f"{k}={fields_str[k]}" for k in fields_str])
        return f"{self.__class__.__name__}({fields_joined_str})"

    def __str__(self) -> str:
        return self.__repr__()

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

# A note on class and instance methods of core ORM
#
# All of these are defined and tested within lamindb, in files starting with _{orm_name}.py


class User(BaseORM):
    """Users.

    All data in this table is synched from the cloud user account to ensure a
    universal user identity, valid across DB instances, email & handle changes.
    """

    id = models.CharField(max_length=8, primary_key=True, default=None)
    """Universal id, valid across DB instances."""
    handle = models.CharField(max_length=30, unique=True, db_index=True, default=None)
    """Universal handle, valid across DB instances (required)."""
    email = models.CharField(max_length=255, unique=True, db_index=True, default=None)
    """Email address (required)."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Name (optional)."""  # has to match hub specification, where it's also optional
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""


class Storage(BaseORM):
    """Storage locations.

    Either S3 or GCP buckets or local storage locations.
    """

    id = models.CharField(max_length=8, default=base62_8, db_index=True, primary_key=True)
    """Universal id, valid across DB instances."""
    root = models.CharField(max_length=255, db_index=True, default=None)
    """Root path of storage, an s3 path, a local path, etc. (required)."""
    type = models.CharField(max_length=30, db_index=True)
    """Local vs. s3 vs. gcp etc."""
    region = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Cloud storage region, if applicable."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_storages")
    """Creator of record, a :class:`~lamindb.User`."""


class Tag(BaseORM):
    """Tags."""

    id = models.CharField(max_length=8, default=base62_8, primary_key=True)
    """A universal random id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, unique=True, default=None)
    """Name or title of tag."""
    files = models.ManyToManyField("File", related_name="tags")
    """:class:`~lamindb.File` records in tag."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_tags")
    """Creator of record, a :class:`~lamindb.User`."""


class Project(BaseORM):
    """Projects."""

    id = models.CharField(max_length=8, default=base62_8, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, unique=True, default=None)
    """Project name or title."""
    external_id = models.CharField(max_length=40, db_index=True, null=True, default=None)
    """External id (such as from a project management tool)."""
    tags = models.ManyToManyField("Tag", related_name="projects")
    """Project tags."""
    files = models.ManyToManyField("File", related_name="projects")
    """Project files."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_projects")
    """Creator of record, a :class:`~lamindb.User`."""


class Transform(BaseORM):
    """Transformations of files (:class:`~lamindb.File`).

    Pipelines, workflows, notebooks, app-based transformations.

    A pipeline is versioned software that transforms data.
    This can be anything from typical workflow tools (Nextflow, Snakemake,
    Prefect, Apache Airflow, etc.) to simple (versioned) scripts.
    """

    id = models.CharField(max_length=14, db_index=True, primary_key=True, default=None)
    """Universal id, composed of stem_id and version suffix."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Transform name or title, a pipeline name, notebook title, etc..
    """
    short_name = models.CharField(max_length=128, db_index=True, null=True, default=None)
    """A short name.
    """
    stem_id = models.CharField(max_length=12, default=base62_12, db_index=True)
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
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_transforms")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("stem_id", "version"),)


class Run(BaseORM):
    """Runs of transformations (:class:`~lamindb.Transform`).

    Typically, a run has inputs and outputs:

    - References to outputs are stored in :class:`~lamindb.File` in the `run` field.
      This is possible as every given file has a unique run that created it. Any
      given `Run` can output multiple `files`: `run.outputs`.
    - References to inputs are stored in the :class:`~lamindb.File` in the
      `input_of` field. Any `file` might serve as an input for multiple `runs`.
      Similarly, any `run` might have many `files` as inputs: `run.inputs`.
    """

    id = models.CharField(max_length=20, default=base62_20, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Name or title of run."""
    external_id = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """External id (such as from a workflow tool)."""
    transform = models.ForeignKey(Transform, PROTECT, related_name="runs")
    """The transform :class:`~lamindb.Transform` that is being run."""
    inputs = models.ManyToManyField("File", related_name="input_of")
    """The input files for the run."""
    # outputs on File
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    run_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_runs")
    """Creator of record, a :class:`~lamindb.User`."""


class Dataset(BaseORM):
    """Datasets: measurements of features.

    Datasets are measurements of features (aka observations of variables).

    1. A feature can be a “high-level” feature, i.e., it has meaning, can label
       a column in a DataFrame, and can be modeled as a Feature or another ORM.
       Examples: gene id, protein id, phenotype name, temperature,
       concentration, treatment label, treatment id, etc.
    2. In other cases, a feature might be a “low-level” feature without semantic
       meaning. Examples: pixels, single letters in sequences, etc.

    LaminDB typically stores datasets as files (`.files`), either as

    1. serialized `DataFrame` or `AnnData` objects (for high-level features)
    2. a set of files of any type (for low-level features, e.g., a folder of
       images or fastqs)

    In simple cases, a single serialized DataFrame or AnnData object (`.file`)
    is enough.

    One might also store a dataset in a SQL table or view, but this is not yet
    supported by LaminDB.
    """

    id = models.CharField(max_length=20, default=base62_20, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, default=None)
    """Name or title of dataset (required)."""
    description = models.TextField(null=True, default=None)
    """A description."""
    hash = models.CharField(max_length=86, db_index=True, null=True, default=None)
    """Hash of dataset content. 86 base64 chars allow to store 64 bytes, 512 bits."""
    feature_sets = models.ManyToManyField("FeatureSet", related_name="datasets")
    """The feature sets measured in this dataset."""
    file = models.ForeignKey("File", on_delete=PROTECT, null=True, unique=True, related_name="datasets")
    """Storage of dataset as a one file."""
    files = models.ManyToManyField("File", related_name="datasets")
    """Storage of dataset as multiple file."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_datasets")
    """Creator of record, a :class:`~lamindb.User`."""


class Feature(BaseORM):
    """Features: column names of DataFrames.

    Note that you can use Bionty ORMs to manage common features like genes,
    pathways, proteins & cell markers.

    Similarly, you can define custom ORMs to manage features like gene sets, nodes, etc.

    This ORM is a way of getting started without using Bionty or a custom schema.
    """

    id = models.CharField(max_length=12, default=base62_12, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, default=None)
    """Name or title of feature (required)."""
    type = models.CharField(max_length=96, null=True, default=None)
    """A way of grouping features of same type."""
    description = models.TextField(null=True, default=None)
    """A description."""
    feature_sets = models.ManyToManyField("FeatureSet", related_name="features")
    """Feature sets linked to this gene."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_features")
    """Creator of record, a :class:`~lamindb.User`."""


class FeatureSet(BaseORM):
    """Feature sets: sets of features.

    A feature set is represented by the hash of the id set for the feature type.

    The current supported feature types are `lnschema_bionty.Gene`,
    `lnschema_bionty.Protein`, and `lnschema_bionty.CellMarker`.

    Guides:

    - :doc:`/biology/scrna`
    - :doc:`/biology/flow`

    Examples:

    >>> import lnschema_bionty as bt
    >>> reference = bt.Gene(species="mouse")
    >>> feature_set = ln.FeatureSet.from_values(adata.var["ensemble_id"], Gene.ensembl_gene_id)
    >>> feature_set.save()
    >>> file = ln.File(adata, name="Mouse Lymph Node scRNA-seq")
    >>> file.save()
    >>> file.featuresets.add(featureset)

    """

    id = models.CharField(max_length=64, primary_key=True, default=None)
    """A universal id, valid across DB instances, a hash of the linked set of features."""
    type = models.CharField(max_length=64)
    """A feature entity type."""
    files = models.ManyToManyField("File", related_name="feature_sets")
    """Files linked to the feature set."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_featuresets")
    """Creator of record, a :class:`~lamindb.User`."""


class File(BaseORM):
    id = models.CharField(max_length=20, primary_key=True)
    """A universal random id (20-char base62), valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """A name or title for the file, mostly useful if no key is provided."""
    key = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Storage key, the relative path within the storage location."""
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
    run = models.ForeignKey(Run, PROTECT, related_name="outputs", null=True)
    """:class:`~lamindb.Run` that created the `file`."""
    transform = models.ForeignKey(Transform, PROTECT, related_name="files", null=True)
    """:class:`~lamindb.Transform` whose run created the `file`."""
    storage: "Storage" = models.ForeignKey(Storage, PROTECT, related_name="files")
    """:class:`~lamindb.Storage` location of `file`, see `.path()` for full path."""
    # tags from Tags.files
    # features from Features.files
    # input_of from Run.inputs
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_files")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("storage", "key"),)
