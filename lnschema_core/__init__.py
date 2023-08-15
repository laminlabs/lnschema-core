"""LaminDB's core registries."""
_schema_id = "yvzi"
_name = "core"
__version__ = "0.45.3"


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
        ParentsAware,
        Registry,
        Run,
        Storage,
        SynonymsAware,
        Transform,
        User,
        ValidationAware,
    )
