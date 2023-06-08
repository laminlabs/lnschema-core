from typing import List

from django.db import models


class NoResultFound(Exception):
    pass


class MultipleResultsFound(Exception):
    pass


class QuerySet(models.QuerySet):
    """Extension of Django QuerySet.

    This brings some of the SQLAlchemy/SQLModel/SQL-inspired calls.

    As LaminDB was based on SQLAlchemy/SQLModel in the beginning, and might
    support it again in the future, these calls will be supported longtime.
    """

    def df(self):
        import pandas as pd

        columns = [field.name for field in self.model._meta.fields if not isinstance(field, models.ForeignKey)]
        columns += [f"{field.name}_id" for field in self.model._meta.fields if isinstance(field, models.ForeignKey)]
        df = pd.DataFrame(self.values(), columns=columns)
        if "id" in df.columns:
            df = df.set_index("id")
        return df

    def list(self) -> List:
        return list(self)

    def first(self):
        if len(self) == 0:
            return None
        return self[0]

    def one(self):
        if len(self) == 0:
            raise NoResultFound
        elif len(self) > 1:
            raise MultipleResultsFound
        else:
            return self[0]

    def one_or_none(self):
        if len(self) == 0:
            return None
        elif len(self) == 1:
            return self[0]
        else:
            raise MultipleResultsFound
