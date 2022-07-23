from datetime import datetime as datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, ForeignKeyConstraint, SQLModel, UniqueConstraint

from .id import id_dobject, id_track


def utcnow():
    return datetime.utcnow().replace(microsecond=0)


class schema_version(SQLModel, table=True):  # type: ignore
    """Schema version."""

    id: Optional[str] = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    time_created: datetime = Field(default_factory=utcnow, nullable=False)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False)


class user(SQLModel, table=True):  # type: ignore
    """Users operating `lamindb`."""

    __table_args__ = (UniqueConstraint("email"),)
    id: Optional[str] = Field(primary_key=True)
    email: str
    time_created: datetime = Field(default_factory=utcnow, nullable=False)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False)


class jupynb(SQLModel, table=True):  # type: ignore
    """Jupyter notebook from which users operate `lamindb`."""

    id: str = Field(default=None, primary_key=True)
    v: str = Field(default=None, primary_key=True)
    name: Optional[str]
    type: str  #: Jupyter notebook (nbproject), pipeline, etc.
    user_id: str = Field(foreign_key="user.id")
    time_created: datetime = Field(default_factory=utcnow, nullable=False)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False)


class dobject(SQLModel, table=True):  # type: ignore
    """Data objects in storage & memory.

    Data objects often correspond to files.

    Storage ⟷ memory examples:
    - `.csv`, `.tsv`, `.feather`, `.parquet` ⟷ `pd.DataFrame`
    - `.h5ad`, `.h5mu`, or their zarr versions ⟷ `anndata.AnnData`, `mudata.MuData`
    - `.jpg`, `.png` ⟷ `np.ndarray`, or a dedicated imaging in-memory container
    - zarr directory ⟷ zarr loader
    - TileDB store ⟷ TileDB loader
    - fastq ⟷ ?
    - .vcf ⟷ ?
    """

    __table_args__ = (
        ForeignKeyConstraint(
            ["jupynb_id", "jupynb_v"],
            ["jupynb.id", "jupynb.v"],
            name="dobject_jupynb",
        ),
    )

    id: Optional[str] = Field(default_factory=id_dobject, primary_key=True)
    v: str = Field(default=None, primary_key=True)
    name: Optional[str]
    file_suffix: str
    jupynb_id: str
    jupynb_v: str
    time_created: datetime = Field(default_factory=utcnow, nullable=False)
    time_updated: datetime = Field(default_factory=utcnow, nullable=False)


# ----------
# Access log
# ----------


class track_do_type(str, Enum):
    """Data access types."""

    ingest = "ingest"
    query = "query"
    update = "update"
    delete = "delete"
    load = "load"


class track_do(SQLModel, table=True):  # type: ignore
    """Data access log: do operations on the database."""

    __table_args__ = (
        ForeignKeyConstraint(
            ["jupynb_id", "jupynb_v"],
            ["jupynb.id", "jupynb.v"],
            name="track_do_jupynb",
        ),
        ForeignKeyConstraint(
            ["dobject_id", "dobject_v"],
            ["dobject.id", "dobject.v"],
            name="track_do_dobject",
        ),
    )

    id: Optional[str] = Field(default_factory=id_track, primary_key=True)
    type: track_do_type = Field(nullable=False)  #: Data access type.
    user_id: str = Field(foreign_key="user.id", nullable=False)
    jupynb_id: str
    jupynb_v: str
    time: datetime = Field(default_factory=utcnow, nullable=False)
    dobject_id: str
    dobject_v: str
