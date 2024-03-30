from lnschema_core.types import TransformType


def test_transform_type():
    assert TransformType.notebook == "notebook"
    assert TransformType.script == "script"
    assert TransformType.pipeline == "pipeline"
    assert TransformType.upload == "upload"


def test_visibility_choice():
    assert TransformType.default == 1
    assert TransformType.hidden == 0
    assert TransformType.trash == -1
