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
   file
   folder
   run
   transform
   project
   secret
"""
from ._id import (  # noqa
    base26,
    base62,
    base64,
    file,
    folder,
    instance,
    project,
    run,
    schema,
    secret,
    storage,
    transform,
    user,
)

# backward compat
pipeline = transform
notebook = transform
