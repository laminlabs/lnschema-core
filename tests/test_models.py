import re
import textwrap

# The tests defined in this script use the lamindb instance defined in test_integrity


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from a string."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def test_registry__repr__param(setup_instance):
    import lnschema_core.models as ln

    param = ln.Param
    expected_repr = textwrap.dedent("""\
    Param
      Basic fields
        .id: BigAutoField
        .name: CharField
        .dtype: CharField
        .created_at: DateTimeField
        .updated_at: DateTimeField
      Relational fields
        .created_by: User
        .run: Run
        .previous_runs: Run
        .paramvalue: ParamValue
    """).strip()

    actual_repr = _strip_ansi(repr(param))
    assert actual_repr.strip() == expected_repr.strip()


def test_registry__repr__artifact(setup_instance):
    import lnschema_core.models as ln

    artifact = ln.Artifact
    expected_repr = textwrap.dedent("""\
    Artifact
      Basic fields
        .id: AutoField
        .uid: CharField
        .description: CharField
        .key: CharField
        .suffix: CharField
        .type: CharField
        .accessor: CharField
        .size: BigIntegerField
        .hash: CharField
        .hash_type: CharField
        .n_objects: BigIntegerField
        .n_observations: BigIntegerField
        .visibility: SmallIntegerField
        .key_is_virtual: BooleanField
        .version: CharField
        .created_at: DateTimeField
        .updated_at: DateTimeField
      Relational fields
        .created_by: User
        .storage: Storage
        .transform: Transform
        .run: Run
        .ulabels: ULabel
        .input_of: Run
        .previous_runs: Run
        .feature_sets: FeatureSet
        .feature_values: FeatureValue
        .param_values: ParamValue
        .latest_report_of: Transform
        .source_code_of: Transform
        .report_of: Run
        .environment_of: Run
        .collection: Collection
        .collections: Collection
    """).strip()

    actual_repr = _strip_ansi(repr(artifact))
    assert actual_repr.strip() == expected_repr.strip()
