from datetime import datetime as datetime
from enum import Enum
from typing import Optional, Union

from sqlmodel import Field, ForeignKeyConstraint, SQLModel, UniqueConstraint

from .id import id_dobject, id_dtransform, id_usage


def utcnow():
    return datetime.utcnow().replace(microsecond=0)


class version_yvzi(SQLModel, table=True):  # type: ignore
    """Schema module version."""

    v: Optional[str] = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    time_created: datetime = Field(default_factory=utcnow, nullable=False)


class user(SQLModel, table=True):  # type: ignore
    """Users operating a given LaminDB instance."""

    __table_args__ = (
        UniqueConstraint("email"),
        UniqueConstraint("handle"),
    )
    id: Optional[str] = Field(primary_key=True)
    email: str
    handle: str = Field(nullable=False)
    time_created: datetime = Field(default_factory=utcnow, nullable=False)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False)


class dobject(SQLModel, table=True):  # type: ignore
    """Data objects in storage & memory.

    Storage ⟷ memory examples:

    - Table: `.csv`, `.tsv`, `.feather`, `.parquet` ⟷ `pd.DataFrame`
    - Annotated matrix: `.h5ad`, `.h5mu`, `.zarrad` ⟷ `anndata.AnnData`, `mudata.MuData`
    - Image: `.jpg`, `.png` ⟷ `np.ndarray`, or a dedicated imaging in-memory container
    - Tensor: zarr directory, TileDB store ⟷ zarr loader, TileDB loader
    - Fastq: fastq ⟷ /
    - VCF: .vcf ⟷ /
    """

    id: Optional[str] = Field(default_factory=id_dobject, primary_key=True)
    v: str = Field(default=None, primary_key=True)
    name: Optional[str]
    file_suffix: str
    dsource_id: str = Field(foreign_key="dtransform.id")
    time_created: datetime = Field(default_factory=utcnow, nullable=False)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False)


class dtransform(SQLModel, table=True):  # type: ignore
    """Data transformations."""

    __table_args__ = (
        ForeignKeyConstraint(
            ["jupynb_id", "jupynb_v"],
            ["jupynb.id", "jupynb.v"],
            name="dtransform_jupynb",
        ),
        ForeignKeyConstraint(
            ["pipeline_id", "pipeline_v"],
            ["pipeline.id", "pipeline.v"],
            name="dtransform_pipeline",
        ),
    )
    id: str = Field(default_factory=id_dtransform, primary_key=True)
    jupynb_id: Union[str, None] = None
    jupynb_v: Union[str, None] = None
    pipeline_id: Union[str, None] = None
    pipeline_v: Union[str, None] = None


class dtransform_in(SQLModel, table=True):  # type: ignore
    """Inputs - link dtransform & dobject."""

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


class dtransform_out(SQLModel, table=True):  # type: ignore
    """Outputs - link dtransform & dobject."""

    __table_args__ = (
        ForeignKeyConstraint(
            ["dobject_id", "dobject_v"],
            ["dobject.id", "dobject.v"],
            name="dtransform_out_dobject",
        ),
    )
    dtransform_id: str = Field(foreign_key="dtransform.id", primary_key=True)
    dobject_id: str = Field(primary_key=True)
    dobject_v: str = Field(primary_key=True)


class jupynb(SQLModel, table=True):  # type: ignore
    """Jupyter notebooks."""

    id: str = Field(default=None, primary_key=True)
    v: str = Field(default=None, primary_key=True)
    name: Optional[str]
    user_id: str = Field(foreign_key="user.id")
    time_created: datetime = Field(default_factory=utcnow, nullable=False)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False)


class pipeline(SQLModel, table=True):  # type: ignore
    """Pipelines."""

    id: str = Field(default=None, primary_key=True)
    v: str = Field(default=None, primary_key=True)


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
    """Data usage log: do operations on the database."""

    __table_args__ = (
        ForeignKeyConstraint(
            ["dobject_id", "dobject_v"],
            ["dobject.id", "dobject.v"],
            name="usage_dobject",
        ),
    )

    id: Optional[str] = Field(default_factory=id_usage, primary_key=True)
    type: usage_type = Field(nullable=False)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    time: datetime = Field(default_factory=utcnow, nullable=False)
    dobject_id: str
    dobject_v: str
