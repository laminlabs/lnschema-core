"""SQLModel extensions.

.. autosummary::
   :toctree: .

   BaseORM
"""

import importlib
import re
import typing
from collections import namedtuple
from typing import Any, Iterable, Optional, Sequence, Tuple, Union

import sqlmodel as sqm
from pydantic import create_model
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import relationship as sa_relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm.session import object_session
from typeguard import check_type

from .. import __name__

MODULE_NAME = __name__

# add naming convention for alembic
sqm.SQLModel.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


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
sqm.SQLModel.__str__ = __repr__


class BaseORM(sqm.SQLModel):  # type: ignore
    """SQLModel with lookup, data validation & schema modules."""

    def __init__(self, **user_kwargs):
        # pydantic does not enforce strict type checking for complex types, only their attributes
        validate_relationship_types(self, user_kwargs)
        super().__init__(**user_kwargs)
        validate_with_pydantic(self, user_kwargs)

    @classmethod
    def lookup(cls, field: Optional[str] = None):
        """Lookup rows by field."""
        import lamindb as ln

        if field is None:
            # by default use the name field
            if "name" in cls.__fields__:
                field = "name"
            else:
                non_ids = [i for i in cls.__fields__.keys() if "id" not in i]
                if len(non_ids) > 0:
                    # the first field isn't named with id
                    field = non_ids[0]
                else:
                    # the first field
                    field = next(iter(cls.__fields__.keys()))
        df = ln.select(cls).df()
        values = set(df[field].values)
        keys = _to_lookup_keys(values, padding=cls.__name__)
        return _namedtuple_from_dict(d=dict(zip(keys, values)), name=cls.__name__)

    @declared_attr
    def __tablename__(cls) -> str:  # type: ignore
        """Prefix table name with module name as in Django."""
        return f"{MODULE_NAME}_{cls.__name__.lower()}"


def get_orm(module_name: str):
    global MODULE_NAME
    MODULE_NAME = module_name

    return BaseORM


# backward compat for migrations ---
SCHEMA_NAME = None


def schema_sqlmodel(schema_name: str):
    global SCHEMA_NAME
    SCHEMA_NAME = schema_name

    import lndb

    if lndb.settings.instance.dialect == "sqlite":
        prefix = f"{schema_name}."
        schema_arg = None
        return BaseORM, prefix, schema_arg
    else:
        prefix = ""
        schema_arg = schema_name
        return BaseORM, prefix, schema_arg


def get_sqlite_prefix_schema_delim_from_alembic() -> Tuple[bool, str, Optional[str], str]:
    from alembic import op

    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema, delim = f"{SCHEMA_NAME}.", None, "."
    else:
        prefix, schema, delim = "", SCHEMA_NAME, "_"

    return sqlite, prefix, schema, delim


# end backward compat for migrations ---


def add_relationship_keys(table: sqm.SQLModel):  # type: ignore
    """add all relationship keys to __sqlmodel_relationships__."""
    for i in getattr(table, "__mapper__").relationships:
        if i not in getattr(table, "__sqlmodel_relationships__"):
            getattr(table, "__sqlmodel_relationships__")[i.key] = None


def add_relationship(
    origin_table: sqm.SQLModel,
    origin_attr_name: str,
    target_attr_name: Optional[str] = None,
):
    """Add relationship defined in the origin table to its respective target table.

    Only valid for many-to-many relationships.

    Args:
        origin_table (sqlmodel.SQLModel): origin (input) table
        origin_attr_name (str): name of the attribute in the origin table that defines the relationship
        target_attr_name (str, optional): name of the corresponding attribute to be added in the relationship target table.
            Defaults to either the back_populates parameter in the origin table relationship attribute (if set) or the snake-case, pluralized name of the origin table.

    Returns:
        None

    Raises:
        ValueError: if origin_attr_name does not correspond to a valid relationship attribute in the origin table
        ValueError: if target_attr_name conflicts with the back_populates parameter set in the attribute of the origin table that defines the relationship
    """
    # raise error if there is no attribute with name origin_attr_name
    origin_attr = getattr(origin_table, origin_attr_name)
    # raise error if attr is not a relationship
    relationship = getattr(origin_attr, "prop")
    if not isinstance(relationship, RelationshipProperty):
        raise ValueError("Input attribute must be a relationship.")
    # make sure relationship key is in __sqlmodel_relationships__
    if relationship not in getattr(origin_table, "__sqlmodel_relationships__"):
        getattr(origin_table, "__sqlmodel_relationships__")[relationship.key] = None
    # create relationship attribute in target table
    target_table = relationship.entity.entity
    target_attr_name = _derive_target_attr_name(origin_table, relationship, target_attr_name)
    setattr(
        target_table,
        target_attr_name,  # type: ignore
        sa_relationship(
            origin_table,
            back_populates=relationship.key,
            secondary=relationship.secondary,
        ),
    )
    # add relationship key to target table
    getattr(target_table, "__sqlmodel_relationships__")[target_attr_name] = None


def add_relationships(origin_table: sqm.SQLModel):
    """Add all relationships defined in the origin table to their corresponding target tables.

    Only valid for many-to-many relationships.

    Args:
        origin_table (sqlmodel.SQLModel): origin (input) table

    Returns:
        None
    """
    for attr in origin_table.__dict__.values():
        # skip attributes that are not relationships
        attr_property = getattr(attr, "prop", None)
        if not isinstance(attr_property, RelationshipProperty):
            continue
        relationship = attr_property
        # only configure relationships that are many-to-many
        if getattr(relationship, "secondary") is not None:
            origin_attr_name = relationship.key
            add_relationship(origin_table, origin_attr_name)


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
                f"  should be of type {rel_type.__module__}.{rel_type}, got "
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
                    try:
                        setattr(model, field_name, getattr(user_kwargs[relationship_name], col_name))
                    except AttributeError:
                        pass


def _derive_target_attr_name(
    origin_table: sqm.SQLModel,
    origin_relationship: RelationshipProperty,
    custom_target_name,
):
    """Derive the name of the relationship attribute in the target table."""
    # If set, back_populates parameter in the origin relationship takes precedence over any custom naming
    if origin_relationship.back_populates is not None:
        if custom_target_name is not None and custom_target_name != origin_relationship.back_populates:
            raise ValueError(
                "Custom name for the relationship attribute in the target table conflicts with back_populates parameter set in the relationship attribute of the origin table."
            )
        return origin_relationship.back_populates
    else:
        if custom_target_name is not None:
            return custom_target_name
        else:
            # Convert origin table name from camel to snake case and make it plural
            return f"{re.sub(r'(?<!^)(?=[A-Z])', '_', origin_table.__name__).lower()}s"


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
        # Union-like types (e.g. typing.Union[str, ForwardRef("lnschema_core._core.Transform")])
        # and raises an error at class definition when a field is typed as such.
        return getattr(typing, parent_ref)[resolved_args[0], resolved_args[1]]


# # as a decorator
# def db_lookup(lookup_field: str = 'name'):
#     def wrapper(sqlmodel_class):
#         @classproperty
#         def df(cls):
#             import lamindb as ln

#             return ln.select(sqlmodel_class).df()

#         @classproperty
#         def lookup(cls):
#             return lookup_field

#         sqlmodel_class.df = df
#         sqlmodel_class.lookup = lookup
#         return sqlmodel_class

#     return wrapper


def _to_lookup_keys(x: Iterable[str], padding: str = "LOOKUP") -> list:
    """Convert a list of strings to tab-completion allowed formats."""
    lookup = [re.sub("[^0-9a-zA-Z]+", "_", str(i)) for i in x]
    for i, value in enumerate(lookup):
        if value == "" or (not value[0].isalpha()):
            lookup[i] = f"{padding}_{value}"
    return lookup


def _namedtuple_from_dict(d: dict, name: str = "entity") -> tuple:
    """Create a namedtuple from a dict to allow autocompletion."""
    nt = namedtuple(name, d.keys())  # type:ignore
    return nt(**d)
