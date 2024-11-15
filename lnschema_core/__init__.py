"""LaminDB's core registries."""

__version__ = "0.76.2"


from lamindb_setup import _check_instance_setup

if _check_instance_setup():
    from . import ids, types
    from .models import (  # type: ignore
        Artifact,
        CanCurate,
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
