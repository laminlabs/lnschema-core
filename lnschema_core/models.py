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
    Union,
    overload,
)

from django.db import models
from django.db.models import CASCADE, PROTECT
from django.db.models.query_utils import DeferredAttribute as Field
from upath import UPath

from lnschema_core.mocks import AnnDataAccessor, BackedAccessor, QuerySet
from lnschema_core.types import AnnDataLike, DataLike, ListLike, PathLike, StrField

from .ids import base62_8, base62_12, base62_20
from .types import TransformType
from .users import current_user_id

if TYPE_CHECKING:
    import pandas as pd

IPYTHON = getattr(builtins, "__IPYTHON__", False)
TRANSFORM_TYPE_DEFAULT = TransformType.notebook if IPYTHON else TransformType.pipeline


class ORM(models.Model):
    """LaminDB's base ORM.

    Is based on `django.db.models.Model`.

    Why does LaminDB call it `ORM` and not `Model`? The term "ORM" can't lead to
    confusion with statistical, machine learning or biological models.
    """

    def add_synonym(
        self,
        synonym: Union[str, ListLike],
        force: bool = False,
        save: Optional[bool] = None,
    ):
        """Add synonyms to a record.

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

    def describe(self):
        """Rich representation of a record with relationships.

        Examples:
            >>> ln.File(ln.dev.datasets.file_jpg_paradisi05(), description="paradisi05").save()
            >>> file = ln.File.select(description="paradisi05").one()
            >>> ln.save(ln.Tag.from_values(["image", "benchmark", "example"], field="name"))
            >>> tags = ln.Tag.select(name__in = ["image", "benchmark", "example"]).all()
            >>> file.tags.set(tags)
            >>> file.describe()
            File(id=jb7BY5UJoQVGMUOKiLcn, key=None, suffix=.jpg, description=paradisi05, size=29358, hash=r4tnqmKI_SjrkdLzpuWp4g, hash_type=md5, created_at=2023-07-19 15:48:26.485889+00:00, updated_at=2023-07-19 16:43:17.792241+00:00) # noqa
            ...
            One/Many-to-One:
                🔗 storage: Storage(id=Zl2q0vQB, root=/home/runner/work/lamindb/lamindb/docs/guide/mydata, type=local, updated_at=2023-07-19 14:18:21, created_by_id=DzTjkKse)
                🔗 transform: None
                🔗 run: None
                🔗 created_by: User(id=DzTjkKse, handle=testuser1, email=testuser1@lamin.ai, name=Test User1, updated_at=2023-07-19 14:18:21)
            Many-to-Many:
                🔗 tags (3): ['benchmark', 'example', 'image']
        """
        pass

    def view_parents(self, field: Optional[StrField] = None, distance: int = 100):
        """View parents of a record in a graph.

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.Tissue.from_bionty(name="subsegmental bronchus").save()
            >>> tissue = lb.Tissue.select(name="subsegmental bronchus").one()
            >>> tissue.view_parents()
        """
        pass

    def set_abbr(self, value: str):
        """Set value for abbr field and add to synonyms.

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.ExperimentalFactor.from_bionty(name="single-cell RNA sequencing").save()
            >>> scrna = lb.ExperimentalFactor.select(name="single-cell RNA sequencing").one()
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

    @classmethod
    def from_values(cls, identifiers: ListLike, field: StrField, **kwargs) -> List["ORM"]:
        """Parse values for an identifier (a name, an id, etc.) and create records.

        This method helps avoid problems around duplication of entries,
        violation of idempotency, and performance when creating records in bulk.

        Guide: :doc:`/biology/registries`.

        Args:
            identifiers: ``ListLike`` A list of values for an identifier, e.g.
                ``["name1", "name2"]``.
            field: ``StrField`` An ``ORM`` field to look up, e.g., ``lb.CellMarker.name``.
            **kwargs: Can contain ``species``. Either ``"human"``, ``"mouse"``, or any other
                `name` of `Bionty.Species`. If ``None``, will use default species in
                bionty for each entity.

        Returns:
            A list of records.

        For every ``value`` in a list-like of identifiers and a given `ORM.field`,
        this function performs:

        1. It checks whether the value already exists in the database
           (``ORM.select(field=value)``). If so, it adds the queried record to
           the returned list and skips step 2. Otherwise, proceed with 2.
        2. If the ``ORM`` is from ``lnschema_bionty``, it checks whether there is an
           exact match in the underlying ontology (``Bionty.inspect(value, field)``).
           If so, it creates a record from Bionty and adds it to the returned list.
           Otherwise, it creates a record that populates a single field using `value`
           and adds the record to the returned list.

        Examples:

            Bulk create records:

            >>> projects = ln.Project.from_values(["benchmark", "prediction", "test"], field="name")
            💬 Created 3 Project records with a single field name
            >>> projects
            [Project(id=mDahtPrz, name=benchmark, created_by_id=DzTjkKse),
            Project(id=2Sjmn9il, name=prediction, created_by_id=DzTjkKse),
            Project(id=gdxrHdTA, name=test, created_by_id=DzTjkKse)]

            Bulk create records with shared kwargs:

            >>> pipelines = ln.Transform.from_values(["Pipeline 1", "Pipeline 2"], field="name",
            ...                                      type="pipeline", version="1")
            💬 Created 2 Transform records with a single field name
            >>> pipelines
            [Transform(id=Ts8k7LSZNZhO1t, name=Pipeline 1, stem_id=Ts8k7LSZNZhO, version=1, type=pipeline, created_by_id=DzTjkKse),
            Transform(id=m2UXSAqqttuuXP, name=Pipeline 2, stem_id=m2UXSAqqttuu, version=1, type=pipeline, created_by_id=DzTjkKse)]

            Returns existing records:

            >>> ln.save(ln.Project.from_values(["benchmark", "prediction", "test"], field="name"))
            >>> projects = ln.Project.from_values(["benchmark", "prediction", "test"], field="name")
            💬 Returned 3 existing Project DB records that matched name field
            >>> projects
            [Project(id=iV3DXy70, name=benchmark, updated_at=2023-07-19 16:07:50, created_by_id=DzTjkKse),
            Project(id=99aB57DI, name=prediction, updated_at=2023-07-19 16:07:50, created_by_id=DzTjkKse),
            Project(id=ueaGXwuL, name=test, updated_at=2023-07-19 16:07:50, created_by_id=DzTjkKse)]

            Bulk create records from bionty:

            >>> import lnschema_bionty as lb
            >>> records = lb.CellType.from_values(["T-cell", "B cell"], field="name")
            💬 Created 1 CellType record from Bionty that matched name field (bionty_source_id=S2Yu)
            💬 Created 1 CellType record from Bionty that matched synonyms (bionty_source_id=S2Yu)
            >>> records
            [CellType(id=BxNjby0x, name=T cell, ontology_id=CL:0000084, synonyms=T-cell|T lymphocyte|T-lymphocyte, description=A Type Of Lymphocyte Whose Defining Characteristic Is The Expression Of A T Cell Receptor Complex., bionty_source_id=S2Yu, created_by_id=DzTjkKse), # noqa
            CellType(id=cx8VcggA, name=B cell, ontology_id=CL:0000236, synonyms=B lymphocyte|B-lymphocyte|B-cell, description=A Lymphocyte Of B Lineage That Is Capable Of B Cell Mediated Immunity., bionty_source_id=S2Yu, created_by_id=DzTjkKse)] # noqa

        """
        pass

    @classmethod
    def inspect(
        cls,
        identifiers: ListLike,
        field: StrField,
        *,
        case_sensitive: bool = False,
        inspect_synonyms: bool = True,
        return_df: bool = False,
        logging: bool = True,
        **kwargs,
    ) -> Union["pd.DataFrame", Dict[str, List[str]]]:
        """Inspect if a list of identifiers are mappable to existing values of a field.

        Args:
            identifiers: `ListLike` Identifiers that will be checked against the
                field.
            field: `StrField` The field of identifiers.
                    Examples are 'ontology_id' to map against the source ID
                    or 'name' to map against the ontologies field names.
            case_sensitive: Whether the identifier inspection is case sensitive.
            inspect_synonyms: Whether to inspect synonyms.
            return_df: Whether to return a Pandas DataFrame.

        Returns:
            - A Dictionary of "mapped" and "unmapped" identifiers
            - If `return_df`: A DataFrame indexed by identifiers with a boolean `__mapped__`
                column that indicates compliance with the identifiers.

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.settings.species = "human"
            >>> gene_synonyms = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> ln.save(lb.Gene.from_values(gene_synonyms, field="symbol"))
            >>> lb.Gene.inspect(gene_symbols, field=lb.Gene.symbol)
            🔶 The identifiers contain synonyms!
            To increase mappability, standardize them via '.map_synonyms()'
            ✅ 3 terms (75.0%) are mapped
            🔶 1 terms (25.0%) are not mapped
            {'mapped': ['A1CF', 'A1BG', 'FANCD20'], 'not_mapped': ['FANCD1']}
        """
        pass

    @classmethod
    def lookup(cls, field: Optional[StrField] = None) -> NamedTuple:
        """Return an auto-complete object for a field.

        Args:
            field: `Optional[StrField] = None` The field to
                look up the values for. Defaults to first string field.

        Returns:
            A `NamedTuple` of lookup information of the field values with a
            dictionary converter.

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.settings.species = "human"
            >>> lb.Gene.from_bionty(symbol="ADGB-DT").save()
            >>> lookup = lb.Gene.lookup()
            >>> lookup.adgb_dt
            Gene(id=SoZXq4Wor2vK, symbol=ADGB-DT, ensembl_gene_id=ENSG00000237468, ncbi_gene_ids=101928661, biotype=lncRNA, description=ADGB divergent transcript [Source:HGNC Symbol;Acc:HGNC:55654], synonyms=, updated_at=2023-07-19 18:31:16, species_id=uHJU, bionty_source_id=abZr, created_by_id=DzTjkKse) # noqa
            >>> lookup_dict = lookup.dict()
            >>> lookup_dict['ADGB-DT']
            Gene(id=SoZXq4Wor2vK, symbol=ADGB-DT, ensembl_gene_id=ENSG00000237468, ncbi_gene_ids=101928661, biotype=lncRNA, description=ADGB divergent transcript [Source:HGNC Symbol;Acc:HGNC:55654], synonyms=, updated_at=2023-07-19 18:31:16, species_id=uHJU, bionty_source_id=abZr, created_by_id=DzTjkKse) # noqa
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
        """Maps input synonyms to standardized names.

        Args:
            synonyms: `Iterable` Synonyms that will be standardized.
            return_mapper: `bool = False` If `True`, returns `{input_synonym1:
                standardized_name1}`.
            case_sensitive: `bool = False` Whether the mapping is case sensitive.
            species: `Optional[str]` Map only against this species related entries.
            keep: `Literal["first", "last", False] = "first"` When a synonym maps to
                multiple names, determines which duplicates to mark as
                `pd.DataFrame.duplicated`

                    - "first": returns the first mapped standardized name
                    - "last": returns the last mapped standardized name
                    - `False`: returns all mapped standardized name
            synonyms_field: `str = "synonyms"` A field containing the concatenated synonyms.
            field: `Optional[str]` The field representing the standardized names.

        Returns:
            If `return_mapper` is `False`: a list of standardized names. Otherwise,
            a dictionary of mapped values with mappable synonyms as keys and
            standardized names as values.

        Examples:
            >>> import lnschema_bionty as lb
            >>> lb.settings.species = "human"
            >>> gene_synonyms = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> ln.save(lb.Gene.from_values(gene_synonyms, field="symbol"))
            >>> standardized_names = lb.Gene.map_synonyms(gene_synonyms)
            >>> standardized_names
            ['A1CF', 'A1BG', 'BRCA2', 'FANCD20']
        """

    @classmethod
    def select(cls, **expressions) -> QuerySet:
        """Query records.

        Args:
            expressions: Fields and values passed as Django query expressions.

        Returns:
            A :class:`~lamindb.dev.QuerySet`.

        See Also:

            `django queries <https://docs.djangoproject.com/en/4.2/topics/db/queries/>`__

        Notes:

            For more info, see tutorial: :doc:`/guide/select`.

        Examples:
            >>> ln.Tag(name="my tag").save()
            >>> tag = ln.Tag.select(name="my tag").one()
            >>> tag
            Tag(id=TMn5Zuju, name=my tag, updated_at=2023-07-19 18:24:49, created_by_id=DzTjkKse)
        """
        from lamindb._select import select

        return select(cls, **expressions)

    @classmethod
    def search(
        cls,
        string: str,
        *,
        field: Optional[StrField] = None,
        return_queryset: bool = False,
        limit: Optional[int] = None,
        case_sensitive: bool = False,
        synonyms_field: Optional[StrField] = "synonyms",
    ) -> Union["pd.DataFrame", "QuerySet"]:
        """Search the table.

        Args:
            string: `str` The input string to match against the field ontology values.
            field: `Optional[StrField] = None` The field
                against which the input string is matching.
            top_hit: `bool = False` If `True`, return only the top hit or hits (in
                case of equal scores).
            case_sensitive: `bool = False` Whether the match is case sensitive.
            synonyms_field: `Optional[StrField] = "synonyms"` Search synonyms if
                column is available. If `None`, is ignored.

        Returns:
            A sorted `DataFrame` of search results with a score in column
            `__ratio__`. If `top_hit` is `True`, the best match.

        Examples:
            >>> ln.save(ln.Tag.from_values(["Tag1", "Tag2", "Tag3"], field="name"))
            >>> ln.Tag.search("Tag2")
                        id   __ratio__
            name
            Tag2  o3FY3c5n  100.000000
            Tag1  CcFPLmpq   75.000000
            Tag3  Qi3c4utq   75.000000
        """
        pass

    class Meta:
        abstract = True


# -------------------------------------------------------------------------------------
# A note on required fields at the ORM level
#
# As Django does most of its validation on the Form-level, it doesn't offer functionality
# for validating the integrity of an ORM object upon instantation (similar to pydantic)
#
# For required fields, we define them as commonly done on the SQL level together
# with a validator in ORM (validate_required_fields)
#
# This goes against the Django convention, but goes with the SQLModel convention
# (Optional fields can be null on the SQL level, non-optional fields cannot)
#
# Due to Django's convention where CharField has pre-configured (null=False, default=""), marking
# a required field necessitates passing `default=None`. Without the validator it would trigger
# an error at the SQL-level, with it, it triggers it at instantiation

# -------------------------------------------------------------------------------------
# A note on class and instance methods of core ORM
#
# All of these are defined and tested within lamindb, in files starting with _{orm_name}.py


class User(ORM):
    """Users.

    All data in this table is synched from the cloud user account to ensure a
    universal user identity, valid across DB instances, email & handle changes.

    Examples:

        Creating user records is managed via the :doc:`/guide/configure`.

        Query a user by handle:

        >>> user = ln.User.select(handle="testuser1").one()
        >>> user
        User(id=DzTjkKse, handle=testuser1, email=testuser1@lamin.ai, name=Test User1, updated_at=2023-07-10 18:37:26)

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


class Storage(ORM):
    """Storage locations.

    Either S3 or GCP buckets or local storage locations.

    See Also:

        :attr:`~lamindb.dev.Settings.storage`

    Examples:

        Configure a default storage upon initiation of a LaminDB instance:

        `lamin init --storage ./mydata # or "s3://my-bucket" or "gs://my-bucket"`

        >>> ln.settings.storage
        PosixPath('/home/runner/work/lamindb/lamindb/docs/guide/mydata')

        Set a new default storage (currently doesn't support SQLite instances):

        >>> ln.load("my-postgres-db")
        >>> ln.settings.storage = "./storage_2" # or a cloud bucket
        >>> ln.settings.storage
        PosixPath('/home/runner/work/lamindb-setup/lamindb-setup/docs/guide/storage_2')

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


class Tag(ORM):
    """Tags.

    Examples:

        Create a new tag:

        >>> tag = ln.Tag(name="ML output")
        >>> tag.save()
        >>> tag
        Tag(id=gelGp2P6, name=ML output, created_by_id=DzTjkKse)

        Tag a file:

        >>> tag = ln.Tag.select(name="ML output").one()
        >>> tag
        Tag(id=gelGp2P6, name=ML output, created_by_id=DzTjkKse)
        >>> file = ln.File("./myfile.csv")
        >>> file.save()
        >>> file
        File(id=MveGmGJImYY5qBwmr0j0, suffix=.csv, size=4, hash=CY9rzUYh03PK3k6DJie09g, hash_type=md5, updated_at=2023-07-19 13:47:59, storage_id=597Sgod0, created_by_id=DzTjkKse) # noqa
        >>> file.tags.add(tag)
        >>> file.tags.list("name")
        ['ML output']

        Tag a project:

        >>> ln.Tag(name="benchmark").save()
        >>> tag = ln.Tag.select(name="benchmark").one()
        Tag(id=gelGp2P6, name=benchmark, created_by_id=DzTjkKse)
        >>> ln.Project(name="My awesome project", external_id="Lamin-0001")
        >>> project = ln.Tag.select(name="My awesome project").one()
        >>> project
        Project(id=23QgqohM, name=My awesome project, external_id=Lamin-0001, created_by_id=DzTjkKse)
        >>> project.tags.add(tag)
        >>> project.tags.list("name")
        ['ML output']

        Query by tag:

        >>> ln.File.select(tags__name = "ML output").first()
        File(id=MveGmGJImYY5qBwmr0j0, suffix=.csv, size=4, hash=CY9rzUYh03PK3k6DJie09g, hash_type=md5, updated_at=2023-07-19 13:47:59, storage_id=597Sgod0, created_by_id=DzTjkKse) # noqa
        >>> ln.Project.select(tags__name = "benchmark").first()
        Project(id=23QgqohM, name=My awesome project, external_id=Lamin-0001, created_by_id=DzTjkKse)
    """

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


class Project(ORM):
    """Projects.

    Examples:

        Create a new project:

        >>> project = ln.Project(name="My awesome project", external_id="Lamin-0001")
        >>> project.save()
        >>> project
        Project(id=23QgqohM, name=My awesome project, external_id=Lamin-0001, created_by_id=DzTjkKse)

        Link files to a project:

        >>> project = ln.Tag.select(name="My awesome project").one()
        >>> project
        Project(id=23QgqohM, name=My awesome project, external_id=Lamin-0001, created_by_id=DzTjkKse)
        >>> file = ln.File("./myfile.csv")
        >>> file.save()
        >>> file
        File(id=MveGmGJImYY5qBwmr0j0, suffix=.csv, size=4, hash=CY9rzUYh03PK3k6DJie09g, hash_type=md5, updated_at=2023-07-19 13:47:59, storage_id=597Sgod0, created_by_id=DzTjkKse) # noqa
        >>> file.projects.add(project)
        >>> file.projects.list("name")
        ['My awesome project']

        Query a file by project:

        >>> ln.File.select(projects__name = "My awesome project").first()
        File(id=MveGmGJImYY5qBwmr0j0, suffix=.csv, size=4, hash=CY9rzUYh03PK3k6DJie09g, hash_type=md5, updated_at=2023-07-19 13:47:59, storage_id=597Sgod0, created_by_id=DzTjkKse)
    """

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


class Transform(ORM):
    """Transformations of files (:class:`~lamindb.File`).

    Pipelines, workflows, notebooks, app-based transformations.

    A pipeline is versioned software that transforms data.
    This can be anything from typical workflow tools (Nextflow, Snakemake,
    Prefect, Apache Airflow, etc.) to simple (versioned) scripts.

    See Also:

        :meth:`lamindb.track`
            Track global Transform & Run for a notebook or pipeline.
        :meth:`lamindb.context`
            Global run context.

    Notes:

        For more info, see tutorial: :doc:`/guide/data-lineage`.

    Examples:

        Create a transform form a pipeline:

        >>> transform = ln.Transform(name="Cell Ranger", version="7.2.0", type="pipeline")
        >>> transform
        Transform(id=JhiujsLlbTKLIt, name=Cell Ranger, stem_id=JhiujsLlbTKL, version=7.2.0, type=pipeline, created_by_id=DzTjkKse)
        >>> transform.save()

        Create a transform from a notebook:

        >>> ln.track()
        ✅ Saved: Transform(id=1LCd8kco9lZUBg, name=Track data lineage / provenance, short_name=02-data-lineage, stem_id=1LCd8kco9lZU, version=0, type=notebook, updated_at=2023-07-10 18:37:19, created_by_id=DzTjkKse) # noqa
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
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent transforms (predecessors) in data lineage.

    These are auto-populated whenever a transform loads a file as run input.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_transforms")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("stem_id", "version"),)


class Run(ORM):
    """Runs of transformations (:class:`~lamindb.Transform`).

    Typically, a run has inputs and outputs:

    - References to outputs are stored in :class:`~lamindb.File` in the `run` field.
      This is possible as every given file has a unique run that created it. Any
      given `Run` can output multiple `files`: `run.outputs`.
    - References to inputs are stored in the :class:`~lamindb.File` in the
      `input_of` field. Any `file` might serve as an input for multiple `runs`.
      Similarly, any `run` might have many `files` as inputs: `run.inputs`.

    Notes:

        For more info, see tutorial: :doc:`/guide/data-lineage`.

    Examples:

        Track a pipeline run:

        >>> ln.Transform(name="Cell Ranger", version="7.2.0", type="pipeline").save()
        >>> transform = ln.Transform.select(name="Cell Ranger", version="7.2.0").one()
        >>> transform
        Transform(id=JhiujsLlbTKLIt, name=Cell Ranger, stem_id=JhiujsLlbTKL, version=7.2.0, type=pipeline, created_by_id=DzTjkKse)
        >>> ln.track(transform)
        💬 Loaded: Transform(id=ceHkZMaiHFdoB6, name=Cell Ranger, stem_id=ceHkZMaiHFdo, version=7.2.0, type=pipeline, updated_at=2023-07-10 18:37:19, created_by_id=DzTjkKse)
        ✅ Saved: Run(id=RcpWIKC8cF74Pn3RUJ1W, run_at=2023-07-10 18:37:19, transform_id=ceHkZMaiHFdoB6, created_by_id=DzTjkKse)
        >>> ln.context.run
        Run(id=RcpWIKC8cF74Pn3RUJ1W, run_at=2023-07-10 18:37:19, transform_id=ceHkZMaiHFdoB6, created_by_id=DzTjkKse)

        Track a notebook run:

        >>> ln.track()
        ✅ Saved: Transform(id=1LCd8kco9lZUBg, name=Track data lineage / provenance, short_name=02-data-lineage, stem_id=1LCd8kco9lZU, version=0, type=notebook, updated_at=2023-07-10 18:37:19, created_by_id=DzTjkKse) # noqa
        ✅ Saved: Run(id=pHgVICV9DxBaV6BAuKJl, run_at=2023-07-10 18:37:19, transform_id=1LCd8kco9lZUBg, created_by_id=DzTjkKse)
        >>> ln.context.run
        Run(id=pHgVICV9DxBaV6BAuKJl, run_at=2023-07-10 18:37:19, transform_id=1LCd8kco9lZUBg, created_by_id=DzTjkKse)
    """

    id = models.CharField(max_length=20, default=base62_20, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Name or title of run."""
    external_id = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """External id (such as from a workflow tool)."""
    transform = models.ForeignKey(Transform, CASCADE, related_name="runs")
    """The transform :class:`~lamindb.Transform` that is being run."""
    inputs = models.ManyToManyField("File", related_name="input_of")
    """The input files for the run."""
    # outputs on File
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    run_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of run execution."""
    created_by = models.ForeignKey(User, CASCADE, default=current_user_id, related_name="created_runs")
    """Creator of record, a :class:`~lamindb.User`."""


class Dataset(ORM):
    """Datasets.

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

    Notes:

        For more info, see tutorial: :doc:`/guide/tutorial1`.

    Examples:

        >>> df = ln.dev.datasets.df_iris_in_meter_batch1()
        >>> df.head()
          sepal_length sepal_width petal_length petal_width iris_species_code
        0        0.051       0.035        0.014       0.002                 0
        1        0.049       0.030        0.014       0.002                 0
        2        0.047       0.032        0.013       0.002                 0
        3        0.046       0.031        0.015       0.002                 0
        4        0.050       0.036        0.014       0.002                 0
        >>> dataset = ln.Dataset(df, name="Iris flower dataset batch1")
        >>> dataset
        Dataset(id=uGQtiyepMdHOq3sZCFWV, name=Iris flower dataset batch1, hash=c5WgMCRPca2iZ2pqC3KiKQ, file_id=uGQtiyepMdHOq3sZCFWV, created_by_id=DzTjkKse)
        >>> dataset.save()
        💡 storing file uGQtiyepMdHOq3sZCFWV with key .lamindb/uGQtiyepMdHOq3sZCFWV.parquet
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


class Feature(ORM):
    """Features.

    Notes:

        You can use `lnschema_bionty` ORMs to manage common features like genes,
        pathways, proteins & cell markers.

        Similarly, you can define custom ORMs to manage features like gene sets, nodes, etc.

        This ORM is a way of getting started without using Bionty or a custom schema.

    Examples:

        >>> df = pd.DataFrame({"feat1": [1, 2], "feat2": [3.1, 4.2], "feat3": ["cond1", "cond2"]})
        >>> features = ln.Feature.from_df(df)
        >>> features.save()
        >>> # the information from the DataFrame is now available in the Feature table
        >>> ln.Feature.select().df()
        id    name    type
         a   feat1     int
         b   feat2 float64
         c   feat3     str

        For more info, see tutorial: :doc:`/biology/features`.
    """

    id = models.CharField(max_length=12, default=base62_12, primary_key=True)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, db_index=True, default=None)
    """Name of feature (required)."""
    type = models.CharField(max_length=96, null=True, default=None)
    """Type. If an ORM, is formatted as ``"{schema_name}{ORM.__name__}"``."""
    unit = models.CharField(max_length=30, null=True, default=None)
    """Unit of measure, ideally SI, e.g., `m`, `s`, `kg`, etc."""
    description = models.TextField(null=True, default=None)
    """A description."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms."""
    feature_sets = models.ManyToManyField("FeatureSet", related_name="features")
    """Feature sets linked to this gene."""
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
        type: Optional[str],
        field: Optional[str],
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
        pass

    @classmethod
    def from_df(
        cls,
        df: "pd.DataFrame",
    ) -> List["Feature"]:
        """Create Feature records for columns."""
        pass

    def save(self, *args, **kwargs) -> None:
        """Save."""
        pass


class FeatureSet(ORM):
    """Jointly measured sets of features.

    .. note::

        A `FeatureSet` is a useful entity as you might have millions of data batches
        that measure the same features: All of them would link against a single
        feature set. If instead, you'd link against single features (say, genes),
        you'd face exploding link tables.

        A `feature_set` is identified by the hash of the id set for the feature type.

    Notes:

        - :doc:`/biology/scrna`
        - :doc:`/biology/flow`

    Examples:

        >>> df = pd.DataFrame({"feat1": [1, 2], "feat2": [3.1, 4.2], "feat3": ["cond1", "cond2"]})
        >>> feature_set = ln.FeatureSet.from_df(df)

        >>> features = ln.Feature.from_values(["feat1", "feat2"])
        >>> ln.FeatureSet(features)

        >>> import lnschema_bionty as bt
        >>> reference = bt.Gene(species="mouse")
        >>> feature_set = ln.FeatureSet.from_values(adata.var["ensemble_id"], Gene.ensembl_gene_id)
        >>> feature_set.save()
        >>> file = ln.File(adata, name="Mouse Lymph Node scRNA-seq")
        >>> file.save()
        >>> file.feature_sets.add(feature_set)
    """

    id = models.CharField(max_length=20, primary_key=True, default=None)
    """A universal id (hash of the set of feature identifiers)."""
    type = models.CharField(max_length=64)
    """Type formatted as ``"{schema_name}{ORM.__name__}"``."""
    field = models.CharField(max_length=64)
    """Field of ORM that was hashed."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_featuresets")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        features: List[ORM],
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

    @classmethod  # type:ignore
    def from_values(cls, values: ListLike, field: Field = Feature.name, **kwargs) -> "FeatureSet":  # type: ignore
        """Create feature set from identifier values.

        Args:
           values: ``ListLike`` A list of identifiers, like feature names or ids.
           field: ``Field = Feature.name`` The field of a reference ORM to
               map values.
           **kwargs: Can contain ``species`` or other context to interpret values.

        Example:

            >>> features = ["feat1", "feat2"]
            >>> feature_set = ln.FeatureSet.from_values(features)

            >>> genes = ["ENS980983409", "ENS980983410"]
            >>> feature_set = ln.FeatureSet.from_values(features, lb.Gene.ensembl_gene_id)
        """
        pass

    @classmethod
    def from_df(
        cls,
        df: "pd.DataFrame",
    ) -> "FeatureSet":
        """Create Feature records for columns."""
        pass

    def save(self, *args, **kwargs) -> None:
        """Save."""


class Category(ORM):
    """Categories of categorical features.

    This is the default registry for tracking categories of categorical features.

    If you're working a lot with different cell lines, proteins, genes, or other
    entities of complexity, consider using the pre-defined biological registries
    in :mod:`lnschema_bionty`.
    """

    id = models.CharField(max_length=12, default=base62_12, primary_key=True)
    """Universal id, valid across DB instances."""
    feature = models.ForeignKey(Feature, CASCADE, related_name="values")
    """Feature."""
    value = models.CharField(max_length=128)
    """String value of category."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_categories")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("feature", "value"),)


class File(ORM):
    """Files.

    Args:
        data: `Union[PathLike, DataLike]` A file path or an in-memory data
            object (`DataFrame`, `AnnData`) to serialize. Can be a cloud path, e.g.,
            `"s3://my-bucket/my_samples/my_file.fcs"`.
        key: `Optional[str] = None` A storage key: a relative filepath within the
            current default storage, e.g., `"my_samples/my_file.fcs"`.
        name: `Optional[str] = None` A description.
        run: `Optional[Run] = None` The run that created the file, gets auto-linked
            if `ln.track()` was called.
        feature_sets: `Optional[List[FeatureSet]] = None` A list of `FeatureSet`
            records describing the features measured in the file.

    Track where files come from by passing the generating :class:`~lamindb.Run`.

    Often, files store jointly measured features: track them with
    :class:`~lamindb.FeatureSet`.

    If files have corresponding representations in storage and memory, LaminDB
    makes some configurable default choices (e.g., serialize a `DataFrame` as a
    `.parquet` file).

    .. admonition:: Formats in storage & their API access

        Listed are typical `suffix` values & in memory data objects.

        - Table: `.csv`, `.tsv`, `.parquet`, `.ipc` ⟷ `DataFrame`, `pyarrow.Table`
        - Annotated matrix: `.h5ad`, `.h5mu`, `.zrad` ⟷ `AnnData`, `MuData`
        - Image: `.jpg`, `.png` ⟷ `np.ndarray`, ...
        - Arrays: HDF5 group, zarr group, TileDB store ⟷ HDF5, zarr, TileDB loaders
        - Fastq: `.fastq` ⟷ /
        - VCF: `.vcf` ⟷ /
        - QC: `.html` ⟷ /

    .. note::

        In some cases, e.g. for zarr-based storage, a `File` object is stored as
        many small objects in what appears to be a "folder" in storage.

    See Also:

        :meth:`lamindb.File.from_df`
            Create a file object from `DataFrame`.
        :meth:`lamindb.File.from_anndata`
            Create a file object from `AnnData`.
        :meth:`lamindb.File.from_dir`
            Bulk create file objects from a directory.

    Notes:

        For more info, see tutorial: :doc:`/guide/tutorial1`.

    Examples:

        Track a file from a local filepath:

        >>> filepath = ln.dev.datasets.file_mini_csv()
        >>> filepath
        PosixPath('mini.csv')
        >>> file = ln.File(filepath)
        💡 File will be copied to storage upon `save()` using storage key = WpfMHb5u3Jp8mzoTs3SH.csv
        >>> file
        File(id=WpfMHb5u3Jp8mzoTs3SH, suffix=.csv, size=11, hash=z1LdF2qN4cN0M2sXrcW8aw, hash_type=md5, storage_id=Zl2q0vQB, created_by_id=DzTjkKse)
        >>> file.save()
        💡 storing file WpfMHb5u3Jp8mzoTs3SH with key .lamindb/WpfMHb5u3Jp8mzoTs3SH.csv

        Track a file from a cloud storage (supports `s3://` and `gs://`):

        >>> file = ln.File("s3://lamindb-ci/test-data/test.csv")
        💡 File in storage ✓ using storage key = test-data/test.csv
        >>> file
        File(id=YDELGH3FqhtiZI7IMWnH, key=test-data/test.csv, suffix=.csv, size=329, hash=85-PotiFdQ2rpJvfLtOISA, hash_type=md5, storage_id=Z7zewD72, created_by_id=DzTjkKse)
        >>> file.save()
    """

    id = models.CharField(max_length=20, primary_key=True)
    """A universal random id (20-char base62), valid across DB instances."""
    storage: "Storage" = models.ForeignKey(Storage, PROTECT, related_name="files")
    """Storage location (:class:`~lamindb.Storage`), e.g., an S3 bucket, local folder or network location."""
    key = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """Storage key, the relative path within the storage location."""
    suffix = models.CharField(max_length=30, db_index=True, null=True, default=None)
    """File suffix.

    This is a file extension if the `file` is stored in a file format.
    It's `None` if the storage format doesn't have a canonical extension.
    """
    description = models.CharField(max_length=255, db_index=True, null=True, default=None)
    """A description."""
    size = models.BigIntegerField(null=True, db_index=True)
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    hash = models.CharField(max_length=86, db_index=True, null=True, default=None)  # 86 base64 chars allow to store 64 bytes, 512 bits
    """Hash or pseudo-hash of file content.

    Useful to ascertain integrity and avoid duplication.
    """
    hash_type = models.CharField(max_length=30, db_index=True, null=True, default=None)
    """Type of hash."""
    feature_sets = models.ManyToManyField(FeatureSet, related_name="files")
    """Files linked to the feature set."""
    transform = models.ForeignKey(Transform, PROTECT, related_name="files", null=True)
    """:class:`~lamindb.Transform` whose run created the `file`."""
    run = models.ForeignKey(Run, PROTECT, related_name="outputs", null=True)
    """:class:`~lamindb.Run` that created the `file`."""
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

    @overload
    def __init__(
        self,
        data: Union[PathLike, DataLike],
        key: Optional[str] = None,
        run: Optional[Run] = None,
        name: Optional[str] = None,
        feature_sets: Optional[List[FeatureSet]] = None,
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
        columns_ref: Field = Feature.name,
        key: Optional[str] = None,
        description: Optional[str] = None,
        run: Optional[Run] = None,
    ) -> "File":
        """Create from ``DataFrame``, link column names as features.

        See Also:

            :meth:`lamindb.Dataset`
                Track datasets.
            :class:`lamindb.Feature`
                Track features.

        Notes:

            For more info, see tutorial: :doc:`/guide/tutorial1`.

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
            💡 File will be copied to storage upon `save()` using storage key = kV3JQuBw4izvUdAkjO4p.parquet
            💬 Created 5 Feature records with a single field name
            >>> file
            File(id=kV3JQuBw4izvUdAkjO4p, suffix=.parquet, description=Iris flower dataset batch1, size=5334, hash=RraiKH9BAtAgS5jg7LWUiA, hash_type=md5, storage_id=Zl2q0vQB, created_by_id=DzTjkKse) # noqa
            >>> file.save()
            💬 Created 2 Category records with a single field value
            💡 storing file kV3JQuBw4izvUdAkjO4p with key .lamindb/kV3JQuBw4izvUdAkjO4p.parquet
        """
        pass

    @classmethod
    def from_anndata(
        cls,
        adata: "AnnDataLike",
        var_ref: Optional[Field],
        obs_columns_ref: Optional[Field] = Feature.name,
        key: Optional[str] = None,
        description: Optional[str] = None,
        run: Optional[Run] = None,
    ) -> "File":
        """Create from ``AnnData`` or ``.h5ad`` file, link ``var_names`` and ``obs.columns`` as features.

        See Also:

            :meth:`lamindb.Dataset`
                Track datasets.
            :class:`lamindb.Feature`
                Track features.

        Notes:

            For more info, see tutorial: :doc:`/guide/tutorial1`.

        Examples:

            >>> import lnschema_bionty as lb
            lb.settings.species = "human"
            ✅ Set species: Species(id=uHJU, name=human, taxon_id=9606, scientific_name=homo_sapiens, updated_at=2023-07-19 14:45:17, bionty_source_id=t317, created_by_id=DzTjkKse) # noqa
            >>> adata = ln.dev.datasets.anndata_with_obs()
            >>> adata
            AnnData object with n_obs × n_vars = 40 × 100
                obs: 'cell_type', 'cell_type_id', 'tissue', 'disease'
            >>> adata.var_names[:2]
            Index(['ENSG00000000003', 'ENSG00000000005'], dtype='object')
            >>> file = ln.File.from_anndata(adata,
            ...                             var_ref=lb.Gene.ensembl_gene_id,
            ...                             description="mini anndata with obs")
            💡 File will be copied to storage upon `save()` using storage key = XcohavbmpLDhAnCrALVC.h5ad
            💬 Using global setting species = human
            💬 Created 99 Gene records from Bionty that matched ensembl_gene_id field (bionty_source_id=abZr)
            💬 Created 4 Feature records with a single field name
            >>> file.save()
            💡 storing file XcohavbmpLDhAnCrALVC with key .lamindb/XcohavbmpLDhAnCrALVC.h5ad
        """
        pass

    @classmethod
    def from_dir(
        cls,
        path: PathLike,
        *,
        run: Optional[Run] = None,
    ) -> List["File"]:
        """Create a list of file objects from a directory.

        Examples:

            >>> dir_path = ln.dev.datasets.generate_cell_ranger_files("sample_001", ln.settings.storage)
            >>> dir_path.name
            'sample_001'
            >>> files = ln.File.from_dir(dir_path)
            💡 using storage prefix = sample_001/
            💬 → 15 files
            >>> files[0]
            File(id=cbGk8IUFIERkTgjBQ2kb, key=sample_001/web_summary.html, suffix=.html, size=6, hash=n4HLxPQUWXUeKl-OLzq6ew, hash_type=md5, storage_id=Zl2q0vQB, created_by_id=DzTjkKse) # noqa
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
            data: ``Union[PathLike, DataLike]`` A file path or an in-memory data
                object (`DataFrame`, `AnnData`).
            run: ``Optional[Run] = None`` The run that created the file gets
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
        """Return a cloud-backed data object to stream.

        Notes:
            For more info, see tutorial: :doc:`/guide/stream`.

        Examples:

            Read AnnData in backed mode from cloud:

            >>> file = ln.File.select(key="lndb-storage/pbmc68k.h5ad").one()
            >>> file.backed()
            AnnData object with n_obs × n_vars = 70 × 765 backed at 's3://lamindb-ci/lndb-storage/pbmc68k.h5ad'
                obs: ['cell_type', 'index', 'louvain', 'n_genes', 'percent_mito']
                obsm: ['X_pca', 'X_umap']
                obsp: ['connectivities', 'distances']
                uns: ['louvain', 'louvain_colors', 'neighbors', 'pca']
                var: ['highly_variable', 'index', 'n_counts']
                varm: ['PCs']
        """
        pass

    @classmethod
    def tree(
        cls,
        prefix: Optional[str] = None,
        *,
        level: int = -1,
        limit_to_directories: bool = False,
        length_limit: int = 1000,
    ):
        """Given a prefix, print a visual tree structure of files.

        Examples:

            >>> dir_path = ln.dev.datasets.generate_cell_ranger_files("sample_001", ln.settings.storage)
            >>> dir_path.name
            'sample_001'
            >>> ln.File.tree(dir_path)
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
            ...
            3 directories, 15 files
        """
        pass

    def path(self) -> Union[Path, UPath]:
        """Path in storage.

        Examples:

            File in cloud storage:

            >>> ln.File("s3://lamindb-ci/lndb-storage/pbmc68k.h5ad").save()
            >>> file = ln.File.select(key="lndb-storage/pbmc68k.h5ad").one()
            >>> file.path()
            S3Path('s3://lamindb-ci/lndb-storage/pbmc68k.h5ad')

            File in local storage:

            >>> ln.File("./myfile.csv", description="myfile").save()
            >>> file = ln.File.select(description="myfile").one()
            >>> file.path()
            PosixPath('/home/runner/work/lamindb/lamindb/docs/guide/mydata/myfile.csv')
        """
        pass

    def load(self, is_run_input: Optional[bool] = None, stream: bool = False) -> DataLike:
        """Stage and load to memory.

        Returns in-memory representation if possible, e.g., an `AnnData` object for an `h5ad` file.

        Examples:

            Load as a `DataFrame`:

            >>> ln.File.from_df(ln.dev.datasets.df_iris_in_meter_batch1(), description="iris").save()
            >>> file = ln.File.select(description="iris").one()
            >>> file.load().head()
            sepal_length sepal_width petal_length petal_width iris_species_code
            0        0.051       0.035        0.014       0.002                 0
            1        0.049       0.030        0.014       0.002                 0
            2        0.047       0.032        0.013       0.002                 0
            3        0.046       0.031        0.015       0.002                 0
            4        0.050       0.036        0.014       0.002                 0

            Load as an `AnnData`:

            >>> ln.File("s3://lamindb-ci/lndb-storage/pbmc68k.h5ad").save()
            >>> file = ln.File.select(key="lndb-storage/pbmc68k.h5ad").one()
            >>> file.load()
            AnnData object with n_obs × n_vars = 70 × 765
                obs: 'cell_type', 'n_genes', 'percent_mito', 'louvain'
                var: 'n_counts', 'highly_variable'
                uns: 'louvain', 'louvain_colors', 'neighbors', 'pca'
                obsm: 'X_pca', 'X_umap'
                varm: 'PCs'
                obsp: 'connectivities', 'distances'

            Fall back to :meth:`~lamindb.File.stage` if no in-memory representation is configured:

            >>> ln.File(ln.dev.datasets.file_jpg_paradisi05(), description="paradisi05").save()
            >>> file = ln.File.select(description="paradisi05").one()
            >>> file.load()
            PosixPath('/home/runner/work/lamindb/lamindb/docs/guide/mydata/.lamindb/jb7BY5UJoQVGMUOKiLcn.jpg')
        """
        pass

    def stage(self, is_run_input: Optional[bool] = None) -> Path:
        """Update cache from cloud storage if outdated.

        Returns a path to a locally cached on-disk object (say, a `.jpg` file).

        Examples:

            Sync file from cloud and returns the local path of the cache:

            >>> ln.File("s3://lamindb-ci/lndb-storage/pbmc68k.h5ad").save()
            >>> file = ln.File.select(key="lndb-storage/pbmc68k.h5ad").one()
            >>> file.stage()
            PosixPath('/home/runner/work/Caches/lamindb/lamindb-ci/lndb-storage/pbmc68k.h5ad')
        """
        pass

    def delete(self, storage: Optional[bool] = None) -> None:
        """Delete file, optionally from storage.

        Args:
            storage: `Optional[bool] = None` Indicate whether you want to delete the
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
            💡 File will be copied to storage upon `save()` using storage key = myfile.csv
            >>> file.save()
            💡 storing file 2fO9kSKVXFXYoLccExOY with key myfile.csv
        """
        pass


# -------------------------------------------------------------------------------------
# Low-level logic needed in lamindb-setup

# Below is needed within lnschema-core because lamindb-setup already performs
# some logging


def format_datetime(dt: Union[datetime, Any]) -> str:
    if not isinstance(dt, datetime):
        return dt
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


def __repr__(self: ORM) -> str:
    field_names = [field.name for field in self._meta.fields if (not isinstance(field, models.ForeignKey) and field.name != "created_at")]
    field_names += [f"{field.name}_id" for field in self._meta.fields if isinstance(field, models.ForeignKey)]
    fields_str = {k: format_datetime(getattr(self, k)) for k in field_names if hasattr(self, k)}
    fields_joined_str = ", ".join([f"{k}={fields_str[k]}" for k in fields_str if fields_str[k] is not None])
    return f"{self.__class__.__name__}({fields_joined_str})"


ORM.__repr__ = __repr__  # type: ignore
ORM.__str__ = __repr__  # type: ignore
