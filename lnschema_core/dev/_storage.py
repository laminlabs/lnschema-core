# add type annotations back asap when re-organizing the module
def storage_key_from_file(file):
    if file.key is None:
        return f"{file.id}{file.suffix}"
    else:
        return f"{file.key}"


# add type annotations back asap when re-organizing the module
def filepath_from_file(dobj):
    from lndb import settings

    storage_key = storage_key_from_file(dobj)
    filepath = settings.instance.storage.key_to_filepath(storage_key)
    return filepath


# add type annotations back asap when re-organizing the module
def filepath_from_folder(folder):
    from lndb import settings

    return settings.instance.storage.key_to_filepath(folder._objectkey)
