from __future__ import annotations

from enum import Enum
from typing import List

import numpy as np
import pandas as pd
from django.db.models import CharField, IntegerChoices, TextField  # needed elsewhere
from django.db.models.query_utils import DeferredAttribute as FieldAttr

ListLike = (
    List[str] | pd.Series | np.array
)  # typing.TypeAlias, >3.10 on but already deprecated
StrField = str | FieldAttr  # typing.TypeAlias


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


class TransformType(ChoicesMixin, str, Enum):
    pipeline = "pipeline"
    notebook = "notebook"
    upload = "upload"
    script = "script"


class VisibilityChoice(IntegerChoices):
    default = 1
    hidden = 0
    trash = -1
