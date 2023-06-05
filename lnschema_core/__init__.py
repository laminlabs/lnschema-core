"""Data objects & lineage (`yvzi`)."""
_schema_id = "yvzi"
_name = "core"
__version__ = "0.35a4"

import lamindb_setup as _lamindb_setup
from lamindb_setup._check_instance_setup import (
    check_instance_setup as _check_instance_setup,
)

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import ids, types
    from .models import (  # type: ignore
        BaseORM,
        Featureset,
        File,
        Folder,
        Project,
        Run,
        RunInput,
        Storage,
        Transform,
        User,
    )

    Features = Featureset  # backward compat
