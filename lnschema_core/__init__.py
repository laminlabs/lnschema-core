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

Tracking migrations:

.. autosummary::
   :toctree: .

   version_yvzi

Auxiliary modules:

.. autosummary::
   :toctree: .

   type
   id

"""
# This is lnschema-module yvzi.
_schema_module_id = "yvzi"
__version__ = "0.5.1"  # denote a pre-release for 0.1.0 with 0.1a1

from . import id, type  # noqa
from ._core import (  # noqa
    dobject,
    dtransform,
    dtransform_in,
    jupynb,
    pipeline,
    pipeline_run,
    storage,
    usage,
    usage_type,
    user,
    version_yvzi,
)
