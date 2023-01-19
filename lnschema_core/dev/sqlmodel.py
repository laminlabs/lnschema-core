"""SQLModel children.

.. autosummary::
   :toctree: .

   SQLModelModule
   SQLModelPrefix
"""

import importlib
import os
from typing import Any, Optional, Sequence, Tuple

import sqlmodel as sqm
from pydantic import create_model
from sqlalchemy.orm import declared_attr

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


sqm.SQLModel.__repr_args__ = __repr_args__


def validate_with_pydantic(model, user_kwargs):
    annotations = model.__annotations__
    kwargs = {**model.__dict__, **user_kwargs}
    pydantic_annotations = {}
    relationship_fields = {}
    for field, ann in annotations.items():
        if ann.__module__ == "typing":
            # handle forward references
            required_ann = ann.__args__[0]
            if "ForwardRef" in str(required_ann.__class__):  # typing.ForwardRef not available in python <= 3.6.12
                ref = required_ann.__forward_arg__.split(".")
                try:
                    # if reference is in another module
                    resolved_ann = getattr(importlib.import_module(ref[0]), ref[-1])
                except Exception:
                    resolved_ann = getattr(importlib.import_module(model.__module__), ref[-1])
            else:
                resolved_ann = required_ann
            # handle optional and relationship fields
            if field in model.__sqlmodel_relationships__:
                relationship_fields[field] = resolved_ann
                pydantic_annotations[field] = (resolved_ann, None)
            elif type(None) in ann.__args__:
                pydantic_annotations[field] = (resolved_ann, None)
            else:
                pydantic_annotations[field] = (resolved_ann, ...)
        else:
            # do not validate auto-populated (server-side) created_at fields
            if field == "created_at" and "created_at" not in user_kwargs:
                continue
            else:
                pydantic_annotations[field] = (ann, ...)
    # pydantic does not check for the type of complex objects, only their attributes
    for key in relationship_fields.keys() & user_kwargs.keys():
        if not isinstance(user_kwargs[key], relationship_fields[key]):
            raise TypeError(f"Validation error for {model.__class__.__name__}: field {field} should be of type {relationship_fields[key].__name__}.")
    validation_model = create_model(model.__class__.__name__, **pydantic_annotations)
    validation_model.validate(kwargs)
    return


class SQLModelModule(sqm.SQLModel):
    """SQLModel for schema module."""

    def __init__(self, **user_kwargs):
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
        super().__init__(**user_kwargs)
        validate_with_pydantic(self, user_kwargs)

    @declared_attr
    def __tablename__(cls) -> str:  # type: ignore
        """Prefix table name with schema module."""
        return f"{SCHEMA_NAME}.{cls.__name__.lower()}"


def is_sqlite():
    # for this to work, lndb_setup can't import lnschema_core statically
    # it can only import it dynamically like all other schema modules
    try:
        from lndb_setup._settings_load import load_instance_settings

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
