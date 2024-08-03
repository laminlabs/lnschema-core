"""LaminDB's core registries."""

__version__ = "0.72.1"


from lamindb_setup import _check_instance_setup

if _check_instance_setup():
    from . import ids, types
    from .models import (  # type: ignore
        Artifact,
        CanValidate,
        Collection,
        Feature,
        FeatureSet,
        HasParents,
        Record,
        Run,
        Storage,
        Transform,
        ULabel,
        User,
    )
