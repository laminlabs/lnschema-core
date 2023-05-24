from django.db import models
from django.db.models import Model as BaseORM
from nbproject._is_run_from_ipython import is_run_from_ipython

from ._users import current_user_id
from .types import TransformType


class User(BaseORM):  # type: ignore
    id = models.CharField(max_length=64, primary_key=True)
    email = models.CharField(max_length=64, unique=True)
    handle2 = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Storage(BaseORM):  # type: ignore
    id = models.CharField(max_length=64, primary_key=True)
    root = models.CharField(max_length=64)
    type = models.CharField(max_length=64, blank=True, null=True)
    region = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("User", models.DO_NOTHING, blank=True, null=True, default=current_user_id)

    class Meta:
        managed = True


class Project(BaseORM):  # type: ignore
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    created_by = models.ForeignKey("User", models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Transform(models.Model):  # type: ignore
    id = models.CharField(max_length=64, primary_key=True)
    version = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64, choices=TransformType.choices(), db_index=True, default=(TransformType.notebook if is_run_from_ipython else TransformType.pipeline))
    title = models.CharField(max_length=64, blank=True, null=True)
    reference = models.CharField(max_length=64, blank=True, null=True)
    created_by = models.ForeignKey("User", models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        constraints = [models.UniqueConstraint(fields=["id", "version"], name="uq_transform_id_version")]


class Run(models.Model):  # type: ignore
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    external_id = models.CharField(max_length=64, blank=True, null=True)
    transform = models.ForeignKey("Transform", models.DO_NOTHING)
    transform_version = models.CharField(max_length=64)
    created_by = models.ForeignKey("User", models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True


class Features(models.Model):  # type: ignore
    id = models.CharField(max_length=64, primary_key=True)
    type = models.CharField(max_length=64)
    created_by = models.ForeignKey("User", models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Folder(models.Model):  # type: ignore
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    key = models.CharField(max_length=64, blank=True, null=True)
    storage = models.ForeignKey("Storage", models.DO_NOTHING)
    created_by = models.ForeignKey("User", models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        unique_together = (("storage", "key"),)


class File(models.Model):  # type: ignore
    id = models.CharField(max_length=64, primary_key=True)
    size = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    suffix = models.CharField(max_length=64, blank=True, null=True)
    hash = models.CharField(max_length=64, blank=True, null=True)
    key = models.CharField(max_length=64, blank=True, null=True)
    run = models.ForeignKey("Run", models.DO_NOTHING, blank=True, null=True)
    transform = models.ForeignKey("Transform", models.DO_NOTHING, blank=True, null=True)
    transform_version = models.CharField(max_length=64, blank=True, null=True)
    storage = models.ForeignKey("Storage", models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("User", models.DO_NOTHING, default=current_user_id)

    class Meta:
        managed = True
        unique_together = (("storage", "key"),)
