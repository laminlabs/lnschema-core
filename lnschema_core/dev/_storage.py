from pathlib import Path
from typing import Union

from cloudpathlib import CloudPath


def get_name_suffix_from_filepath(filepath: Union[Path, CloudPath]):
    suffix = "".join(filepath.suffixes)
    name = filepath.name.replace(suffix, "")
    return name, suffix


# add type annotations back asap when re-organizing the module
def storage_key_from_dobject(dobj):
    return f"{dobj.id}{dobj.suffix}"


# add type annotations back asap when re-organizing the module
def filepath_from_dobject(dobj):
    from lndb_setup import settings

    storage_key = storage_key_from_dobject(dobj)
    filepath = settings.instance.storage.key_to_filepath(storage_key)
    return filepath
