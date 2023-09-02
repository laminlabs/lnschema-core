"""LaminDB's core registries."""
_schema_id = "yvzi"
_name = "core"
__version__ = "0.46.5"


from lamindb_setup import _check_instance_setup

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import ids, types
    from .models import ORM  # backward compat
    from .models import (  # type: ignore
        CanValidate,
        Dataset,
        Feature,
        FeatureSet,
        File,
        HasParents,
        Label,
        Modality,
        Registry,
        Run,
        Storage,
        Transform,
        User,
    )
