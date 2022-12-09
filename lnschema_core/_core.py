import base64
import hashlib
from datetime import datetime as datetime
from pathlib import Path
from typing import Any, List, Optional, Set, Tuple, Union, overload  # noqa

import anndata as ad
import pandas as pd
import sqlalchemy as sa
from cloudpathlib import CloudPath
from lamin_logger import logger
from pydantic.fields import PrivateAttr
from sqlmodel import Field, ForeignKeyConstraint, Relationship
from sqlmodel import SQLModel as SQLModelPublicSchema

from . import _name as schema_name
from ._link import DObjectFeatures, DSetDObject, ProjectDSet, RunIn  # noqa
from ._timestamps import CreatedAt, UpdatedAt
from ._users import CreatedBy
from .dev import id as idg
from .dev._storage import filepath_from_dobject
from .dev.sqlmodel import schema_sqlmodel
from .dev.type import usage as usage_type

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


def serialize(
    data: Union[Path, str, pd.DataFrame, ad.AnnData], name, format
) -> Tuple[Any, Path, str, str]:
    """Serialize a data object that's provided as file or in memory."""
    from lamindb.dev._core import get_name_suffix_from_filepath
    from lamindb.dev.object import infer_suffix, write_to_file

    memory_rep = None
    if isinstance(data, (Path, str)):
        local_filepath = Path(data)
        name, suffix = get_name_suffix_from_filepath(local_filepath)
    elif isinstance(data, (pd.DataFrame, ad.AnnData)):
        if name is None:
            raise RuntimeError("Provide name if recording in-memory data.")
        memory_rep = data
        suffix = infer_suffix(data, format)
        local_filepath = Path(f"{name}{suffix}")
        if suffix != ".zarr":
            write_to_file(data, local_filepath)
    else:
        raise NotImplementedError("Recording not yet implemented for this type.")
    return memory_rep, local_filepath, name, suffix


def get_features_records(
    parsing_id: str,
    features_ref: Any,
    df_curated: pd.DataFrame,
) -> List[Any]:
    # insert species entry if not exists
    import lnschema_bionty as bionty
    from lamindb import add, select
    from lamindb.schema._table import table_meta

    species = select(bionty.Species, common_name=features_ref.species).one_or_none()
    if species is None:
        species = add(bionty.Species(common_name=features_ref.species))

    model = table_meta.get_model(f"bionty.{features_ref.entity}")

    # all existing feature records of the species in the db
    stmt = (
        select(model)
        .where(getattr(model, parsing_id).in_(df_curated.index))
        .where(getattr(model, "species_id") == species.id)
    )
    records = stmt.all()
    records_df = df_curated.index.intersection(stmt.df()[parsing_id])

    # new records to be appended
    new_ids = df_curated.index.difference(records_df)
    if len(new_ids) > 0:
        # mapped new_ids
        mapped = features_ref.df.loc[features_ref.df.index.intersection(new_ids)].copy()
        mapped.index.name = parsing_id
        if mapped.shape[0] > 0:
            for kwargs in mapped.reset_index().to_dict(orient="records"):
                kwargs["species_id"] = species.id
                record = model(**kwargs)
                records.append(record)
        # unmapped new_ids
        unmapped = set(new_ids).difference(mapped.index)
        if len(unmapped) > 0:
            for i in unmapped:
                record = model(**{parsing_id: i, "species_id": species.id})
                records.append(record)

    return records


def create_dobject_from_data(
    data: Union[Path, str, pd.DataFrame, ad.AnnData],
    *,
    name: Optional[str] = None,
    features_ref: Any = None,
    source: Optional["Run"] = None,
    id: Optional[str] = None,
    format: Optional[str] = None,
):
    """Record a data object.

    Guide: :doc:`/db/guide/ingest`.

    Args:
        data: Filepath or in-memory data.
        name: Name of the data object, required if an in-memory object is passed.
        features_ref: Reference against which to link features.
        source: The data transform that links to the data source of the data object.
        id: The id of the dobject.
        format: Whether to use `h5ad` or `zarr` to store an `AnnData` object.
    """
    from lamindb import select, settings
    from lamindb.dev.object import size_adata

    run = get_run(source)
    memory_rep, local_filepath, name, suffix = serialize(data, name, format)
    if suffix != ".zarr":
        size = Path(local_filepath).stat().st_size
    else:
        size = size_adata(memory_rep)
    hash = get_hash(local_filepath, suffix)
    storage = select(Storage, root=str(settings.instance.storage_root)).one()
    dobject = DObject(  # type: ignore
        name=name,
        suffix=suffix,
        hash=hash,
        run_id=run.id,
        size=size,
        storage_id=storage.id,
        source=run,
    )
    if id is not None:  # cannot pass it into constructor due to default factory
        dobject.id = id
    dobject._local_filepath = local_filepath
    dobject._memory_rep = memory_rep
    if features_ref is not None:
        dobject.features.append(get_features(dobject, features_ref))
    return dobject


def get_run(run: Optional["Run"]) -> "Run":
    if run is None:
        from lamindb._nb import _run

        run = _run
        if run is None:
            raise ValueError("Pass a Run record.")
    return run


def parse_features(df: pd.DataFrame, features_ref: Any) -> None:
    """Link features to a knowledge table.

    Args:
        df: a DataFrame
        features_ref: Features reference class.
    """
    from lamindb import select
    from lamindb.knowledge import CellMarker, Gene, Protein

    parsing_id = features_ref._id_field

    # Add and curate features against a knowledge table
    column = None
    if parsing_id in df.columns:
        column = parsing_id
    else:
        logger.warning(f"{parsing_id} column not found, using index as features.")
    df_curated = features_ref.curate(df=df, column=column)

    # logging of curation
    n = df_curated["__curated__"].count()
    n_mapped = df_curated["__curated__"].sum()
    log = {  # noqa  TODO: store this somewhere in the db
        "feature": parsing_id,
        "n_mapped": n_mapped,
        "percent_mapped": round(n_mapped / n * 100, 1),
        "unmapped": df_curated.index[~df_curated["__curated__"]],
    }

    features_hash = hash_set(set(df_curated.index))

    features = select(
        Features,
        id=features_hash,
        type=features_ref.entity,
    ).one_or_none()
    if features is not None:
        return features  # features already exists!

    features = Features(id=features_hash, type=features_ref.entity)
    records = get_features_records(parsing_id, features_ref, df_curated)

    if isinstance(features_ref, Gene):
        for record in records:
            features.genes.append(record)
    elif isinstance(features_ref, Protein):
        for record in records:
            features.proteins.append(record)
    elif isinstance(features_ref, CellMarker):
        for record in records:
            features.cell_markers.append(record)

    return features


def get_features(dobject, features_ref):
    """Updates dobject in place."""
    from lamindb.dev.file import load_to_memory

    memory_rep = dobject._memory_rep
    if memory_rep is None:
        memory_rep = load_to_memory(dobject._local_filepath)
    try:
        df = getattr(memory_rep, "var")  # for AnnData objects
        if callable(df):
            df = memory_rep
    except AttributeError:
        df = memory_rep
    return parse_features(df, features_ref)


def get_hash(local_filepath, suffix):
    from lamindb import select

    if suffix != ".zarr":  # if not streamed
        hash = hash_file(local_filepath)
        result = select(DObject, hash=hash).one_or_none()
        if result is not None:
            logger.warning(
                "Based on the MD5 hash, the same data object is already"
                f" in the DB: {result}"
            )
    else:
        hash = None
    return hash


def hash_file(path: Path) -> str:
    # based on https://stackoverflow.com/questions/3431825/generating-an-md5-hash-of-a-file  # noqa
    hash_md5 = hashlib.md5()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return to_b64_str(hash_md5.digest())


def to_b64_str(bstr: bytes):
    b64 = base64.urlsafe_b64encode(bstr).decode().strip("=")
    return b64


# a lot to read about this: lamin-notes/2022/hashing
def hash_set(s: Set[str]) -> str:
    bstr = ":".join(sorted(s)).encode("utf-8")
    # as we're truncating at 20 b64, we choose md5 over sha512
    return to_b64_str(hashlib.md5(bstr).digest())[:20]


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


class Storage(SQLModelPublicSchema, table=True):  # type: ignore
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
    """Datasets, collections of data objects.

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

    size: Optional[int] = Field(
        default=None, sa_column=sa.Column(sa.BigInteger(), index=True)
    )
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    hash: Optional[str] = Field(default=None, index=True)
    """Hash (md5)."""

    # We need the fully module-qualified path below, as there might be more
    # schema modules with an ORM called "Run"
    source: "lnschema_core._core.Run" = Relationship(  # type: ignore  # noqa
        back_populates="output"
    )
    """Link to :class:`~lnschema_core.Run` that generated the `dobject`."""
    run_id: str = Field(foreign_key="core.run.id", index=True)
    """The source run id."""
    storage_id: str = Field(foreign_key="storage.id", index=True)
    """The id of :class:`~lnschema_core.Storage` location that stores the `dobject`."""
    features: List["Features"] = Relationship(
        back_populates="dobjects",
        sa_relationship_kwargs=dict(secondary=DObjectFeatures.__table__),
    )
    """Link to feature sets."""
    targets: List["lnschema_core._core.Run"] = Relationship(  # type: ignore  # noqa
        back_populates="input",
        sa_relationship_kwargs=dict(secondary=RunIn.__table__),
    )
    "Runs that use this dobject as input."
    created_at: datetime = CreatedAt
    """Time of creation."""
    updated_at: Optional[datetime] = UpdatedAt
    """Time of last update."""

    # private attributes
    _local_filepath: Path = PrivateAttr()
    _memory_rep: Path = PrivateAttr()

    def path(self) -> Union[Path, CloudPath]:
        """Path on storage."""
        return filepath_from_dobject(self)

    @overload
    def __init__(
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        *,
        name: Optional[str] = None,
        features_ref: Any = None,
        source: Optional["Run"] = None,
        id: Optional[str] = None,
        format: Optional[str] = None,
    ):
        """Create a DObject record from data."""
        ...

    @overload
    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        source: Optional["Run"] = None,
        suffix: Optional[str] = None,
        hash: Optional[str] = None,
        run_id: Optional[str] = None,
        storage_id: Optional[str] = None,
        features: List["Features"] = [],
        targets: List["Run"] = [],
    ):
        """Create a DObject record from fields."""
        ...

    def __init__(  # type: ignore
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        *,
        features_ref: Any = None,
        source: Optional["Run"] = None,
        format: Optional[str] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        suffix: Optional[str] = None,
        hash: Optional[str] = None,
        run_id: Optional[str] = None,
        storage_id: Optional[str] = None,
        features: List["Features"] = [],
        targets: List["Run"] = [],
    ):
        kwargs = locals()
        if data is not None:
            record = create_dobject_from_data(
                data=data,
                name=name,
                features_ref=features_ref,
                source=source,
                id=id,
                format=format,
            )
            kwargs = record.dict()

        super().__init__(**kwargs)


class Run(SQLModel, table=True):  # type: ignore
    """Code runs that transform data.

    A data transformation (`run`) is _any_ transformation of a `dobject`.

    For instance:

    - Jupyter notebooks (`notebook`)
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
            ["notebook_id", "notebook_v"],
            ["core.notebook.id", "core.notebook.v"],
        ),
        {"schema": schema_arg},
    )
    id: str = Field(default_factory=idg.run, primary_key=True)
    """Universal base62 ID & primary key, generated through :func:`~lnschema_core.dev.id.run`."""  # noqa
    name: Optional[str] = Field(default=None, index=True)
    pipeline_id: Optional[str] = Field(default=None, index=True)
    pipeline_v: Optional[str] = Field(default=None, index=True)
    pipeline: Optional["lnschema_core._core.Pipeline"] = Relationship()  # type: ignore # noqa
    """Link to :class:`~lnschema_core.Pipeline`."""
    notebook_id: Optional[str] = Field(default=None, index=True)
    notebook_v: Optional[str] = Field(default=None, index=True)
    notebook: Optional["Notebook"] = Relationship()
    """Link to :class:`~lnschema_core.Notebook`."""
    output: List["DObject"] = Relationship(back_populates="source")
    """Output data :class:`~lnschema_core.DObject`."""
    input: List["DObject"] = Relationship(
        back_populates="targets", sa_relationship_kwargs=dict(secondary=RunIn.__table__)
    )
    """Input data :class:`~lnschema_core.DObject`."""
    created_by: str = CreatedBy
    """Auto-populated link to :class:`~lnschema_core.User`."""
    created_at: datetime = CreatedAt
    """Time of creation."""


class Notebook(SQLModel, table=True):  # type: ignore
    """Jupyter notebooks.

    Jupyter notebooks (`notebooks`) represent one type of data transformation
    (`run`) and have a unique correspondence in `run`.

    IDs for Jupyter notebooks are generated through nbproject.
    """

    id: str = Field(default=None, primary_key=True)
    """Universal base62 ID & primary key, generated by :func:`~lnschema_core.dev.id.notebook`."""  # noqa
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
