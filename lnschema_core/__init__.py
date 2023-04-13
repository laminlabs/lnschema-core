"""Data lineage (`yvzi`)."""
_schema_id = "yvzi"
_name = "core"
_migration = "d161a14a12e3"
__version__ = "0.32.2"

from lndb._check_instance_setup import check_instance_setup as _check_instance_setup

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import dev, link
    from ._core import Features, File, Folder, Project, Run, Storage, Transform, User

    # backward compat
    DObject = File
    DFolder = Folder
