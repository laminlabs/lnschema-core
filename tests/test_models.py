import textwrap

import lamindb as ln


def test_registry__repr__param():
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

    assert repr(param) == expected_repr


def test_registry__repr__artifact():
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

    # TODO these fields should also be tested for but they require an instance with Bionty
    """
      Bionty fields
        .organisms: bionty.Organism
        .genes: bionty.Gene
        .proteins: bionty.Protein
        .cell_markers: bionty.CellMarker
        .tissues: bionty.Tissue
        .cell_types: bionty.CellType
        .diseases: bionty.Disease
        .cell_lines: bionty.CellLine
        .phenotypes: bionty.Phenotype
        .pathways: bionty.Pathway
        .experimental_factors: bionty.ExperimentalFactor
        .developmental_stages: bionty.DevelopmentalStage
        .ethnicities: bionty.Ethnicity
        .reference_of_source: bionty.Source
        .reference_of_sources: bionty.Source
    """

    assert repr(artifact) == expected_repr
