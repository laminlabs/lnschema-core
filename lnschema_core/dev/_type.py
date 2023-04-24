from enum import Enum
from pathlib import Path
from typing import TypeVar

import anndata as ad
import pandas as pd
from lndb.dev.upath import UPath

PathLike = TypeVar("PathLike", str, Path, UPath)
DataLike = TypeVar("DataLike", ad.AnnData, pd.DataFrame)


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
