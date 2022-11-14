from datetime import datetime as datetime
from typing import Optional

from sqlmodel import Field, ForeignKeyConstraint

from . import _name as schema_name
from ._timestamps import CreatedAt, UpdatedAt
from ._users import CreatedBy
from .dev import id as idg
from .dev._storage import filepath_from_dobject
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
    """Universal base62 ID, generated by :func:`~lnschema_core.dev.id.storage`."""
    root: str = Field(index=True)
    """Semantic identifier to the root of the storage location, like an s3 path, a local path, etc."""  # noqa
    type: Optional[str] = None
    """Local vs. s3 vs. gcp etc."""
    region: Optional[str] = None
    """Cloud storage region if applicable."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class DSet(SQLModel, table=True):  # type: ignore
    """Datasets: collections of data objects.

    In LaminDB, a dataset is a collection of data objects (`DObject`).
    """

    id: str = Field(default_factory=idg.dset, primary_key=True)
    name: str = Field(index=True)
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lnschema_core.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""
    updated_at: Optional[datetime] = UpdatedAt
    """Time of last update."""


class DSetDObject(SQLModel, table=True):  # type: ignore
    """Link table of dset and dobject."""

    __tablename__ = f"{prefix}dset_dobject"

    dset_id: str = Field(foreign_key="core.dset.id", primary_key=True)
    """Link to :class:`~lnschema_core.dset`."""
    dobject_id: str = Field(foreign_key="core.dobject.id", primary_key=True)
    """Link to :class:`~lnschema_core.dobject`."""


class Project(SQLModel, table=True):  # type: ignore
    """Projects."""

    id: str = Field(default_factory=idg.project, primary_key=True)
    name: str = Field(index=True)
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lnschema_core.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""
    updated_at: Optional[datetime] = UpdatedAt
    """Time of last update."""


class ProjectDSet(SQLModel, table=True):  # type: ignore
    """Link table of project and dset."""

    __tablename__ = f"{prefix}project_dset"

    project_id: str = Field(foreign_key="core.project.id", primary_key=True)
    """Link to :class:`~lnschema_core.dobject`."""
    dset_id: str = Field(foreign_key="core.dset.id", primary_key=True)
    """Link to :class:`~lnschema_core.dset`."""


class DObject(SQLModel, table=True):  # type: ignore
    """Data objects in storage & memory.

    Data objects (`dobjects`) represent atomic datasets: jointly measured
    observations of variables (features) that are stored in object storage.

    They are generated by running code (`runs`, instances of
    :class:`~lnschema_core.Run`).

    A `dobject` might contain a single observation, for instance, a single image.

    Data objects typically have canonical on-disk and in-memory representations. If
    choices among these representations are made, a one-to-one mapping can be
    achieved, which means that any given `dobject` has a default in-memory and
    on-disk representation.

    LaminDB offers meaningful default choices. For instance,

    - It defaults to pandas DataFrames for in-memory representation of tables
      and allows you to configure loading tables into polars DataFrames.
    - It defaults to the `.parquet` format for tables, but allows you to
      configure `.csv` or `.ipc`.

    Some datasets do not have a canonical in-memory representation, for
    instance, `.fastq`, `.vcf`, or files describing QC of datasets.

    Examples for storage ⟷ memory correspondence:

    - Table: `.csv`, `.tsv`, `.parquet`, `.ipc` (`.feather`) ⟷
      `pandas.DataFrame`, `polars.DataFrame`
    - Annotated matrix: `.h5ad`, `.h5mu`, `.zarrad` ⟷ `anndata.AnnData`,
      `mudata.MuData`
    - Image: `.jpg`, `.png` ⟷ `np.ndarray`, or a dedicated imaging in-memory
      container
    - Tensor: zarr directory, TileDB store ⟷ zarr loader, TileDB loader
    - Fastq: `.fastq` ⟷ /
    - VCF: `.vcf` ⟷ /
    - QC: `.html` ⟷ /
    """

    id: str = Field(default_factory=idg.dobject, primary_key=True)
    """Universal base62 ID, generated by :func:`~lnschema_core.dev.id.dobject`."""
    name: Optional[str] = Field(index=True)
    """Semantic name or title. Defaults to `None`."""
    suffix: Optional[str] = Field(default=None, index=True)
    """Suffix to construct the storage key. Defaults to `None`.

    This is a file extension if the `dobject` is stored in a file format.
    It's `None` if the storage format doesn't have a canonical extension.
    """
    size: Optional[float] = Field(default=None, index=True)
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    run_id: str = Field(foreign_key="core.run.id", index=True)
    """Link to :class:`~lnschema_core.Run` that generated the `dobject`."""
    storage_id: str = Field(foreign_key="core.storage.id", index=True)
    """Link to :class:`~lnschema_core.Storage` location that stores the `dobject`."""
    checksum: Optional[str] = Field(default=None, index=True)
    """Checksum of file (md5)."""
    created_at: datetime = CreatedAt
    """Time of creation."""
    updated_at: Optional[datetime] = UpdatedAt
    """Time of last update."""

    @property
    def path(self):
        """Path on storage."""
        return filepath_from_dobject(self)


class Run(SQLModel, table=True):  # type: ignore
    """Code runs that transform data.

    A data transformation (`run`) is _any_ transformation of a `dobject`.

    For instance:

    - Jupyter notebooks (`jupynb`)
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
            ["jupynb_id", "jupynb_v"],
            ["core.jupynb.id", "core.jupynb.v"],
        ),
        {"schema": schema_arg},
    )
    id: str = Field(default_factory=idg.run, primary_key=True)
    """Universal base62 ID & primary key, generated through :func:`~lnschema_core.dev.id.run`."""  # noqa
    name: Optional[str] = Field(default=None, index=True)
    pipeline_id: Optional[str] = Field(default=None, index=True)
    """Link to :class:`~lnschema_core.Pipeline`."""
    pipeline_v: Optional[str] = Field(default=None, index=True)
    jupynb_id: Optional[str] = Field(default=None, index=True)
    """Link to :class:`~lnschema_core.Jupynb`."""
    jupynb_v: Optional[str] = Field(default=None, index=True)
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lnschema_core.User`."""
    created_at: datetime = CreatedAt


class RunIn(SQLModel, table=True):  # type: ignore
    """Inputs of runs.

    This is a many-to-many link table for `run` and `dobject` storing the
    inputs of data transformations.

    A data transformation can have an arbitrary number of data objects as inputs.

    - The same `dobject` can be used as input in many different `runs`.
    - One `run` can have several `dobjects` as inputs.
    """

    __tablename__ = f"{prefix}run_in"

    run_id: str = Field(foreign_key="core.run.id", primary_key=True)
    """Link to :class:`~lnschema_core.Run`."""
    dobject_id: str = Field(foreign_key="core.dobject.id", primary_key=True)
    """Link to :class:`~lnschema_core.DObject`."""


class Jupynb(SQLModel, table=True):  # type: ignore
    """Jupyter notebooks.

    Jupyter notebooks (`jupynbs`) represent one type of data transformation
    (`run`) and have a unique correspondence in `run`.

    IDs for Jupyter notebooks are generated through nbproject.
    """

    id: str = Field(default=None, primary_key=True)
    """Universal base62 ID & primary key, generated by :func:`~lnschema_core.dev.id.jupynb`."""  # noqa
    v: str = Field(default="1", primary_key=True)
    """Version identifier, defaults to `"1"`.

    Use this to label different versions of the same notebook.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    name: str = Field(index=True)
    """Title of the notebook as generated by `nbproject.meta.title
    <https://lamin.ai/docs/nbproject/nbproject.dev.metalive#nbproject.dev.MetaLive.title>`__.
    """
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lnschema_core.User`."""
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
    """Auto-populated link to :class:`~lnschema_core.User`."""
    created_at: datetime = CreatedAt
    """Auto-populated time stamp."""
    updated_at: Optional[datetime] = UpdatedAt


class Usage(SQLModel, table=True):  # type: ignore
    """Data usage log.

    Any API call in the `lamindb.db` API is logged here.
    """

    id: str = Field(default_factory=idg.usage, primary_key=True)
    """Universal base62 ID & primary key, generated by :func:`~lnschema_core.dev.id.usage`."""  # noqa
    type: usage_type = Field(nullable=False, index=True)
    """Usage type."""
    user_id: str = CreatedBy
    """Link to :class:`~lnschema_core.User`."""
    time: datetime = CreatedAt
    """Time of event."""
    dobject_id: str = Field(foreign_key="core.dobject.id", index=True)
    """Link to the affected :class:`~lnschema_core.DObject`."""
