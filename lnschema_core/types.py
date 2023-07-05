from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

from django.db.models import CharField, TextField
from upath import UPath

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd

PathLike = TypeVar("PathLike", str, Path, UPath)
# statically typing the following is hard because these are all heavy
# dependencies, even DataFrame is heavy & slow to import
DataLike = Any
AnnDataLike = Any
ListLike = TypeVar("ListLike", "pd.Series", list, "np.array")
StrField = TypeVar("StrField", str, CharField, TextField)


class ChoicesMixin:
    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

    # needs to mix with Enum
    def __repr__(self):
        return self.value

    # needs to mix with Enum
    def __str__(self):
        return self.value


class TransformType(ChoicesMixin, Enum):
    pipeline = "pipeline"
    notebook = "notebook"
    app = "app"
    api = "api"
