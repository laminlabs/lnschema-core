from __future__ import annotations

from enum import Enum
from typing import List, Literal, Union

import numpy as np
import pandas as pd
from django.db.models import IntegerChoices  # needed elsewhere
from django.db.models.query_utils import DeferredAttribute as FieldAttr

# need to use Union because __future__.annotations doesn't do the job here <3.10
# typing.TypeAlias, >3.10 on but already deprecated
ListLike = Union[List[str], pd.Series, np.array]
StrField = Union[str, FieldAttr]  # typing.TypeAlias

TransformType = Literal["pipeline", "notebook", "upload", "script", "function", "glue"]
ArtifactType = Literal["dataset", "model"]


class VisibilityChoice(IntegerChoices):
    default = 1
    hidden = 0
    trash = -1
