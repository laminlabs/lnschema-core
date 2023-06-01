"""Data lineage (`yvzi`)."""
_schema_id = "yvzi"
_name = "core"
_migration = "1c49c9f9a982"
__version__ = "0.35a1"

import lamindb_setup as _lamindb_setup
from lamindb_setup._check_instance_setup import (
    check_instance_setup as _check_instance_setup,
)

try:
    from lamindb_setup import _USE_DJANGO
except Exception:
    _USE_DJANGO = False

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import dev, link, types

    if not _USE_DJANGO:
        from ._core import (  # type: ignore
            Features,
            File,
            Folder,
            Project,
            Run,
            Storage,
            Transform,
            User,
        )
    else:
        from .models import (  # type: ignore
            Features,
            File,
            Folder,
            Project,
            Run,
            Storage,
            Transform,
            User,
        )
