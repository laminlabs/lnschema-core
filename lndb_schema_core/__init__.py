"""Schema module core (`yvzi`).

Import the package::

   import lndb_schema_core

This is the complete API reference:

.. autosummary::
   :toctree: .

   dobject
   dtransform
   dtransform_in
   dtransform_out
   jupynb
   version_yvzi
   track_do
   track_do_type
   user

"""
# This is lndb-schema-module yvzi.
_schema_module_id = "yvzi"
__version__ = "0.2.1"  # denote a pre-release for 0.1.0 with 0.1a1

from . import id
from ._core import (  # noqa
    dobject,
    dtransform,
    dtransform_in,
    dtransform_out,
    jupynb,
    track_do,
    track_do_type,
    user,
    version_yvzi,
)
