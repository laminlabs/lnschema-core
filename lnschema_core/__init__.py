"""Data lineage (`yvzi`)."""
_schema_id = "yvzi"
_name = "core"
_migration = "c3f38ffe9e03"
__version__ = "0.34a2"

from lndb._check_instance_setup import check_instance_setup as _check_instance_setup

_INSTANCE_SETUP = _check_instance_setup()
_USE_DJANGO: bool = False

if _INSTANCE_SETUP:
    from . import dev, link, types

    if not _USE_DJANGO:
        from ._core import (
            Features,
            File,
            Folder,
            Project,
            Run,
            Storage,
            Transform,
            User,
        )
