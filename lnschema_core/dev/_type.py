from enum import Enum


class usage(str, Enum):
    """Data access types."""

    ingest = "ingest"
    insert = "insert"
    select = "select"
    update = "update"
    delete = "delete"
    load = "load"
    link = "link"
