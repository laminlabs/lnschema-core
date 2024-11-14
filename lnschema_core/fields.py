from django.db import models


class CharField(models.CharField):
    """Custom `CharField` with default values for `blank`, `default`, and `max_length`.

    Django default values for `CharField` are `blank=False`, `default=""`, undefined `max_length`.
    """

    def __init__(self, max_length: int = 255, **kwargs):
        kwargs["max_length"] = max_length  # Set max_length in kwargs
        kwargs.setdefault("blank", True)
        kwargs.setdefault("default", None)
        super().__init__(**kwargs)  # Pass all arguments as kwargs


class TextField(models.TextField):
    """Custom `TextField` with default values for `blank` and `default`.

    Django default values for `TextField` are `blank=False`, `default=''`.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        kwargs.setdefault("default", None)
        super().__init__(*args, **kwargs)


class ForeignKey(models.ForeignKey):
    """Custom `ForeignKey` with default values for `blank`.

    Django default value for `ForeignKey` `blank=False`.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)


class BooleanField(models.BooleanField):
    """Custom `BooleanField` with default values for `blank` and `default`.

    Django default values for `BooleanField` are `blank=False`, `default=False`.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        kwargs.setdefault("default", None)
        super().__init__(*args, **kwargs)


class DateTimeField(models.DateTimeField):
    """Custom `DateTimeField` with default values for `blank`.

    Django default values for `DateTimeField` are `blank=False`.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)


class BigIntegerField(models.BigIntegerField):
    """Custom `BigIntegerField` with default values for `blank`.

    Django default values for `BigIntegerField` are `blank=False`.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)


class IntegerField(models.IntegerField):
    """Custom `IntegerField` with default values for `blank`.

    Django default values for `IntegerField` are `blank=False`.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)
