"""Data lineage (`yvzi`)."""
_schema_id = "yvzi"
_name = "core"
_migration = "1c49c9f9a982"
__version__ = "0.35a1"

from lndb._check_instance_setup import check_instance_setup as _check_instance_setup

import lndb as _lndb

try:
    from lndb import _USE_DJANGO
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
