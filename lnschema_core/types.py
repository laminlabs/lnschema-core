from __future__ import annotations

from enum import Enum
from typing import List, Union

import numpy as np
import pandas as pd
from django.db.models import CharField, IntegerChoices, TextField  # needed elsewhere
from django.db.models.query_utils import DeferredAttribute as FieldAttr

# need to use Union because __future__.annotations doesn't do the job here <3.10
# typing.TypeAlias, >3.10 on but already deprecated
ListLike = Union[List[str], pd.Series, np.array]
StrField = Union[str, FieldAttr]  # typing.TypeAlias


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
    function = "function"


class VisibilityChoice(IntegerChoices):
    default = 1
    hidden = 0
    trash = -1
