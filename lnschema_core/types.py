from enum import Enum
from typing import TYPE_CHECKING, Any, TypeVar

from django.db.models import CharField, IntegerChoices, TextField  # noqa
from django.db.models.query_utils import DeferredAttribute as FieldAttr  # noqa

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd


# statically typing the following is hard because these are all heavy
# dependencies, even DataFrame is heavy & slow to import
DataLike = Any
AnnDataLike = Any
ListLike = TypeVar("ListLike", list, "pd.Series", "np.array")
StrField = TypeVar("StrField", str, FieldAttr)


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
    upload = "upload"
    script = "script"


class VisibilityChoice(IntegerChoices):
    default = 1
    hidden = 0
    trash = -1
