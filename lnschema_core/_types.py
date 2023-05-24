from enum import Enum
from pathlib import Path
from typing import Callable, TypeVar

import anndata as ad
import numpy as np
import pandas as pd
from lndb.dev.upath import UPath
from sqlalchemy.orm.attributes import InstrumentedAttribute

PathLike = TypeVar("PathLike", str, Path, UPath)
DataLike = TypeVar("DataLike", ad.AnnData, pd.DataFrame)
ListLike = TypeVar("ListLike", pd.Series, list, np.array)
SQLModelField = TypeVar("SQLModelField", Callable, InstrumentedAttribute)


class Usage(str, Enum):
    """Data access types."""

    ingest = "ingest"
    insert = "insert"
    select = "select"
    update = "update"
    delete = "delete"
    load = "load"
    link = "link"


class TransformType(Enum):
    pipeline = "pipeline"
    notebook = "notebook"
    app = "app"

    def __repr__(self):
        return self.name

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]
