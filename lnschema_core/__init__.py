"""Data objects & lineage (`yvzi`)."""
_schema_id = "yvzi"
_name = "core"
__version__ = "0.37.0"


from lamindb_setup import _check_instance_setup

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import ids, types
    from .models import (  # type: ignore
        ORM,
        Dataset,
        Feature,
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
