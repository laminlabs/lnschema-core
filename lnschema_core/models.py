from django.db import models
from django.db.models import Model as BaseORM
from nbproject._is_run_from_ipython import is_run_from_ipython

from ._users import current_user_id_as_int
from .types import TransformType


class RunInput(models.Model):
    run = models.ForeignKey("Run", on_delete=models.CASCADE)
    file = models.ForeignKey("File", on_delete=models.CASCADE)

    class Meta:
        managed = True


class User(BaseORM):
    email = models.CharField(max_length=64, unique=True)
    handle2 = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Storage(BaseORM):
    root = models.CharField(max_length=64)
    type = models.CharField(max_length=64, blank=True, null=True)
    region = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, default=current_user_id_as_int)

    class Meta:
        managed = True


class Project(BaseORM):
    name = models.CharField(max_length=64)
    folders = models.ManyToManyField("Folder")
    files = models.ManyToManyField("File")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id_as_int)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Transform(models.Model):
    name = models.CharField(max_length=64)
    version = models.CharField(max_length=64)
    type = models.CharField(max_length=64, choices=TransformType.choices(), db_index=True, default=(TransformType.notebook if is_run_from_ipython else TransformType.pipeline))
    title = models.CharField(max_length=64, blank=True, null=True)
    reference = models.CharField(max_length=64, blank=True, null=True)
    created_by = models.ForeignKey("User", models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "version"),)


class Run(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    external_id = models.CharField(max_length=64, blank=True, null=True)
    transform = models.ForeignKey(Transform, models.DO_NOTHING)
    inputs = models.ManyToManyField("File", through=RunInput, related_name="input_of")
    # outputs on File
    created_by = models.ForeignKey(User, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True


class Features(models.Model):
    type = models.CharField(max_length=64)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id_as_int)
    created_at = models.DateTimeField(auto_now=True)
    files = models.ManyToManyField("File")

    class Meta:
        managed = True


class Folder(models.Model):
    name = models.CharField(max_length=64)
    key = models.CharField(max_length=64, blank=True, null=True)
    storage = models.ForeignKey(Storage, models.DO_NOTHING)
    files = models.ManyToManyField("File")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id_as_int)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        unique_together = (("storage", "key"),)


class File(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    suffix = models.CharField(max_length=64, blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True)
    hash = models.CharField(max_length=64, blank=True, null=True)
    key = models.CharField(max_length=64, blank=True, null=True)
    run = models.ForeignKey(Run, models.DO_NOTHING, blank=True, null=True, related_name="outputs")
    transform = models.ForeignKey(Transform, models.DO_NOTHING, blank=True, null=True)
    storage = models.ForeignKey(Storage, models.DO_NOTHING)
    # folders from Folders.files
    # features from Features.files
    # input_of from Run.inputs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id_as_int)

    class Meta:
        managed = True
        unique_together = (("storage", "key"),)
