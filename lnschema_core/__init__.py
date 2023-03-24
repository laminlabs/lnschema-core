"""Data lineage (`yvzi`).

.. note::
   Please see the documented API reference `here <https://lamin.ai/docs/db/lamindb.schema>`__.

   This page just provides a list of entities.

Import the package::

   import lnschema_core

Entities:

.. autosummary::
   :toctree: .

   File
   Run
   Transform
   Folder
   User
   Storage
   Project
   Features

Development tools:

.. autosummary::
   :toctree: .

   dev
   link
"""
_schema_id = "yvzi"
_name = "core"
_migration = "5846a15d9241"
__version__ = "0.30rc3"

from . import dev, link
from ._core import Features, File, Folder, Project, Run, Storage, Transform, User

# backward compat
DObject = File
DFolder = Folder
