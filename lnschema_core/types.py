"""Types.

.. autosummary::
   :toctree: .

   PathLike
   DataLike
   TransformType
"""
from enum import Enum
from pathlib import Path
from typing import Any, TypeVar

from upath import UPath

PathLike = TypeVar("PathLike", str, Path, UPath)
# statically typing the following is hard because these are all heavy dependencies, even DataFrame is heavy & slow to import
DataLike = Any


class ChoicesMixin:
    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class TransformType(ChoicesMixin, Enum):
    pipeline = "pipeline"
    notebook = "notebook"
    app = "app"
    api = "api"

    def __repr__(self):
        return self.name
