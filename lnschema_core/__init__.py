"""Data objects & lineage."""
_schema_id = "yvzi"
_name = "core"
__version__ = "0.43.3"


from lamindb_setup import _check_instance_setup

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import ids, types
    from .models import ORM  # backward compat
    from .models import (  # type: ignore
        Dataset,
        Feature,
        FeatureSet,
        File,
        Label,
        Modality,
        Registry,
        Run,
        Storage,
        Transform,
        User,
    )
