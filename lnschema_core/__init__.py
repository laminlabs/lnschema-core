"""LaminDB's core registries."""

__version__ = "0.64.0"


from lamindb_setup import _check_instance_setup

if _check_instance_setup():
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
