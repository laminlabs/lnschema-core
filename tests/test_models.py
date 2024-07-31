import lamindb as ln


def test_registry__repr__param():
    param = ln.Param
    repr_string = repr(param)

    # Header
    assert "Param" in repr_string

    # Basic fields
    assert ".id: BigAutoField" in repr_string
    assert ".name: CharField" in repr_string
    assert ".dtype: CharField" in repr_string
    assert ".created_at: DateTimeField" in repr_string
    assert ".updated_at: DateTimeField" in repr_string

    # Relational fields
    assert ".created_by: User" in repr_string
    assert ".run: Run" in repr_string
    assert ".previous_runs: Run" in repr_string
    assert ".paramvalue: ParamValue" in repr_string


def test_registry__repr__artifact():
    artifact = ln.Artifact
    repr_string = repr(artifact)

    # Header
    assert "Artifact" in repr_string

    # Basic fields
    assert ".id: AutoField" in repr_string
    assert ".uid: CharField" in repr_string
    assert ".description: CharField" in repr_string
    assert ".key: CharField" in repr_string
    assert ".suffix: CharField" in repr_string
    assert ".type: CharField" in repr_string
    assert ".accessor: CharField" in repr_string
    assert ".size: BigIntegerField" in repr_string
    assert ".hash: CharField" in repr_string
    assert ".hash_type: CharField" in repr_string
    assert ".n_objects: BigIntegerField" in repr_string
    assert ".n_observations: BigIntegerField" in repr_string
    assert ".visibility: SmallIntegerField" in repr_string
    assert ".key_is_virtual: BooleanField" in repr_string
    assert ".version: CharField" in repr_string
    assert ".created_at: DateTimeField" in repr_string
    assert ".updated_at: DateTimeField" in repr_string

    # Relational fields
    assert ".created_by: User" in repr_string
    assert ".storage: Storage" in repr_string
    assert ".transform: Transform" in repr_string
    assert ".run: Run" in repr_string
    assert ".ulabels: ULabel" in repr_string
    assert ".input_of: Run" in repr_string
    assert ".previous_runs: Run" in repr_string
    assert ".feature_sets: FeatureSet" in repr_string
    assert ".feature_values: FeatureValue" in repr_string
    assert ".param_values: ParamValue" in repr_string
    assert ".latest_report_of: Transform" in repr_string
    assert ".source_code_of: Transform" in repr_string
    assert ".report_of: Run" in repr_string
    assert ".environment_of: Run" in repr_string
    assert ".collection: Collection" in repr_string
    assert ".collections: Collection" in repr_string

    # Bionty fields
    assert ".organisms: bionty.Organism" in repr_string
    assert ".genes: bionty.Gene" in repr_string
    assert ".proteins: bionty.Protein" in repr_string
    assert ".cell_markers: bionty.CellMarker" in repr_string
    assert ".tissues: bionty.Tissue" in repr_string
    assert ".cell_types: bionty.CellType" in repr_string
    assert ".diseases: bionty.Disease" in repr_string
    assert ".cell_lines: bionty.CellLine" in repr_string
    assert ".phenotypes: bionty.Phenotype" in repr_string
    assert ".pathways: bionty.Pathway" in repr_string
    assert ".experimental_factors: bionty.ExperimentalFactor" in repr_string
    assert ".developmental_stages: bionty.DevelopmentalStage" in repr_string
    assert ".ethnicities: bionty.Ethnicity" in repr_string
    assert ".reference_of_source: bionty.Source" in repr_string
    assert ".reference_of_sources: bionty.Source" in repr_string
