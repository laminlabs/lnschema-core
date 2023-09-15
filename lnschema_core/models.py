import builtins
from datetime import datetime
from pathlib import Path
from typing import (  # noqa
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    NamedTuple,
    Optional,
    Type,
    Union,
    overload,
)

from django.db import models
from django.db.models import CASCADE, PROTECT
from lamin_utils import logger
from lamindb_setup import _check_instance_setup
from upath import UPath

from lnschema_core.mocks import AnnDataAccessor, BackedAccessor, QuerySet
from lnschema_core.types import (
    AnnDataLike,
    CharField,
    DataLike,
    FieldAttr,
    ListLike,
    PathLike,
    StrField,
    TextField,
)

from .ids import base62_8, base62_12, base62_20
from .types import TransformType
from .users import current_user_id

_INSTANCE_SETUP = _check_instance_setup()

if TYPE_CHECKING or _INSTANCE_SETUP:
    import numpy as np
    import pandas as pd
    from lamin_utils._inspect import InspectResult
    from lamindb.dev import FeatureManager, LabelManager


IPYTHON = getattr(builtins, "__IPYTHON__", False)
TRANSFORM_TYPE_DEFAULT = TransformType.notebook if IPYTHON else TransformType.pipeline


class CanValidate:
    """Base class providing :class:`~lamindb.dev.Registry`-based validation."""

    @classmethod
    def inspect(
        cls,
        values: ListLike,
        field: Optional[Union[str, StrField]] = None,
        *,
        mute: bool = False,
        **kwargs,
    ) -> "InspectResult":
        """Inspect if values are mappable to a field.

        Being mappable means that an exact match exists.

        Args:
            values: Values that will be checked against the
                field.
            field: The field of values. Examples are `'ontology_id'` to map
                against the source ID or `'name'` to map against the ontologies
                field names.
            mute: Mute logging.

        See Also:
            :meth:`~lamindb.dev.CanValidate.validate`

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.settings.species = "human"
            >>> ln.save(lb.Gene.from_values(["A1CF", "A1BG", "BRCA2"], field="symbol"))
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> result = lb.Gene.inspect(gene_symbols, field=lb.Gene.symbol)
            ✅ 2 terms (50.00%) are validated
            🔶 2 terms (50.00%) are not validated
                🟠 detected synonyms
                to increase validated terms, standardize them via .standardize()
            >>> result.validated
            ['A1CF', 'A1BG']
            >>> result.non_validated
            ['FANCD1', 'FANCD20']
        """
        pass

    @classmethod
    def validate(
        cls,
        values: ListLike,
        field: Optional[Union[str, StrField]] = None,
        *,
        mute: bool = False,
        **kwargs,
    ) -> "np.ndarray":
        """Validate values against existing values of a string field.

        Note this is strict validation, only asserts exact matches.

        Args:
            values: Values that will be validated against the field.
            field: The field of values.
                    Examples are `'ontology_id'` to map against the source ID
                    or `'name'` to map against the ontologies field names.
            mute: Mute logging.

        Returns:
            A vector of booleans indicating if an element is validated.

        See Also:
            :meth:`~lamindb.dev.CanValidate.inspect`

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.settings.species = "human"
            >>> ln.save(lb.Gene.from_values(["A1CF", "A1BG", "BRCA2"], field="symbol"))
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> lb.Gene.validate(gene_symbols, field=lb.Gene.symbol)
            ✅ 2 terms (50.00%) are validated
            🔶 2 terms (50.00%) are not validated
            array([ True,  True, False, False])
        """
        pass

    @classmethod
    def standardize(
        cls,
        values: Iterable,
        field: Optional[Union[str, StrField]] = None,
        *,
        return_mapper: bool = False,
        case_sensitive: bool = False,
        mute: bool = False,
        bionty_aware: bool = True,
        keep: Literal["first", "last", False] = "first",
        synonyms_field: str = "synonyms",
        **kwargs,
    ) -> Union[List[str], Dict[str, str]]:
        """Maps input synonyms to standardized names.

        Args:
            values: Synonyms that will be standardized.
            return_mapper: If `True`, returns `{input_synonym1:
                standardized_name1}`.
            case_sensitive: Whether the mapping is case sensitive.
            mute: Mute logging.
            bionty_aware: Whether to standardize from Bionty reference.
            keep: When a synonym maps to
                multiple names, determines which duplicates to mark as
                `pd.DataFrame.duplicated`:

                    - `"first"`: returns the first mapped standardized name
                    - `"last"`: returns the last mapped standardized name
                    - `False`: returns all mapped standardized name
            synonyms_field: A field containing the concatenated synonyms.
            field: The field representing the standardized names.

        Returns:
            If `return_mapper` is `False`: a list of standardized names. Otherwise,
            a dictionary of mapped values with mappable synonyms as keys and
            standardized names as values.

        See Also:
            :meth:`~lamindb.dev.CanValidate.add_synonym`
                Add synonyms
            :meth:`~lamindb.dev.CanValidate.remove_synonym`
                Remove synonyms

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.settings.species = "human"
            >>> ln.save(lb.Gene.from_values(["A1CF", "A1BG", "BRCA2"], field="symbol"))
            >>> gene_synonyms = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> standardized_names = lb.Gene.standardize(gene_synonyms)
            >>> standardized_names
            ['A1CF', 'A1BG', 'BRCA2', 'FANCD20']
        """
        pass

    @classmethod
    def map_synonyms(
        cls,
        synonyms: Iterable,
        *,
        return_mapper: bool = False,
        case_sensitive: bool = False,
        keep: Literal["first", "last", False] = "first",
        synonyms_field: str = "synonyms",
        field: Optional[str] = None,
        **kwargs,
    ) -> Union[List[str], Dict[str, str]]:
        """{}"""
        logger.warning("`map_synonyms()` is deprecated, use `.standardize()`!'")
        return cls.standardize(
            values=synonyms,
            return_mapper=return_mapper,
            case_sensitive=case_sensitive,
            keep=keep,
            synonyms_field=synonyms_field,
            field=field,
            **kwargs,
        )

    def add_synonym(
        self,
        synonym: Union[str, ListLike],
        force: bool = False,
        save: Optional[bool] = None,
    ):
        """Add synonyms to a record.

        Args:
            synonym
            force
            save

        See Also:
            :meth:`~lamindb.dev.CanValidate.remove_synonym`
                Remove synonyms

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.CellType.from_bionty(name="T cell").save()
            >>> lookup = lb.CellType.lookup()
            >>> record = lookup.t_cell
            >>> record.synonyms
            'T-cell|T lymphocyte|T-lymphocyte'
            >>> record.add_synonym("T cells")
            >>> record.synonyms
            'T cells|T-cell|T-lymphocyte|T lymphocyte'
        """
        pass

    def remove_synonym(self, synonym: Union[str, ListLike]):
        """Remove synonyms from a record.

        Args:
            synonym: The synonym value.

        See Also:
            :meth:`~lamindb.dev.CanValidate.add_synonym`
                Add synonyms

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.CellType.from_bionty(name="T cell").save()
            >>> lookup = lb.CellType.lookup()
            >>> record = lookup.t_cell
            >>> record.synonyms
            'T-cell|T lymphocyte|T-lymphocyte'
            >>> record.remove_synonym("T-cell")
            'T lymphocyte|T-lymphocyte'
        """
        pass

    def set_abbr(self, value: str):
        """Set value for abbr field and add to synonyms.

        Args:
            value: A value for an abbreviation.

        See Also:
            :meth:`~lamindb.dev.CanValidate.add_synonym`
                Add synonyms

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.ExperimentalFactor.from_bionty(name="single-cell RNA sequencing").save()
            >>> scrna = lb.ExperimentalFactor.filter(name="single-cell RNA sequencing").one()
            >>> scrna.abbr
            None
            >>> scrna.synonyms
            'single-cell RNA-seq|single-cell transcriptome sequencing|scRNA-seq|single cell RNA sequencing'
            >>> scrna.set_abbr("scRNA")
            >>> scrna.abbr
            'scRNA'
            >>> scrna.synonyms
            'scRNA|single-cell RNA-seq|single cell RNA sequencing|single-cell transcriptome sequencing|scRNA-seq'
            >>> scrna.save()
        """
        pass


class HasParents:
    """Base class for hierarchical methods."""

    def view_parents(
        self,
        field: Optional[StrField] = None,
        with_children: bool = False,
        distance: int = 5,
    ):
        """View parents in a graph.

        Args:
            field: Field to display on graph
            with_children: Also show children.
            distance: Maximum distance still shown.

        There are two types of registries with a `parents` field:

        - Ontological hierarchies: :class:`~lamindb.ULabel` (project & sub-project), :class:`~lnschema_bionty.CellType` (cell type & subtype), ...
        - Procedural/temporal hierarchies: :class:`~lamindb.Transform` (preceding transform & successing transform), ...

        See Also:
            - :doc:`docs:data-flow`
            - :doc:`/tutorial`

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.Tissue.from_bionty(name="subsegmental bronchus").save()
            >>> record = lb.Tissue.filter(name="respiratory tube").one()
            >>> record.view_parents()
            >>> tissue.view_parents(with_children=True)
        """
        pass


class Registry(models.Model):
    """Registry base class.

    Extends ``django.db.models.Model``.

    Why does LaminDB call it `Registry` and not `Model`? The term "Registry" can't lead to
    confusion with statistical, machine learning or biological models.
    """

    @classmethod
    def from_values(cls, values: ListLike, field: Optional[StrField] = None, **kwargs) -> List["Registry"]:
        """Parse values for an identifier (a name, an id, etc.) and load corresponding records.

        Args:
            values: A list of values for an identifier, e.g.
                `["name1", "name2"]`.
            field: A `Registry` field to look up, e.g., `lb.CellMarker.name`.
            **kwargs: Additional conditions for creation of records, e.g., `species="human"`.

        Returns:
            A list of records.

        Notes:
            For more info, see tutorial: :doc:`bio-registries`.

        Examples:

            Bulk create from non-validated values will log warnings & returns empty list:

            >>> ulabels = ln.ULabel.from_values(["benchmark", "prediction", "test"], field="name")
            >>> assert len(ulabels) == 0

            Bulk create records from validated values returns the corresponding existing records:

            >>> ln.save([ln.ULabel(name=name) for name in ["benchmark", "prediction", "test"]])
            >>> ulabels = ln.ULabel.from_values(["benchmark", "prediction", "test"], field="name")
            >>> assert len(ulabels) == 3

            Bulk create records with shared kwargs:

            >>> pipelines = ln.Transform.from_values(["Pipeline 1", "Pipeline 2"], field="name",
            ...                                      type="pipeline", version="1")
            >>> pipelines

            Bulk create records from bionty:

            >>> import lnschema_bionty as lb
            >>> records = lb.CellType.from_values(["T cell", "B cell"], field="name")
            >>> records
        """
        pass

    @classmethod
    def lookup(cls, field: Optional[StrField] = None, return_field: Optional[StrField] = None) -> NamedTuple:
        """Return an auto-complete object for a field.

        Args:
            field: The field to
                look up the values for. Defaults to first string field.

        Returns:
            A `NamedTuple` of lookup information of the field values with a
            dictionary converter.

        See Also:
            :meth:`~lamindb.dev.Registry.search`

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.settings.species = "human"
            >>> lb.Gene.from_bionty(symbol="ADGB-DT").save()
            >>> lookup = lb.Gene.lookup()
            >>> lookup.adgb_dt
            >>> lookup_dict = lookup.dict()
            >>> lookup_dict['ADGB-DT']
        """
        pass

    @classmethod
    def filter(cls, **expressions) -> QuerySet:
        """Query records (see :doc:`meta`).

        Args:
            expressions: Fields and values passed as Django query expressions.

        Returns:
            A :class:`~lamindb.dev.QuerySet`.

        See Also:
            - Guide: :doc:`meta`
            - Django documentation: `Queries <https://docs.djangoproject.com/en/4.2/topics/db/queries/>`__

        Examples:
            >>> ln.ULabel(name="my ulabel").save()
            >>> ulabel = ln.ULabel.filter(name="my ulabel").one()
        """
        from lamindb._filter import filter

        return filter(cls, **expressions)

    @classmethod
    def search(
        cls,
        string: str,
        *,
        field: Optional[StrField] = None,
        limit: Optional[int] = 20,
        return_queryset: bool = False,
        case_sensitive: bool = False,
        synonyms_field: Optional[StrField] = "synonyms",  # type: ignore
    ) -> Union["pd.DataFrame", "QuerySet"]:
        """Search.

        Makes reasonable choices of which fields to search.

        For instance, for :class:`~lamindb.File`, searches `key` and
        `description` fields.

        Args:
            string: The input string to match against the field ontology values.
            field: The field against which the input string is matching.
            limit: Maximum amount of top results to return.
            return_queryset: Return search result as a sorted QuerySet.
            case_sensitive: Whether the match is case sensitive.
            synonyms_field: Search synonyms if column is available. If `None`,
                is ignored.

        Returns:
            A sorted `DataFrame` of search results with a score in column `__ratio__`.
            If `return_queryset` is `True`, an ordered `QuerySet`.

        See Also:
            :meth:`~lamindb.dev.Registry.filter`
            :meth:`~lamindb.dev.Registry.lookup`

        Examples:
            >>> ln.save(ln.ULabel.from_values(["ULabel1", "ULabel2", "ULabel3"], field="name"))
            >>> ln.ULabel.search("ULabel2")
                        id   __ratio__
            name
            ULabel2  o3FY3c5n  100.000000
            ULabel1  CcFPLmpq   75.000000
            ULabel3  Qi3c4utq   75.000000
        """
        pass

    class Meta:
        abstract = True


class Data:
    """Base class for :class:`~lamindb.File` & :class:`~lamindb.Dataset`."""

    @property
    def features(self) -> "FeatureManager":
        """Feature manager (:class:`~lamindb.dev.FeatureManager`)."""
        pass

    @property
    def labels(self) -> "LabelManager":
        """Label manager (:class:`~lamindb.dev.LabelManager`)."""
        pass

    def describe(self):
        """Describe relations of data record.

        Examples:
            >>> ln.File(ln.dev.datasets.file_jpg_paradisi05(), description="paradisi05").save()
            >>> file = ln.File.filter(description="paradisi05").one()
            >>> ln.save(ln.ULabel.from_values(["image", "benchmark", "example"], field="name"))
            >>> ulabels = ln.ULabel.filter(name__in=["image", "benchmark", "example"]).all()
            >>> file.ulabels.set(ulabels)
            >>> file.describe()
        """
        pass


# -------------------------------------------------------------------------------------
# A note on required fields at the Registry level
#
# As Django does most of its validation on the Form-level, it doesn't offer functionality
# for validating the integrity of an Registry object upon instantation (similar to pydantic)
#
# For required fields, we define them as commonly done on the SQL level together
# with a validator in Registry (validate_required_fields)
#
# This goes against the Django convention, but goes with the SQLModel convention
# (Optional fields can be null on the SQL level, non-optional fields cannot)
#
# Due to Django's convention where CharFieldAttr has pre-configured (null=False, default=""), marking
# a required field necessitates passing `default=None`. Without the validator it would trigger
# an error at the SQL-level, with it, it triggers it at instantiation

# -------------------------------------------------------------------------------------
# A note on class and instance methods of core Registry
#
# All of these are defined and tested within lamindb, in files starting with _{orm_name}.py


class User(Registry, CanValidate):
    """Users: humans and bots.

    All data in this registry is synced from the cloud user account to ensure a
    persistent universal user identity, valid across DB instances and email,
    name & handle changes. Hence, no need to manually create records.

    Examples:

        Query a user by handle:

        >>> user = ln.User.filter(handle="testuser1").one()
        >>> user
        User(id=DzTjkKse, handle=testuser1, email=testuser1@lamin.ai, name=Test User1, updated_at=2023-07-10 18:37:26)
    """

    id = CharField(max_length=8, primary_key=True, default=None)
    """Universal id, valid across DB instances."""
    handle = CharField(max_length=30, unique=True, db_index=True, default=None)
    """Universal handle, valid across DB instances (required)."""
    email = CharField(max_length=255, unique=True, db_index=True, default=None)
    """Email address (required)."""
    name = CharField(max_length=255, db_index=True, null=True, default=None)
    """Name (optional)."""  # has to match hub specification, where it's also optional
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""

    @overload
    def __init__(
        self,
        handle: str,
        email: str,
        name: Optional[str],
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(User, self).__init__(*args, **kwargs)


class Storage(Registry):
    """Storage locations: S3/GCP buckets or local directories.

    Is auto-managed, no need to create objects.

    See Also:
        :attr:`~lamindb.dev.Settings.storage`

    Examples:

        Configure the default storage location upon initiation of a LaminDB instance:

        `lamin init --storage ./mydata # or "s3://my-bucket" or "gs://my-bucket"`

        View the default storage location:

        >>> ln.settings.storage
        PosixPath('/home/runner/work/lamindb/lamindb/docs/guide/mydata')

        Set a new default storage (currently doesn't support SQLite instances):

        >>> ln.load("my-postgres-db")
        >>> ln.settings.storage = "./storage_2" # or a cloud bucket
        >>> ln.settings.storage
        PosixPath('/home/runner/work/lamindb-setup/lamindb-setup/docs/guide/storage_2')
    """

    id = CharField(max_length=8, default=base62_8, db_index=True, primary_key=True)
    """Universal id, valid across DB instances."""
    root = CharField(max_length=255, db_index=True, unique=True, default=None)
    """Root path of storage, an s3 path, a local path, etc. (required)."""
    type = CharField(max_length=30, db_index=True)
    """Local vs. s3 vs. gcp etc."""
    region = CharField(max_length=64, db_index=True, null=True, default=None)
    """Cloud storage region, if applicable."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_storages")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        root: str,
        type: str,
        region: Optional[str],
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(Storage, self).__init__(*args, **kwargs)


class Transform(Registry, HasParents):
    """Transforms of files & datasets.

    Pipelines, notebooks, app uploads.

    A pipeline is versioned software that transforms data.
    This can be anything from typical workflow tools (Nextflow, Snakemake,
    Prefect, Apache Airflow, etc.) to simple (versioned) scripts.

    Args:
        name: `str` A name or title.
        short_name: `Optional[str] = None` A short name or abbreviation.
        version: `Optional[str] = None` A version.
        type: `Optional[TransformType] = None` Either `'notebook'`, `'pipeline'`
            or `'app'`. If `None`, defaults to `'notebook'` within an IPython
            environment and to `'pipeline'` outside of it.
        reference: `Optional[str] = None` A reference like a URL.
        is_new_version_of: `Optional[Transform] = None` An old version of the transform.

    See Also:
        :meth:`lamindb.track`
            Track global Transform & Run for a notebook or pipeline.
        :class:`~lamindb.Run`
            Executions of the transform.

    Notes:
        For more info, see tutorial: :doc:`docs:data-flow`.

    Examples:

        Create a transform for a pipeline:

        >>> transform = ln.Transform(name="Cell Ranger", version="7.2.0", type="pipeline")
        >>> transform.save()

        Create a transform from a notebook:

        >>> ln.track()

        View parents of a transform:

        >>> transform.view_parents()
    """

    id = CharField(max_length=14, db_index=True, primary_key=True, default=None)
    """Universal id."""
    name = CharField(max_length=255, db_index=True, null=True, default=None)
    """Transform name or title, a pipeline name, notebook title, etc..
    """
    short_name = CharField(max_length=128, db_index=True, null=True, default=None)
    """A short name (optional)."""
    version = CharField(max_length=10, default=None, null=True, db_index=True)
    """Version (default `None`).

    Use this to label different versions of a transform.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    type = CharField(
        max_length=20,
        choices=TransformType.choices(),
        db_index=True,
        default=TRANSFORM_TYPE_DEFAULT,
    )
    """Transform type.

    Defaults to `notebook` if run from ipython and to `pipeline` if run from python.

    If run from the app, it defaults to `app`.
    """
    reference = CharField(max_length=255, db_index=True, null=True, default=None)
    """Reference for the transform, e.g., a URL.
    """
    reference_type = CharField(max_length=255, db_index=True, null=True, default=None)
    """Type of reference, e.g., github link."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent transforms (predecessors) in data flow.

    These are auto-populated whenever a transform loads a file as run input.
    """
    initial_version = models.ForeignKey("self", PROTECT, null=True, default=None)
    """Initial version of the transform, a :class:`~lamindb.Transform` record."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_transforms")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        name: str,
        short_name: Optional[str] = None,
        version: Optional[str] = None,
        type: Optional[TransformType] = None,
        reference: Optional[str] = None,
        reference_type: Optional[str] = None,
        is_new_version_of: Optional["Transform"] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(Transform, self).__init__(*args, **kwargs)


class Run(Registry):
    """Runs of transforms.

    Args:
        transform: `Transform` A :class:`~lamindb.Transform` record.
        reference: `Optional[str] = None` For instance, an external ID or a download URL.
        reference_type: `Optional[str] = None` For instance, `redun_id`, `nextflow_id` or `url`.

    See Also:
        :meth:`~lamindb.track`
            Track global run & transform records for a notebook or pipeline.

    Notes:
        See guide: :doc:`docs:data-flow`.

        Typically, a run has inputs (`run.inputs`) and outputs (`run.outputs`):

            - References to outputs are also stored in the `run` field of :class:`~lamindb.File` and :class:`~lamindb.Dataset`.
            - References to inputs are also stored in the `input_of` field of :class:`~lamindb.File` and :class:`~lamindb.Dataset`.

    Examples:

        >>> ln.Transform(name="Cell Ranger", version="7.2.0", type="pipeline").save()
        >>> transform = ln.Transform.filter(name="Cell Ranger", version="7.2.0").one()
        >>> run = ln.Run(transform)

        Create a global run context:

        >>> ln.track(transform)
        >>> ln.dev.run_context.run  # global available run

        Track a notebook run:

        >>> ln.track()  # Jupyter notebook metadata is automatically parsed
        >>> ln.dev.context.run
    """

    id = CharField(max_length=20, default=base62_20, primary_key=True)
    """Universal id, valid across DB instances."""
    transform = models.ForeignKey(Transform, CASCADE, related_name="runs")
    """The transform :class:`~lamindb.Transform` that is being run."""
    run_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, CASCADE, default=current_user_id, related_name="created_runs")
    """Creator of record, a :class:`~lamindb.User`."""
    # input_files on File
    # output_files on File
    reference = CharField(max_length=255, db_index=True, null=True, default=None)
    """A reference like a URL or external ID (such as from a workflow manager)."""
    reference_type = CharField(max_length=255, db_index=True, null=True, default=None)
    """Type of reference, e.g., a workflow manager execution ID."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""

    @overload
    def __init__(
        self,
        transform: Transform,
        reference: Optional[str] = None,
        reference_type: Optional[str] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(Run, self).__init__(*args, **kwargs)


class ULabel(Registry, HasParents, CanValidate):
    """Universal label ontology.

    Args:
        name: `str` A name.
        description: `str` A description.

    A `ULabel` record provides the easiest way to annotate a file or dataset
    with a label: `"My project"`, `"curated"`, or `"Batch X"`:

        >>> my_project = ULabel(name="My project")
        >>> my_project.save()
        >>> dataset.ulabels.add(my_project)

    In some cases, a label is measured *within* a file or dataset a feature (a
    :class:`~lamindb.Feature` record) denotes the column name in which the label
    is stored. For instance, the dataset might contain measurements across 2
    species of the Iris flower: `"setosa"` & `"versicolor"`.

    See :doc:`tutorial1` to learn more.

    .. note::

        If you work with complex entities like cell lines, cell types, tissues,
        etc., consider using the pre-defined biological registries in
        :mod:`lnschema_bionty` to label files & datasets.

        If you work with biological samples, likely, the only sustainable way of
        tracking metadata, is to create a custom schema module.

    See Also:
        :meth:`lamindb.Feature`
            Dimensions of measurement for files & datasets.

    Examples:

        Create a new label:

        >>> my_project = ln.ULabel(name="My project")
        >>> my_project.save()

        Label a file without associating it to a feature:

        >>> ulabel = ln.ULabel.filter(name="My project").one()
        >>> file = ln.File("./myfile.csv")
        >>> file.save()
        >>> file.ulabels.add(ulabel)
        >>> file.ulabels.list("name")
        ['My project']

        Organize labels in a hierarchy:

        >>> ulabels = ln.ULabel.lookup()  # create a lookup
        >>> is_project = ln.ULabel(name="is_project")  # create a super-category `is_project`
        >>> is_project.save()
        >>> ulabels.my_project.parents.add(is_project)

        Query by `ULabel`:

        >>> ln.File.filter(ulabels=project).first()
    """

    id = CharField(max_length=8, default=base62_8, primary_key=True)
    """A universal random id, valid across DB instances."""
    name = CharField(max_length=255, db_index=True, unique=True, default=None)
    """Name or title of ulabel (required)."""
    description = TextField(null=True, default=None)
    """A description (optional)."""
    reference = CharField(max_length=255, db_index=True, null=True, default=None)
    """A reference like URL or external ID."""
    reference_type = CharField(max_length=255, db_index=True, null=True, default=None)
    """Type of reference, e.g., donor_id from Vendor X."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent labels, useful to hierarchically group labels (optional)."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_ulabels")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        reference: Optional[str] = None,
        reference_type: Optional[str] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass


class Modality(Registry, HasParents, CanValidate):
    """Measurement types of features.

    .. note::

        This will soon borrow readout-related records from the experimental factor
        ontology, see :class:`~lnschema_bionty.ExperimentalFactor`.

    Args:
        name: `str` A name.
        ontology_id: `Optional[str]` A public ontology ID.
        abbr: `Optional[str]` An abbreviation.
        description: `Optional[str]` A description.
    """

    id = CharField(max_length=8, default=base62_8, primary_key=True)
    """Universal id, valid across DB instances."""
    name = CharField(max_length=256, db_index=True)
    """Name of the modality (required)."""
    ontology_id = CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the modality."""
    abbr = CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation for the modality (optional)."""
    synonyms = TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this modality."""
    description = TextField(null=True, default=None)
    """Description."""
    molecule = TextField(null=True, default=None, db_index=True)
    """Molecular experimental factor, parsed from EFO."""
    instrument = TextField(null=True, default=None, db_index=True)
    """Instrument used to measure, parsed from EFO."""
    measurement = TextField(null=True, default=None, db_index=True)
    """Phenotypic experimental factor, parsed from EFO."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parents."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_modalities",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str,
        abbr: Optional[str],
        description: Optional[str],
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(Modality, self).__init__(*args, **kwargs)


class Feature(Registry, CanValidate):
    """Dimensions of measurement.

    See Also:
        :meth:`~lamindb.Feature.from_df`
            Create feature records from DataFrame.
        :attr:`~lamindb.dev.Data.features`
            Manage feature annotations of files & datasets.
        :meth:`lamindb.ULabel`
            ULabels for files & datasets.

    Args:
        name: `str` Name of the feature, typically, a column name.
        type: `str` Simple type (`"number"`, `"category"`, `"str"`, `"datetime"`).
        unit: `Optional[str] = None` Unit of measure, ideally SI (`"m"`, `"s"`, `"kg"`, etc.) or `"normalized"` etc.
        description: `Optional[str] = None` A description.
        synonyms: `Optional[str] = None` Bar-separated synonyms.

    .. note::

        *Features* and *labels* denote two ways for using entities to organize data:

        1. A feature qualifies *which entity* is measured (e.g., is a vector of categories)
        2. A label *is* a measured value of an entity (a category)

        If re-shaping data introduced ambiguity, ask yourself what the joint measurement was:
        a feature qualifies variables in a joint measurement.
        You might be looking at a label if data was re-shaped from there.

    Notes:

        For more control, you can use :mod:`lnschema_bionty` ORMs to manage
        common basic biological entities like genes, proteins & cell markers
        involved in expression/count measurements.

        Similarly, you can define custom ORMs to manage high-level derived
        features like gene sets, malignancy, etc.

    Examples:

        >>> df = pd.DataFrame({"feat1": [1, 2], "feat2": [3.1, 4.2], "feat3": ["cond1", "cond2"]})
        >>> features = ln.Feature.from_df(df)
        >>> features.save()
        >>> # the information from the DataFrame is now available in the Feature table
        >>> ln.Feature.filter().df()
        id    name    type
         a   feat1     int
         b   feat2   float
         c   feat3     str

    """

    id = CharField(max_length=12, default=base62_12, primary_key=True)
    """Universal id, valid across DB instances."""
    name = CharField(max_length=255, db_index=True, default=None)
    """Name of feature (required)."""
    type = CharField(max_length=64, db_index=True, default=None)
    """Simple type ("float", "int", "str", "category").

    If "category", consider managing categories with :class:`~lamindb.ULabel` or
    another Registry for managing labels.
    """
    modality = models.ForeignKey(Modality, PROTECT, null=True, default=None, related_name="features")
    """The measurement modality, e.g., "RNA", "Protein", "Gene Module", "pathway" (:class:`~lamindb.Modality`)."""
    unit = CharField(max_length=30, db_index=True, null=True, default=None)
    """Unit of measure, ideally SI (`m`, `s`, `kg`, etc.) or 'normalized' etc. (optional)."""
    description = TextField(db_index=True, null=True, default=None)
    """A description."""
    registries = CharField(max_length=128, db_index=True, default=None, null=True)
    """Registries that provide values for labels, bar-separated (|) (optional)."""
    synonyms = TextField(null=True, default=None)
    """Bar-separated (|) synonyms (optional)."""
    feature_sets = models.ManyToManyField("FeatureSet", related_name="features")
    """Feature sets linked to this feature."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_features")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        name: str,
        type: str,
        unit: Optional[str],
        description: Optional[str],
        synonyms: Optional[str],
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    @classmethod
    def from_df(cls, df: "pd.DataFrame") -> List["Feature"]:
        """Create Feature records for columns."""
        pass

    def save(self, *args, **kwargs) -> None:
        """Save."""
        pass


class FeatureSet(Registry):
    """Jointly measured sets of features.

    See Also:
        :meth:`~lamindb.FeatureSet.from_values`
            Create from values.
        :meth:`~lamindb.FeatureSet.from_df`
            Create from dataframe columns.
        :class:`~lamindb.Modality`
            Type of measurement.

    Note:

        Feature sets are useful as you might have millions of data batches
        that measure the same features: all of them link against the same
        feature set. If instead, you'd link against single features (say, genes),
        you'd face exploding link tables.

        A `feature_set` is identified by the hash of feature values.

    Args:
        features: `Iterable[Registry]` An iterable of :class:`~lamindb.Feature`
            records to hash, e.g., `[Feature(...), Feature(...)]`. Is turned into
            a set upon instantiation. If you'd like to pass values, use
            :meth:`~lamindb.FeatureSet.from_values` or
            :meth:`~lamindb.FeatureSet.from_df`.
        type: `Optional[Union[Type, str]] = None` The simple type. Defaults to
            `None` if reference Registry is :class:`~lamindb.Feature`, defaults to
            `"float"` otherwise.
        modality: `Optional[str] = None` A name or id for :class:`~lamindb.Modality`.
        name: `Optional[str] = None` A name.

    Examples:

        >>> df = pd.DataFrame({"feat1": [1, 2], "feat2": [3.1, 4.2], "feat3": ["cond1", "cond2"]})
        >>> feature_set = ln.FeatureSet.from_df(df)

        >>> features = ln.Feature.from_values(["feat1", "feat2"], type=float)
        >>> ln.FeatureSet(features)

        >>> import lnschema_bionty as bt
        >>> reference = bt.Gene(species="mouse")
        >>> feature_set = ln.FeatureSet.from_values(adata.var["ensemble_id"], Gene.ensembl_gene_id)
        >>> feature_set.save()
        >>> file = ln.File(adata, name="Mouse Lymph Node scRNA-seq")
        >>> file.save()
        >>> file.features.add_feature_st(feature_set, slot="var")
    """

    id = CharField(max_length=20, primary_key=True, default=None)
    """A universal id (hash of the set of feature values)."""
    name = CharField(max_length=128, null=True, default=None)
    """A name (optional)."""
    n = models.IntegerField()
    """Number of features in the set."""
    type = CharField(max_length=64, null=True, default=None)
    """Simple type, e.g., "str", "int". Is `None` for :class:`~lamindb.Feature` (optional).

    For :class:`~lamindb.Feature`, types are expected to be in-homogeneous and defined on a per-feature level.
    """
    modality = models.ForeignKey(Modality, PROTECT, null=True, default=None, related_name="feature_sets")
    """The measurement modality, e.g., "RNA", "Protein", "Gene Module", "pathway" (:class:`~lamindb.Modality`)."""
    registry = CharField(max_length=128, db_index=True)
    """The registry that stores & validated the feature identifiers, e.g., `'core.Feature'` or `'bionty.Gene'`."""
    hash = CharField(max_length=20, default=None, db_index=True, null=True)
    """The hash of the set."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_feature_sets")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        features: Iterable[Registry],
        type: Optional[Union[Type, str]] = None,
        modality: Optional[str] = None,
        name: Optional[str] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    @classmethod
    def from_values(  # type: ignore
        cls,
        values: ListLike,
        field: FieldAttr = Feature.name,
        type: Optional[Union[Type, str]] = None,
        name: Optional[str] = None,
        modality: Optional[Modality] = None,
        **kwargs,
    ) -> Optional["FeatureSet"]:
        """Create feature set for validated features.

        Args:
            values: A list of values, like feature names or ids.
            field: The field of a reference Registry to
                map values.
            type: The simple type. Defaults to
                `None` if reference registry is :class:`~lamindb.Feature`, defaults to
                `"float"` otherwise.
            name: A name.
            modality: A name or id for :class:`~lamindb.Modality`.
            **kwargs: Can contain ``species`` or other context to interpret values.

        Examples:

            >>> features = ["feat1", "feat2"]
            >>> feature_set = ln.FeatureSet.from_values(features)

            >>> genes = ["ENS980983409", "ENS980983410"]
            >>> feature_set = ln.FeatureSet.from_values(features, lb.Gene.ensembl_gene_id, float)
        """
        pass

    @classmethod
    def from_df(
        cls,
        df: "pd.DataFrame",
        field: FieldAttr = Feature.name,
        name: Optional[str] = None,
        modality: Optional[Modality] = None,
    ) -> Optional["FeatureSet"]:
        """Create feature set for validated features."""
        pass

    def save(self, *args, **kwargs) -> None:
        """Save."""
        pass


class File(Registry, Data):
    """Files: immutable data batches.

    Args:
        data: `Union[PathLike, DataLike]` A path or data
            object (`DataFrame`, `AnnData`).
        key: `Optional[str] = None` A relative path within default storage,
            e.g., `"myfolder/myfile.fcs"`.
        description: `Optional[str] = None` A description.
        version: `Optional[str] = None` A version string.
        is_new_version_of: `Optional[File] = None` An old version of the file.
        run: `Optional[Run] = None` The run that creates the file.

    .. dropdown:: Typical storage formats & their API accessors

        Listed are typical values for the `suffix` & `accessor` fields.

        - Table: `.csv`, `.tsv`, `.parquet`, `.ipc` ⟷ `DataFrame`, `pyarrow.Table`
        - Annotated matrix: `.h5ad`, `.h5mu`, `.zrad` ⟷ `AnnData`, `MuData`
        - Image: `.jpg`, `.png` ⟷ `np.ndarray`, ...
        - Arrays: HDF5 group, zarr group, TileDB store ⟷ HDF5, zarr, TileDB loaders
        - Fastq: `.fastq` ⟷ /
        - VCF: `.vcf` ⟷ /
        - QC: `.html` ⟷ /

        LaminDB makes some default choices (e.g., serialize a `DataFrame` as a
        `.parquet` file).

    See Also:
        :class:`~lamindb.Dataset`
            Mutable collections of data batches.
        :meth:`~lamindb.File.from_df`
            Create a file object from `DataFrame` and track features.
        :meth:`~lamindb.File.from_anndata`
            Create a file object from `AnnData` and track features.
        :meth:`~lamindb.File.from_dir`
            Bulk create file objects from a directory.

    Notes:
        For more info, see tutorial: :doc:`/tutorial`.

    Examples:

        Create a file from a cloud storage (supports `s3://` and `gs://`):

        >>> file = ln.File("s3://lamindb-ci/test-data/test.csv")
        >>> file.save()  # only metadata is saved

        Create a file from a local temporary filepath using `key`:

        >>> temporary_filepath = ln.dev.datasets.file_jpg_paradisi05()
        >>> file = ln.File(temporary_filepath, key="images/paradisi05_image.jpg")
        >>> file.save()

        .. dropdown:: Why does the API look this way?

            It's inspired by APIs building on AWS S3.

            Both boto3 and quilt select a bucket (akin to default storage in LaminDB) and define a target path through a `key` argument.

            In `boto3 <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/upload_file.html>`__::

                # signature: S3.Bucket.upload_file(filepath, key)
                import boto3
                s3 = boto3.resource('s3')
                bucket = s3.Bucket('mybucket')
                bucket.upload_file('/tmp/hello.txt', 'hello.txt')

            In `quilt3 <https://docs.quiltdata.com/api-reference/bucket>`__::

                # signature: quilt3.Bucket.put_file(key, filepath)
                import quilt3
                bucket = quilt3.Bucket('mybucket')
                bucket.put_file('hello.txt', '/tmp/hello.txt')


        Make a new version of a file:

        >>> # a non-versioned file
        >>> file = ln.File(df1, description="My dataframe")
        >>> file.save()
        >>> # create new file from old file and version both
        >>> new_file = ln.File(df2, is_new_version_of=file)
        >>> assert new_file.initial_version == file.initial_version
        >>> assert file.version == "1"
        >>> assert new_file.version == "2"

    """

    id = CharField(max_length=20, primary_key=True)
    """A universal random id (20-char base62 ~ UUID), valid across DB instances."""
    storage = models.ForeignKey(Storage, PROTECT, related_name="files")
    """Storage location (:class:`~lamindb.Storage`), e.g., an S3 or GCP bucket or a local directory."""
    key = CharField(max_length=255, db_index=True, null=True, default=None)
    """Storage key, the relative path within the storage location."""
    suffix = CharField(max_length=30, db_index=True, default=None)
    # Initially, we thought about having this be nullable to indicate folders
    # But, for instance, .zarr is stored in a folder that ends with a .zarr suffix
    """Path suffix or empty string if no canonical suffix exists.

    This is either a file suffix (`".csv"`, `".h5ad"`, etc.) or the empty string "".
    """
    accessor = CharField(max_length=64, db_index=True, null=True, default=None)
    """Default backed or memory accessor, e.g., DataFrame, AnnData.

    Soon, also: SOMA, MuData, zarr.Group, tiledb.Array, etc.
    """
    description = CharField(max_length=255, db_index=True, null=True, default=None)
    """A description."""
    version = CharField(max_length=10, null=True, default=None, db_index=True)
    """Version (default `None`).

    Use this together with `initial_version` to label different versions of a file.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    size = models.BigIntegerField(null=True, db_index=True)
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    hash = CharField(max_length=86, db_index=True, null=True, default=None)  # 86 base64 chars allow to store 64 bytes, 512 bits
    """Hash or pseudo-hash of file content.

    Useful to ascertain integrity and avoid duplication.
    """
    hash_type = CharField(max_length=30, db_index=True, null=True, default=None)
    """Type of hash."""
    feature_sets = models.ManyToManyField(FeatureSet, related_name="files", through="FileFeatureSet")
    """The feature sets measured in the file (:class:`~lamindb.FeatureSet`)."""
    ulabels = models.ManyToManyField(ULabel, through="FileULabel", related_name="files")
    """The ulabels measured in the file (:class:`~lamindb.ULabel`)."""
    transform = models.ForeignKey(Transform, PROTECT, related_name="files", null=True, default=None)
    """:class:`~lamindb.Transform` whose run created the file."""
    run = models.ForeignKey(Run, PROTECT, related_name="output_files", null=True, default=None)
    """:class:`~lamindb.Run` that created the file."""
    input_of = models.ManyToManyField(Run, related_name="input_files")
    """Runs that use this file as an input."""
    initial_version = models.ForeignKey("self", PROTECT, null=True, default=None)
    """Initial version of the file, a :class:`~lamindb.File` object."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_files")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("storage", "key"),)

    @overload
    def __init__(
        self,
        data: Union[PathLike, DataLike],
        key: Optional[str] = None,
        description: Optional[str] = None,
        is_new_version_of: Optional["File"] = None,
        run: Optional[Run] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    @property
    def path(self) -> Union[Path, UPath]:
        """File path (`Path`, `UPath`).

        Examples:

            File in cloud storage:

            >>> ln.File("s3://lamindb-ci/lndb-storage/pbmc68k.h5ad").save()
            >>> file = ln.File.filter(key="lndb-storage/pbmc68k.h5ad").one()
            >>> file.path
            S3Path('s3://lamindb-ci/lndb-storage/pbmc68k.h5ad')

            File in local storage:

            >>> ln.File("./myfile.csv", description="myfile").save()
            >>> file = ln.File.filter(description="myfile").one()
            >>> file.path
            PosixPath('/home/runner/work/lamindb/lamindb/docs/guide/mydata/myfile.csv')
        """
        pass

    @classmethod
    def from_df(
        cls,
        df: "pd.DataFrame",
        field: FieldAttr = Feature.name,
        key: Optional[str] = None,
        description: Optional[str] = None,
        run: Optional[Run] = None,
        modality: Optional[Modality] = None,
    ) -> "File":
        """Create from ``DataFrame``, validate & link features.

        See Also:
            :meth:`lamindb.Dataset`
                Track datasets.
            :class:`lamindb.Feature`
                Track features.

        Notes:
            For more info, see tutorial: :doc:`/tutorial`.

        Examples:
            >>> df = ln.dev.datasets.df_iris_in_meter_batch1()
            >>> df.head()
              sepal_length sepal_width petal_length petal_width iris_species_code
            0        0.051       0.035        0.014       0.002                 0
            1        0.049       0.030        0.014       0.002                 0
            2        0.047       0.032        0.013       0.002                 0
            3        0.046       0.031        0.015       0.002                 0
            4        0.050       0.036        0.014       0.002                 0
            >>> file = ln.File.from_df(df, description="Iris flower dataset batch1")
            >>> file.save()
        """
        pass

    @classmethod
    def from_anndata(
        cls,
        adata: "AnnDataLike",
        field: Optional[FieldAttr],
        key: Optional[str] = None,
        description: Optional[str] = None,
        run: Optional[Run] = None,
        modality: Optional[Modality] = None,
    ) -> "File":
        """Create from ``AnnDataLike``, validate & link features.

        See Also:

            :meth:`lamindb.Dataset`
                Track datasets.
            :class:`lamindb.Feature`
                Track features.

        Notes:

            For more info, see tutorial: :doc:`/tutorial`.

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.settings.species = "human"
            >>> adata = ln.dev.datasets.anndata_with_obs()
            >>> adata.var_names[:2]
            Index(['ENSG00000000003', 'ENSG00000000005'], dtype='object')
            >>> file = ln.File.from_anndata(adata,
            ...                             field=lb.Gene.ensembl_gene_id,
            ...                             description="mini anndata with obs")
            >>> file.save()
        """
        pass

    @classmethod
    def from_dir(
        cls,
        path: PathLike,
        key: Optional[str] = None,
        *,
        run: Optional[Run] = None,
    ) -> List["File"]:
        """Create a list of file objects from a directory.

        Args:
            path: Source path of folder.
            key: Key for storage destination. If `None` and
                directory is in a registered location, an inferred `key` will
                reflect the relative position. If `None` and directory is outside
                of a registered storage location, the inferred key defaults to `path.name`.
            run: A `Run` object.

        Examples:
            >>> dir_path = ln.dev.datasets.generate_cell_ranger_files("sample_001", ln.settings.storage)
            >>> files = ln.File.from_dir(dir_path)
            >>> ln.save(files)
        """
        pass

    def replace(
        self,
        data: Union[PathLike, DataLike],
        run: Optional[Run] = None,
        format: Optional[str] = None,
    ) -> None:
        """Replace file content.

        Args:
            data: A file path or an in-memory data
                object (`DataFrame`, `AnnData`).
            run: The run that created the file gets
                auto-linked if ``ln.track()`` was called.

        Examples:

            Say we made a change to the content of a file (e.g., edited the image
            `paradisi05_laminopathic_nuclei.jpg`).

            This is how we replace the old file in storage with the new file:

            >>> file.replace("paradisi05_laminopathic_nuclei.jpg")
            >>> file.save()

            Note that this neither changes the storage key nor the filename.

            However, it will update the suffix if the file type changes.
        """
        pass

    def backed(self, is_run_input: Optional[bool] = None) -> Union["AnnDataAccessor", "BackedAccessor"]:
        """Return a cloud-backed data object.

        Notes:
            For more info, see tutorial: :doc:`/data`.

        Examples:

            Read AnnData in backed mode from cloud:

            >>> file = ln.File.filter(key="lndb-storage/pbmc68k.h5ad").one()
            >>> file.backed()
            AnnData object with n_obs × n_vars = 70 × 765 backed at 's3://lamindb-ci/lndb-storage/pbmc68k.h5ad'
        """
        pass

    @classmethod
    def view_tree(
        cls,
        path: Optional[PathLike] = None,
        *,
        level: int = -1,
        limit_to_directories: bool = False,
        length_limit: int = 1000,
    ) -> None:
        """Print a visual tree structure of files & directories.

        Examples:
            >>> dir_path = ln.dev.datasets.generate_cell_ranger_files("sample_001", ln.settings.storage)
            >>> dir_path.name
            'sample_001'
            >>> ln.File.view_tree(dir_path)
            3 subdirectories, 15 files
            sample_001
            ├── web_summary.html
            ├── metrics_summary.csv
            ├── molecule_info.h5
            ├── filtered_feature_bc_matrix
            │   ├── features.tsv.gz
            │   ├── barcodes.tsv.gz
            │   └── matrix.mtx.gz
            ├── analysis
            │   └── analysis.csv
            ├── raw_feature_bc_matrix
            │   ├── features.tsv.gz
            │   ├── barcodes.tsv.gz
            │   └── matrix.mtx.gz
            ├── possorted_genome_bam.bam.bai
            ├── cloupe.cloupe
            ├── possorted_genome_bam.bam
            ├── filtered_feature_bc_matrix.h5
            └── raw_feature_bc_matrix.h5
        """
        pass

    def load(self, is_run_input: Optional[bool] = None, stream: bool = False, **kwargs) -> DataLike:
        """Stage and load to memory.

        Returns in-memory representation if possible, e.g., an `AnnData` object for an `h5ad` file.

        Examples:

            Load as a `DataFrame`:

            >>> df = ln.dev.datasets.df_iris_in_meter_batch1()
            >>> ln.File.from_df(df, description="iris").save()
            >>> file = ln.File.filter(description="iris").one()
            >>> file.load().head()
            sepal_length sepal_width petal_length petal_width iris_species_code
            0        0.051       0.035        0.014       0.002                 0
            1        0.049       0.030        0.014       0.002                 0
            2        0.047       0.032        0.013       0.002                 0
            3        0.046       0.031        0.015       0.002                 0
            4        0.050       0.036        0.014       0.002                 0

            Load as an `AnnData`:

            >>> ln.File("s3://lamindb-ci/lndb-storage/pbmc68k.h5ad").save()
            >>> file = ln.File.filter(key="lndb-storage/pbmc68k.h5ad").one()
            >>> file.load()
            AnnData object with n_obs × n_vars = 70 × 765

            Fall back to :meth:`~lamindb.File.stage` if no in-memory representation is configured:

            >>> ln.File(ln.dev.datasets.file_jpg_paradisi05(), description="paradisi05").save()
            >>> file = ln.File.filter(description="paradisi05").one()
            >>> file.load()
            PosixPath('/home/runner/work/lamindb/lamindb/docs/guide/mydata/.lamindb/jb7BY5UJoQVGMUOKiLcn.jpg')
        """
        pass

    def stage(self, is_run_input: Optional[bool] = None) -> Path:
        """Update cache from cloud storage if outdated.

        Returns a path to a locally cached on-disk object (say, a `.jpg` file).

        Examples:

            Sync file from cloud and return the local path of the cache:

            >>> ln.settings.storage = "s3://lamindb-ci"
            >>> ln.File("s3://lamindb-ci/lndb-storage/pbmc68k.h5ad").save()
            >>> file = ln.File.filter(key="lndb-storage/pbmc68k.h5ad").one()
            >>> file.stage()
            PosixPath('/home/runner/work/Caches/lamindb/lamindb-ci/lndb-storage/pbmc68k.h5ad')
        """
        pass

    def delete(self, storage: Optional[bool] = None) -> None:
        """Delete file, optionally from storage.

        Args:
            storage: Indicate whether you want to delete the
                file in storage.

        Examples:

            For any `File` object `file`, call:

            >>> file.delete()
        """
        pass

    def save(self, *args, **kwargs) -> None:
        """Save the file to database & storage.

        Examples:
            >>> file = ln.File("./myfile.csv", key="myfile.csv")
            >>> file.save()
        """
        pass


class Dataset(Registry, Data):
    """Datasets: mutable collections of data batches.

    Args:
        data: `DataLike` A data object (`DataFrame`, `AnnData`) to store.
        name: `str` A name.
        description: `Optional[str] = None` A description.
        version: `Optional[str] = None` A version string.
        is_new_version_of: `Optional[Dataset] = None` An old version of the dataset.
        run: `Optional[Run] = None` The run that creates the dataset.

    See Also:
        :class:`~lamindb.File`

    Notes:
        See tutorial: :doc:`/tutorial`.

        The `File` & `Dataset` registries both

        - track data batches of arbitrary format & size

        - can validate & link features (the measured dimensions in a data batch)

        Typically,

        - a file stores a single immutable batch of data

        - a dataset stores a mutable collection of data batches

        Examples:

        - Blob-like immutable files (pdf, txt, csv, jpg, ...) or arrays (h5,
          h5ad, ...) → :class:`~lamindb.File`

        - Mutable streamable backends (DuckDB, zarr, TileDB, ...) →
          :class:`~lamindb.Dataset` wrapping :class:`~lamindb.File`

        - Collections of files → :class:`~lamindb.Dataset` wrapping
          :class:`~lamindb.File`

        - Datasets in BigQuery, Snowflake, Postgres, ... →
          :class:`~lamindb.Dataset` (not yet implemented)

        Hence, while

        - files *always* have a one-to-one correspondence with a storage accessor

        - datasets *can* reference a single file, multiple files or a dataset in
          a warehouse like BigQuery or Snowflake

    Examples:

        Create a dataset from a DataFrame:

        >>> df = ln.dev.datasets.df_iris_in_meter_batch1()
        >>> df.head()
          sepal_length sepal_width petal_length petal_width iris_species_code
        0        0.051       0.035        0.014       0.002                 0
        1        0.049       0.030        0.014       0.002                 0
        2        0.047       0.032        0.013       0.002                 0
        3        0.046       0.031        0.015       0.002                 0
        4        0.050       0.036        0.014       0.002                 0
        >>> dataset = ln.Dataset(df, name="Iris flower dataset batch1")
        >>> dataset.save()

        Create a dataset from a collection of :class:`~lamindb.File` objects:

        >>> dataset = ln.Dataset([file1, file2], name="My dataset")
        >>> dataset.save()

        Make a new version of a dataset:

        >>> # a non-versioned dataset
        >>> dataset = ln.Dataset(df1, description="My dataframe")
        >>> dataset.save()
        >>> # create new dataset from old dataset and version both
        >>> new_dataset = ln.File(df2, is_new_version_of=dataset)
        >>> assert new_dataset.initial_version == dataset.initial_version
        >>> assert dataset.version == "1"
        >>> assert new_dataset.version == "2"
    """

    id = CharField(max_length=20, default=base62_20, primary_key=True)
    """Universal id, valid across DB instances."""
    name = CharField(max_length=255, db_index=True, default=None)
    """Name or title of dataset (required)."""
    description = TextField(null=True, default=None)
    """A description."""
    version = CharField(max_length=10, null=True, default=None, db_index=True)
    """Version (default `None`).

    Use this together with `initial_version` to label different versions of a dataset.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    hash = CharField(max_length=86, db_index=True, null=True, default=None)
    """Hash of dataset content. 86 base64 chars allow to store 64 bytes, 512 bits."""
    reference = CharField(max_length=255, db_index=True, null=True, default=None)
    """A reference like URL or external ID."""
    reference_type = CharField(max_length=255, db_index=True, null=True, default=None)
    """Type of reference, e.g., cellxgene Census dataset_id."""
    feature_sets = models.ManyToManyField("FeatureSet", related_name="datasets", through="DatasetFeatureSet")
    """The feature sets measured in this dataset (see :class:`~lamindb.FeatureSet`)."""
    ulabels = models.ManyToManyField("ULabel", through="DatasetULabel", related_name="datasets")
    """ULabels sampled in the dataset (see :class:`~lamindb.Feature`)."""
    transform = models.ForeignKey(Transform, PROTECT, related_name="datasets", null=True, default=None)
    """:class:`~lamindb.Transform` whose run created the dataset."""
    run = models.ForeignKey(Run, PROTECT, related_name="output_datasets", null=True, default=None)
    """:class:`~lamindb.Run` that created the `file`."""
    input_of = models.ManyToManyField(Run, related_name="input_datasets")
    """Runs that use this dataset as an input."""
    file = models.ForeignKey("File", on_delete=PROTECT, null=True, unique=True, related_name="datasets")
    """Storage of dataset as a one file."""
    files = models.ManyToManyField("File", related_name="datasets")
    """Storage of dataset as multiple file."""
    initial_version = models.ForeignKey("self", PROTECT, null=True, default=None)
    """Initial version of the dataset, a :class:`~lamindb.Dataset` object."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_datasets")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        data: Any,
        name: str,
        description: Optional[str] = None,
        reference: Optional[str] = None,
        reference_type: Optional[str] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    @classmethod
    def from_df(
        cls,
        df: "pd.DataFrame",
        field: FieldAttr = Feature.name,
        name: Optional[str] = None,
        description: Optional[str] = None,
        run: Optional[Run] = None,
        modality: Optional[Modality] = None,
        reference: Optional[str] = None,
        reference_type: Optional[str] = None,
    ) -> "Dataset":
        """Create from ``DataFrame``, validate & link features.

        See Also:
            :class:`~lamindb.File`
                Track files.
            :class:`~lamindb.Feature`
                Track features.

        Notes:
            For more info, see tutorial: :doc:`/tutorial`.

        Examples:
            >>> df = ln.dev.datasets.df_iris_in_meter_batch1()
            >>> df.head()
              sepal_length sepal_width petal_length petal_width iris_species_code
            0        0.051       0.035        0.014       0.002                 0
            1        0.049       0.030        0.014       0.002                 0
            2        0.047       0.032        0.013       0.002                 0
            3        0.046       0.031        0.015       0.002                 0
            4        0.050       0.036        0.014       0.002                 0
            >>> dataset = ln.Dataset.from_df(df, description="Iris flower dataset batch1")
        """
        pass

    @classmethod
    def from_anndata(
        cls,
        adata: "AnnDataLike",
        field: Optional[FieldAttr],
        name: Optional[str] = None,
        description: Optional[str] = None,
        run: Optional[Run] = None,
        modality: Optional[Modality] = None,
        reference: Optional[str] = None,
        reference_type: Optional[str] = None,
    ) -> "Dataset":
        """Create from ``AnnDataLike``, validate & link features.

        See Also:

            :class:`~lamindb.File`
                Track files.
            :class:`~lamindb.Feature`
                Track features.

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.settings.species = "human"
            >>> adata = ln.dev.datasets.anndata_with_obs()
            >>> adata.var_names[:2]
            Index(['ENSG00000000003', 'ENSG00000000005'], dtype='object')
            >>> dataset = ln.Dataset.from_anndata(adata, name="My dataset", field=lb.Gene.ensembl_gene_id)
            >>> dataset.save()
        """
        pass


class LinkORM:
    pass


class FileFeatureSet(Registry, LinkORM):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    feature_set = models.ForeignKey(FeatureSet, on_delete=models.CASCADE)
    slot = CharField(max_length=40, null=True, default=None)

    class Meta:
        unique_together = ("file", "feature_set")


class DatasetFeatureSet(Registry, LinkORM):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    feature_set = models.ForeignKey(FeatureSet, on_delete=models.CASCADE)
    slot = CharField(max_length=50, null=True, default=None)

    class Meta:
        unique_together = ("dataset", "feature_set")


class FileULabel(Registry, LinkORM):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    ulabel = models.ForeignKey(ULabel, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, CASCADE, null=True, default=None)

    class Meta:
        unique_together = ("file", "ulabel")


class DatasetULabel(Registry, LinkORM):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    ulabel = models.ForeignKey(ULabel, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, CASCADE, null=True, default=None)

    class Meta:
        unique_together = ("dataset", "ulabel")


# -------------------------------------------------------------------------------------
# Low-level logic needed in lamindb-setup

# Below is needed within lnschema-core because lamindb-setup already performs
# some logging


def format_field_value(value: Union[datetime, str, Any]) -> Any:
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return value


def __repr__(self: Registry, include_foreign_keys: bool = True) -> str:
    field_names = [field.name for field in self._meta.fields if (not isinstance(field, models.ForeignKey) and field.name != "created_at")]
    if include_foreign_keys:
        field_names += [f"{field.name}_id" for field in self._meta.fields if isinstance(field, models.ForeignKey)]
    fields_str = {k: format_field_value(getattr(self, k)) for k in field_names if hasattr(self, k)}
    fields_joined_str = ", ".join([f"{k}={fields_str[k]}" for k in fields_str if fields_str[k] is not None])
    return f"{self.__class__.__name__}({fields_joined_str})"


Registry.__repr__ = __repr__  # type: ignore
Registry.__str__ = __repr__  # type: ignore

# backward compat
ORM = Registry


def deferred_attribute__repr__(self):
    return f"FieldAttr({self.field.model.__name__}.{self.field.name})"


FieldAttr.__repr__ = deferred_attribute__repr__  # type: ignore
