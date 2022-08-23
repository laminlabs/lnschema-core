from datetime import datetime as datetime
from enum import Enum
from typing import Optional, Union

from sqlmodel import Field, ForeignKeyConstraint, SQLModel, UniqueConstraint

from .id import id_dobject, id_dtransform, id_storage, id_usage


def utcnow():
    return datetime.utcnow().replace(microsecond=0)


class version_yvzi(SQLModel, table=True):  # type: ignore
    """Core schema module versions deployed in a given instance.

    Migrations of the schema module add rows to this table, storing the schema
    module version to which we migrated along with the user who performed the
    migration.
    """

    v: Optional[str] = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    time_created: datetime = Field(default_factory=utcnow, nullable=False)


class user(SQLModel, table=True):  # type: ignore
    """Users operating a given LaminDB instance.

    The All data here is always synched from the corresponding table in the hub.
    """

    __table_args__ = (
        UniqueConstraint("email"),
        UniqueConstraint("handle"),
    )
    id: Optional[str] = Field(primary_key=True)
    email: str = Field(index=True)
    handle: str = Field(nullable=False, index=True)
    time_created: datetime = Field(default_factory=utcnow, nullable=False)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False)


class storage(SQLModel, table=True):  # type: ignore
    """Storage locations.

    A dobject or dtransform-associated file can be stored in any desired S3,
    GCP, Azure or local storage location. This table tracks these locations
    along with metadata.
    """

    id: Optional[str] = Field(default_factory=id_storage, primary_key=True)
    root: str = Field(index=True)
    region: Optional[str]
    type: Optional[str]
    time_created: datetime = Field(default_factory=utcnow, nullable=False)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False)


class dobject(SQLModel, table=True):  # type: ignore
    """Data objects in storage & memory.

    Data objects (`dobjects`) always represent a dataset, a set of jointly measured
    observations of variables (features).

    A `dobject` might contain a single observation, for instance, a single image.

    Datasets typically have canonical on-disk and in-memory representations. If
    choices among these representations are made, a one-to-one mapping can be
    achieved, which means that any given `dobject` has a default in-memory and
    on-disk representation.

    LaminDB offers meaningful default representations. For instance,

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

    id: Optional[str] = Field(default_factory=id_dobject, primary_key=True)
    v: str = Field(default=None, primary_key=True)
    name: Optional[str] = Field(index=True)
    file_suffix: str = Field(index=True)
    dtransform_id: str = Field(foreign_key="dtransform.id", index=True)
    storage_id: str = Field(foreign_key="storage.id", index=True)
    time_created: datetime = Field(default_factory=utcnow, nullable=False, index=True)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False, index=True)


class dtransform(SQLModel, table=True):  # type: ignore
    """Data transformations.

    A data transformation (`dtransform`) is _any_ transformation of a `dobject`.
    For instance:

    - Jupyter notebooks (`jupynb`)
    - Pipeline runs of software (workflows) and scripts (`pipeline_run`).
    - Physical instruments making measurements (needs to be configured).
    - Human decisions based on data visualizations (needs to be configured).

    It typically has inputs and outputs:

    - References to outputs are stored in the `dobject` table in the
      `dtransform_id` column, which stores a foreign key into the `dtransform`
      table. This is possible as every given `dobject` has a unique data source:
      the `dtransform` that produced the `dobject`. Note that a given
      `dtransform` may output several `dobjects`.
    - References to input `dobjects` are stored in the `dtransform_in` table, a
      many-to-many link table between the `dobject` and `dtransform` tables. Any
      `dobject` might serve as an input for many `dtransform`. Similarly, any
      `dtransform` might have many `dobjects` as inputs.
    """

    __table_args__ = (
        ForeignKeyConstraint(
            ["jupynb_id", "jupynb_v"],
            ["jupynb.id", "jupynb.v"],
            name="dtransform_jupynb",
        ),
    )
    id: str = Field(default_factory=id_dtransform, primary_key=True)
    jupynb_id: Union[str, None] = Field(default=None, index=True)
    jupynb_v: Union[str, None] = Field(default=None, index=True)
    pipeline_run_id: Union[str, None] = Field(
        default=None, foreign_key="pipeline_run.id", index=True
    )


class dtransform_in(SQLModel, table=True):  # type: ignore
    """Input data for data transformations.

    This is a many-to-many link table for `dtransform` and `dobject` storing the
    inputs of data transformations.

    A data transformation can have an arbitrary number of data objects as inputs.

    - The same `dobject` can be used as input in many different `dtransforms`.
    - One `dtransform` can have several `dobjects` as inputs.
    """

    __table_args__ = (
        ForeignKeyConstraint(
            ["dobject_id", "dobject_v"],
            ["dobject.id", "dobject.v"],
            name="dtransform_in_dobject",
        ),
    )
    dtransform_id: str = Field(foreign_key="dtransform.id", primary_key=True)
    dobject_id: str = Field(primary_key=True)
    dobject_v: str = Field(primary_key=True)


class jupynb(SQLModel, table=True):  # type: ignore
    """Jupyter notebooks.

    Jupyter notebooks (`jupynbs`) represent one type of data transformation
    (`dtransform`) and have a unique correspondence in `dtransform`.

    IDs for Jupyter notebooks are generated through nbproject.
    """

    id: str = Field(default=None, primary_key=True)
    v: str = Field(default=None, primary_key=True)
    name: Optional[str] = Field(index=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    time_created: datetime = Field(default_factory=utcnow, nullable=False, index=True)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False, index=True)


class pipeline_run(SQLModel, table=True):  # type: ignore
    """Pipeline runs.

    Pipeline runs represent one type of data transformation (`dtransform`) and
    have a unique correspondence in `dtransform`.

    A pipeline is typically versioned software that can perform a data
    transformation/processing workflow. This can be anything from typical
    workflow tools (Nextflow, snakemake, prefect, Apache Airflow, etc.) to
    simple (versioned) scripts.

    For instance, `lnbfx` stores references to bioinformatics workflow runs by
    linking to entries in this table.
    """

    id: str = Field(default=None, primary_key=True)


# ----------
# Access log
# ----------


class usage_type(str, Enum):
    """Data access types."""

    ingest = "ingest"
    query = "query"
    update = "update"
    delete = "delete"
    load = "load"
    link = "link"


class usage(SQLModel, table=True):  # type: ignore
    """Data usage log.

    Any API call in the `lamindb.do` API is logged here.
    """

    __table_args__ = (
        ForeignKeyConstraint(
            ["dobject_id", "dobject_v"],
            ["dobject.id", "dobject.v"],
            name="usage_dobject",
        ),
    )

    id: Optional[str] = Field(default_factory=id_usage, primary_key=True)
    type: usage_type = Field(nullable=False, index=True)
    user_id: str = Field(foreign_key="user.id", nullable=False, index=True)
    time: datetime = Field(default_factory=utcnow, nullable=False, index=True)
    dobject_id: str = Field(index=True)
    dobject_v: str = Field(index=True)
