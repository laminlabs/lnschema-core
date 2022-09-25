"""Schema module core (`yvzi`).

Import the package::

   import lnschema_core

Main tables:

.. autosummary::
   :toctree: .

   dobject
   dtransform
   dtransform_in
   user
   usage

Data transformations:

.. autosummary::
   :toctree: .

   jupynb
   pipeline
   pipeline_run

Tracking versions & migrations:

.. autosummary::
   :toctree: .

   version_yvzi
   migration_yvzi

Auxiliary modules:

.. autosummary::
   :toctree: .

   type
   id

"""
# This is lnschema-module yvzi.
_schema_id = "yvzi"
_migration = "7e8f7b30792e"
__version__ = "0.8.0"  # denote a pre-release for 0.1.0 with 0.1a1

from . import id, type  # noqa
from ._core import (  # noqa
    dobject,
    dtransform,
    dtransform_in,
    jupynb,
    migration_yvzi,
    pipeline,
    pipeline_run,
    storage,
    usage,
    usage_type,
    user,
    version_yvzi,
)
