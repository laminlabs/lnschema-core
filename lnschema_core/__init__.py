"""LaminDB's core registries."""

__version__ = "0.74.5"


from lamindb_setup import _check_instance_setup


def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="lnschema_core")
    return globals()[name]


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
