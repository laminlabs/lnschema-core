"""IDs.

See: https://github.com/laminlabs/lamin-notes/blob/main/docs/2022/ids.ipynb

Base generators:

.. autosummary::
   :toctree: .

   base26
   base62
   base64

Entity-related generators:

.. autosummary::
   :toctree: .

   schema
   user
   instance
   storage
   dobject
   run
   usage
   jupynb
   pipeline
   project
   secret
"""
from ._id import (  # noqa
    base26,
    base62,
    base64,
    dobject,
    dset,
    instance,
    jupynb,
    pipeline,
    project,
    run,
    schema,
    secret,
    storage,
    usage,
    user,
)

id_base62 = base62  # backward compat
id_base26 = base26  # backward compat
id_schema_module = schema  # backward compat
id_dobject = dobject  # backward compat
id_run = run  # backward compat
id_user = user  # backward compat
id_usage = usage  # backward compat
id_secret = secret  # backward compat
id_instance = instance  # backward compat
id_storage = storage  # backward compat
