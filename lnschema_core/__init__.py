"""LaminDB's core registries."""

__version__ = "0.61.1"


from lamindb_setup import _check_instance_setup

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import ids, types
    from .models import ORM  # backward compat
    from .models import (  # type: ignore
        Artifact,
        CanValidate,
        Collection,
        Feature,
        FeatureSet,
        HasParents,
        Registry,
        Run,
        Storage,
        Transform,
        ULabel,
        User,
    )
