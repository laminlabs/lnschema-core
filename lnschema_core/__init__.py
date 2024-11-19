"""LaminDB's core registries."""

__version__ = "0.77.0"


from lamindb_setup import _check_instance_setup

if _check_instance_setup():
    from . import ids, types, validation
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

    # backward compatibility
    CanValidate = CanCurate
