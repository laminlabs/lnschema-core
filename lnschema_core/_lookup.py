import re
from collections import namedtuple
from typing import Iterable, Optional

from django.db import models


def lookup(orm: models.Model, field: Optional[str] = None):
    """Lookup rows by field."""
    model_field_names = [i.name for i in orm._meta.fields]
    if field is None:
        # by default use the name field
        if "name" in model_field_names:
            field = "name"
        else:
            non_ids = [i for i in model_field_names if "id" not in i]
            if len(non_ids) > 0:
                # the first field isn't named with id
                field = non_ids[0]
            else:
                # the first field
                field = model_field_names[0]
    values = set(orm.objects.values_list(field, flat=True))
    for value in [None, ""]:
        if value in values:
            values.remove(value)
    keys = to_lookup_keys(values, padding=orm.__name__)
    nt = namedtuple_from_dict(d=dict(zip(keys, values)), name=orm.__name__)
    return nt


def to_lookup_keys(x: Iterable[str], padding: str = "LOOKUP") -> list:
    """Convert a list of strings to tab-completion allowed formats."""
    lookup = [re.sub("[^0-9a-zA-Z]+", "_", str(i)) for i in x]
    for i, value in enumerate(lookup):
        if value == "" or (not value[0].isalpha()):
            lookup[i] = f"{padding}_{value}"
    return lookup


def namedtuple_from_dict(d: dict, name: str = "entity") -> tuple:
    """Create a namedtuple from a dict to allow autocompletion."""
    nt = namedtuple(name, d.keys())  # type:ignore
    return nt(**d)
