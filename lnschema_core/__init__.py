"""Data objects & lineage (`yvzi`)."""
_schema_id = "yvzi"
_name = "core"
__version__ = "0.36.1"

# can directly import from lamindb_setup going forward
from lamindb_setup._check_instance_setup import (
    check_instance_setup as _check_instance_setup,
)

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import ids, types
    from .models import (  # type: ignore
        BaseORM,
        FeatureSet,
        File,
        Project,
        Run,
        Storage,
        Tag,
        Transform,
        User,
    )

    Features = FeatureSet  # backward compat
