"""SQLModel children.

.. autosummary::
   :toctree: .

   SQLModelModule
   SQLModelPrefix
"""

import importlib
import os
import typing
from typing import Any, Optional, Sequence, Tuple, Union

import sqlmodel as sqm
from pydantic import create_model
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm.session import object_session
from typeguard import check_type

# add naming convention for alembic
sqm.SQLModel.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


# it's tricky to deal with class variables in SQLModel children
# hence, we're using a global variable, here
SCHEMA_NAME = None


def __repr_args__(self) -> Sequence[Tuple[Optional[str], Any]]:
    # sort like fields
    return [(k, self.__dict__[k]) for k in self.__fields__ if (not k.startswith("_sa_") and k in self.__dict__ and self.__dict__[k] is not None)]  # noqa  # noqa


def __repr__(self):
    if object_session(self) is not None:
        return "[session open] " + super(sqm.SQLModel, self).__repr__()
    else:
        return super(sqm.SQLModel, self).__repr__()


sqm.SQLModel.__repr_args__ = __repr_args__
sqm.SQLModel.__repr__ = __repr__


class SQLModelModule(sqm.SQLModel):
    """SQLModel for schema module."""

    def __init__(self, **user_kwargs):
        # pydantic does not enforce strict type checking for complex types, only their attributes
        validate_relationship_types(self, user_kwargs)
        super().__init__(**user_kwargs)
        validate_with_pydantic(self, user_kwargs)

    # this here is problematic for those tables that overwrite
    # __table_args__; we currently need to treat them manually
    @declared_attr
    def __table_args__(cls) -> str:
        """Update table args with schema module."""
        return dict(schema=f"{SCHEMA_NAME}")  # type: ignore


class SQLModelPrefix(sqm.SQLModel):  # type: ignore
    """SQLModel prefixed by schema module name."""

    def __init__(self, **user_kwargs):
        # pydantic does not enforce strict type checking for complex types, only their attributes
        validate_relationship_types(self, user_kwargs)
        super().__init__(**user_kwargs)
        validate_with_pydantic(self, user_kwargs)

    @declared_attr
    def __tablename__(cls) -> str:  # type: ignore
        """Prefix table name with schema module."""
        return f"{SCHEMA_NAME}.{cls.__name__.lower()}"


def is_sqlite():
    # for this to work, lndb can't import lnschema_core statically
    # it can only import it dynamically like all other schema modules
    try:
        from lndb._settings_load import load_instance_settings

        isettings = load_instance_settings()
        sqlite_true = isettings.dialect == "sqlite"
    except (ImportError, RuntimeError):
        sqlite_true = True

    return sqlite_true


def schema_sqlmodel(schema_name: str):
    global SCHEMA_NAME
    SCHEMA_NAME = schema_name

    if "hub" in os.environ and os.environ["hub"] == "true":
        prefix = ""
        schema_arg = schema_name
        return SQLModelModule, prefix, schema_arg
    elif is_sqlite():
        prefix = f"{schema_name}."
        schema_arg = None
        return SQLModelPrefix, prefix, schema_arg
    else:
        prefix = ""
        schema_arg = schema_name
        return SQLModelModule, prefix, schema_arg


def add_relationship_keys(table: sqm.SQLModel):  # type: ignore
    """add all relationship keys to __sqlmodel_relationships__."""
    for i in getattr(table, "__mapper__").relationships:
        if i not in getattr(table, "__sqlmodel_relationships__"):
            getattr(table, "__sqlmodel_relationships__")[i.key] = None


def validate_with_pydantic(model, user_kwargs):
    annotations = model.__annotations__
    kwargs = {**model.__dict__, **user_kwargs}
    pydantic_annotations = {}
    for field, ann in annotations.items():
        # ignore special fields
        if field.startswith("_"):
            kwargs.pop(field, None)
            user_kwargs.pop(field, None)
            continue

        # resolve forward references
        resolved_ann = ann
        if "ForwardRef" in str(ann):  # typing.ForwardRef not available in python <= 3.6.12
            resolved_ann = _resolve_forward_ref(ann, model.__module__)

        # handle relationship and optional fields
        if field in model.__sqlmodel_relationships__ or _is_ann_optional(ann) or _is_field_optional(model.__fields__.get(field)):
            pydantic_annotations[field] = (resolved_ann, None)
        else:
            # do not validate auto-populated (server-side) created_at fields
            if field in model.__fields__:
                sa_column_kwargs = getattr(model.__fields__[field].field_info, "sa_column_kwargs", None)
                if isinstance(sa_column_kwargs, dict):
                    if "server_default" in sa_column_kwargs and field not in user_kwargs:
                        continue
            pydantic_annotations[field] = (resolved_ann, ...)

    # validate with pydantic
    validation_model = create_model(model.__class__.__name__, **pydantic_annotations)
    validation_model.validate(kwargs)
    return


def validate_relationship_types(model, user_kwargs):
    # only validate standard sqlmodel relationships (typed) passed by the user
    standard_sqm_relationships = {k: v for k, v in model.__sqlmodel_relationships__.items() if v is not None}
    standard_user_rel_keys = standard_sqm_relationships.keys() & user_kwargs.keys()
    for key in standard_user_rel_keys:
        if "ForwardRef" in str(model.__annotations__[key]):
            rel_type = _resolve_forward_ref(model.__annotations__[key], model.__module__)
        else:
            rel_type = model.__annotations__[key]
        try:
            check_type(key, user_kwargs[key], rel_type)
        except TypeError:
            error_message = (
                f"Validation error for {model.__class__.__name__}\n"
                f"{key}\n"
                f"  should be of type {rel_type.__module__}.{rel_type.__name__}, got "
                f"{user_kwargs[key].__class__.__module__}.{user_kwargs[key].__class__.__name__} instead."
            )
            raise TypeError(error_message) from None

    # auto-populate foreign key fields associated with any relationship passed by the user (avoid missing key error during pydantic validation)
    all_user_rel_keys = model.__sqlmodel_relationships__.keys() & user_kwargs.keys()
    for relationship_name in all_user_rel_keys:
        rel_local_fields = getattr(model.__class__, relationship_name).property.local_columns  # model fields associated with the relationship
        rel_fk_fields = [field for field in rel_local_fields if not field.primary_key]  # primary keys are returned as local fields in link table relationships
        rel_fk_field_names = [field.name for field in rel_fk_fields]
        target_col_names = [list(field.foreign_keys)[0].column.name for field in rel_fk_fields]
        for field_name, col_name in zip(rel_fk_field_names, target_col_names):
            if hasattr(model, field_name):
                if getattr(model, field_name) is None:
                    setattr(model, field_name, getattr(user_kwargs[relationship_name], col_name))


def _is_ann_optional(type_ann):
    if type_ann.__module__ == "typing":
        try:
            if type_ann.__origin__ == Union:
                if type(None) in type_ann.__args__:
                    return True
        except Exception:
            return False
    return False


def _is_field_optional(model_field):
    if model_field is None:
        return False
    return not model_field.required


def _resolve_forward_ref(ann, module):
    # fetch target type as string
    forward_args = []
    parent_ref = None
    if _is_ann_optional(ann):
        forward_args = [ann.__args__[0].__forward_arg__]
    else:
        try:
            for arg in ann.__args__:
                if "ForwardRef" in str(arg):
                    forward_args += [arg.__forward_arg__]
            parent_ref = ann._name
        except Exception:
            forward_args = [ann.__forward_arg__]

    # fetch target type from string
    resolved_args = []
    for arg in forward_args:
        split_arg = arg.split(".")
        try:
            # if reference is in another module
            resolved_args += [getattr(importlib.import_module(split_arg[0]), split_arg[-1])]
        except Exception:
            resolved_args += [getattr(importlib.import_module(module), split_arg[-1])]

    # return resolved annotation
    if len(resolved_args) == 1:
        if parent_ref is None:
            return resolved_args[0]
        else:
            return getattr(typing, parent_ref)[resolved_args[0]]
    else:
        # This code should never run. SQLmodel is incompatible with non-optional
        # Union-like types (e.g. typing.Union[str, ForwardRef("lnschema_core._core.Pipeline")])
        # and raises an error at class definition when a field is typed as such.
        return getattr(typing, parent_ref)[resolved_args[0], resolved_args[1]]
