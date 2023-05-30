"""Data lineage (`yvzi`)."""
_schema_id = "yvzi"
_name = "core"
_migration = "1c49c9f9a982"
__version__ = "0.34.0"

from lndb._check_instance_setup import check_instance_setup as _check_instance_setup

import lndb as _lndb
from lndb import _USE_DJANGO

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import dev, link, types

    if not _USE_DJANGO:
        from lndb.dev._django import setup_django

        setup_django(_lndb.settings.instance)

        from .models import (
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
