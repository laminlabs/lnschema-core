from lnschema_core.types import TransformType, VisibilityChoice


def test_transform_type():
    assert TransformType.notebook == "notebook"
    assert TransformType.script == "script"
    assert TransformType.pipeline == "pipeline"
    assert TransformType.upload == "upload"


def test_visibility_choice():
    assert VisibilityChoice.default == 1
    assert VisibilityChoice.hidden == 0
    assert VisibilityChoice.trash == -1
