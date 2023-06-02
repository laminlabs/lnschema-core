import re
from collections import namedtuple
from typing import Any, Iterable, Optional

from lamindb_setup import _USE_DJANGO


def lookup(cls: Any, field: Optional[str] = None):
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
    if _USE_DJANGO:
        values = set(cls.objects.values_list(field, flat=True))
    else:
        df = ln.select(cls).df()
        values = set(df[field].values)
    for value in [None, ""]:
        if value in values:
            values.remove(value)
    keys = to_lookup_keys(values, padding=cls.__name__)
    nt = namedtuple_from_dict(d=dict(zip(keys, values)), name=cls.__name__)
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
