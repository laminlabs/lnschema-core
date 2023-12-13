# Generated by Django 4.2.5 on 2023-12-09 09:04

import django.db.models.deletion
import lamindb_setup
from django.db import migrations, models

import lnschema_core.models
import lnschema_core.users


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0030_alter_dataset_visibility_alter_file_visibility"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="File",
            new_name="Artifact",
        ),
        migrations.RenameModel(
            old_name="FileFeatureSet",
            new_name="ArtifactFeatureSet",
        ),
        migrations.RenameModel(
            old_name="FileULabel",
            new_name="ArtifactULabel",
        ),
        migrations.RenameField(
            model_name="artifactfeatureset",
            old_name="file",
            new_name="artifact",
        ),
        migrations.RenameField(
            model_name="dataset",
            old_name="file",
            new_name="artifact",
        ),
        migrations.RenameField(
            model_name="dataset",
            old_name="files",
            new_name="artifacts",
        ),
        migrations.RenameField(
            model_name="ArtifactULabel",
            old_name="file",
            new_name="artifact",
        ),
        migrations.AlterUniqueTogether(
            name="artifactfeatureset",
            unique_together={("artifact", "feature_set")},
        ),
        migrations.AlterUniqueTogether(
            name="artifactulabel",
            unique_together={("artifact", "ulabel")},
        ),
        migrations.AlterField(
            model_name="artifact",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_artifacts", to="lnschema_core.user"
            ),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="feature_sets",
            field=models.ManyToManyField(related_name="artifacts", through="lnschema_core.ArtifactFeatureSet", to="lnschema_core.featureset"),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="input_of",
            field=models.ManyToManyField(related_name="input_artifacts", to="lnschema_core.run"),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="run",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="output_artifacts", to="lnschema_core.run"),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="storage",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="artifacts", to="lnschema_core.storage"),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="transform",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="output_artifacts", to="lnschema_core.transform"),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="ulabels",
            field=models.ManyToManyField(related_name="artifacts", through="lnschema_core.ArtifactULabel", to="lnschema_core.ulabel"),
        ),
        migrations.RenameField(
            model_name="transform",
            old_name="source_file",
            new_name="source_code",
        ),
        migrations.AlterField(
            model_name="transform",
            name="source_code",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="source_code_of", to="lnschema_core.artifact"),
        ),
        migrations.AlterField(
            model_name="transform",
            name="latest_report",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="latest_report_of", to="lnschema_core.artifact"),
        ),
        migrations.AlterField(
            model_name="run",
            name="report",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="report_of", to="lnschema_core.artifact"),
        ),
    ]


schemas = lamindb_setup.settings.instance.schema
if "bionty" in schemas:
    Migration.dependencies.append(("lnschema_bionty", "0020_alter_organism_bionty_source"))
if "lamin1" in schemas:
    Migration.dependencies.append(("lnschema_lamin1", "0014_rename_species_biosample_organism"))
