[![pypi](https://img.shields.io/pypi/v/lnschema_core?color=%2334D058&label=pypi%20package)](https://pypi.org/project/lnschema_core)

# `lnschema_core`

`lnschema_core` is documented & tested within `lamindb`: [github.com/laminlabs/lamindb](https://github.com/laminlabs/lamindb).

## Developers' Note

This package implements models but leaves concrete implementations of non-ORM methods (such as `Artifact.cache`) empty. The methods are implemented in `lamindb` and then the model classes are monkey-patched there as well.

### Why monkey pathing?

We want to avoid implementing anything non-ORM related in this package and just have models here, so that concrete implementations are all in `lamindb`. This provides better code structure and clarity compared to having imports from `lamindb` needed if the implementations are done here.

### Why not simple inheritance?

It is possible to replace monkey patching with simple inheritance for some model classes (like `Artifact`), but it is hard to do for all due to the situation when a model class inherits another model class within `lnschema-core`. This is true, for example, for `Artifact` inheriting `Record`.

If we want simple inheritance for `Artifact` in `lamindb`, we will also have to implement simple inheritance for `Record` there and make the `Artifact` child class inherit this `Record` child class, duplicating the inheritance structure and complicating the code.
