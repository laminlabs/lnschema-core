from __future__ import annotations

import builtins
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Literal,
    NamedTuple,
    overload,
)

from django.db import models
from django.db.models import CASCADE, PROTECT, Field
from django.db.models.base import ModelBase
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
    ManyToManyRel,
    ManyToOneRel,
)
from lamin_utils import colors, logger
from lamindb_setup import _check_instance_setup
from lamindb_setup.core.hashing import HASH_LENGTH

from lnschema_core.types import (
    ArtifactType,
    CharField,
    FieldAttr,
    ListLike,
    StrField,
    TextField,
    TransformType,
    VisibilityChoice,
)

from .ids import base62_8, base62_12, base62_20
from .users import current_user_id

if TYPE_CHECKING:
    from pathlib import Path

    import numpy as np
    import pandas as pd
    from anndata import AnnData
    from lamin_utils._inspect import InspectResult
    from lamindb.core import LabelManager
    from lamindb_setup.core.types import UPathStr
    from mudata import MuData
    from tiledbsoma import Collection as SOMACollection
    from tiledbsoma import Experiment as SOMAExperiment
    from upath import UPath

    from lnschema_core.mocks import (
        AnnDataAccessor,
        BackedAccessor,
        MappedCollection,
        QuerySet,
        RecordsList,
    )


_TRACKING_READY: bool | None = None
IS_RUN_FROM_IPYTHON = getattr(builtins, "__IPYTHON__", False)


class IsVersioned(models.Model):
    """Base class for versioned models."""

    class Meta:
        abstract = True

    _len_stem_uid: int

    version: str = CharField(max_length=10, default=None, null=True, db_index=True)
    """Version (default `None`).

    Defines version of a family of records characterized by the same `stem_uid`.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """

    @overload
    def __init__(self): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

    @property
    def stem_uid(self) -> str:
        """Universal id characterizing the version family.

        The full uid of a record is obtained via concatenating the stem uid and version information::

            stem_uid = random_base62(n_char)  # a random base62 sequence of length n_char
            version_uid = encode_base62(md5_hash(version))[:4]  # version is, e.g., "1" or "2.1.0" or "2022-03-01"
            uid = f"{stem_uid}{version_uid}"  # concatenate the stem_uid & version_uid

        """
        return self.uid[: self._len_stem_uid]  # type: ignore

    @property
    def versions(self) -> QuerySet:
        """Lists all records of the same version family.

        >>> new_artifact = ln.Artifact(df2, is_new_version_of=artifact)
        >>> new_artifact.save()
        >>> new_artifact.versions()
        """
        return self.__class__.filter(uid__startswith=self.stem_uid)  # type: ignore

    def _add_to_version_family(
        self, is_new_version_of: IsVersioned, version: str | None = None
    ):
        """Add current record to a version family.

        Args:
            is_new_version_of: a record that belongs to the version family.
            version: semantic version of the record.
        """
        pass


def current_run() -> Run | None:
    global _TRACKING_READY

    if not _TRACKING_READY:
        _TRACKING_READY = _check_instance_setup()
    if _TRACKING_READY:
        import lamindb.core

        return lamindb.core.run_context.run
    else:
        return None


class TracksRun(models.Model):
    """Base class tracking latest run, creating user. nd `created_at` timestamp."""

    class Meta:
        abstract = True

    created_at: datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    created_by: User = models.ForeignKey(
        "lnschema_core.User", PROTECT, default=current_user_id
    )
    """Creator of record."""
    run: Run = models.ForeignKey(
        "lnschema_core.Run", PROTECT, null=True, default=current_run
    )
    """Last run that created or updated the record."""

    @overload
    def __init__(self): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class TracksUpdates(models.Model):
    """Base class tracking previous runs and `updated_at` timestamp."""

    class Meta:
        abstract = True

    updated_at: datetime = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    # no default related_name below because it'd clash with the reverse accessor
    # of the .run field
    _previous_runs: Run = models.ManyToManyField("lnschema_core.Run", related_name="+")
    """Sequence of runs that created or updated the record."""

    @overload
    def __init__(self): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class CanValidate:
    """Base class providing :class:`~lamindb.core.Record`-based validation."""

    @classmethod
    def inspect(
        cls,
        values: ListLike,
        field: str | StrField | None = None,
        *,
        mute: bool = False,
        organism: str | Record | None = None,
        source: Record | None = None,
    ) -> InspectResult:
        """Inspect if values are mappable to a field.

        Being mappable means that an exact match exists.

        Args:
            values: Values that will be checked against the
                field.
            field: The field of values. Examples are `'ontology_id'` to map
                against the source ID or `'name'` to map against the ontologies
                field names.
            mute: Mute logging.
            organism: An Organism name or record.
            source: A Source record.

        See Also:
            :meth:`~lamindb.core.CanValidate.validate`

        Examples:
            >>> import bionty as bt
            >>> bt.settings.organism = "human"
            >>> ln.save(bt.Gene.from_values(["A1CF", "A1BG", "BRCA2"], field="symbol"))
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> result = bt.Gene.inspect(gene_symbols, field=bt.Gene.symbol)
            >>> result.validated
            ['A1CF', 'A1BG']
            >>> result.non_validated
            ['FANCD1', 'FANCD20']
        """
        pass

    @classmethod
    def validate(
        cls,
        values: ListLike,
        field: str | StrField | None = None,
        *,
        mute: bool = False,
        organism: str | Record | None = None,
    ) -> np.ndarray:
        """Validate values against existing values of a string field.

        Note this is strict validation, only asserts exact matches.

        Args:
            values: Values that will be validated against the field.
            field: The field of values.
                    Examples are `'ontology_id'` to map against the source ID
                    or `'name'` to map against the ontologies field names.
            mute: Mute logging.

        Returns:
            A vector of booleans indicating if an element is validated.

        See Also:
            :meth:`~lamindb.core.CanValidate.inspect`

        Examples:
            >>> import bionty as bt
            >>> bt.settings.organism = "human"
            >>> ln.save(bt.Gene.from_values(["A1CF", "A1BG", "BRCA2"], field="symbol"))
            >>> gene_symbols = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> bt.Gene.validate(gene_symbols, field=bt.Gene.symbol)
            ✅ 2 terms (50.00%) are validated
            🔶 2 terms (50.00%) are not validated
            array([ True,  True, False, False])
        """
        pass

    @classmethod
    def standardize(
        cls,
        values: Iterable,
        field: str | StrField | None = None,
        *,
        return_field: str | StrField | None = None,
        return_mapper: bool = False,
        case_sensitive: bool = False,
        mute: bool = False,
        public_aware: bool = True,
        keep: Literal["first", "last", False] = "first",
        synonyms_field: str = "synonyms",
        organism: str | Record | None = None,
    ) -> list[str] | dict[str, str]:
        """Maps input synonyms to standardized names.

        Args:
            values: Identifiers that will be standardized.
            field: The field representing the standardized names.
            return_field: The field to return. Defaults to field.
            return_mapper: If `True`, returns `{input_value: standardized_name}`.
            case_sensitive: Whether the mapping is case sensitive.
            mute: Mute logging.
            public_aware: Whether to standardize from Bionty reference. Defaults to `True` for Bionty registries.
            keep: When a synonym maps to multiple names, determines which duplicates to mark as `pd.DataFrame.duplicated`:
                    - `"first"`: returns the first mapped standardized name
                    - `"last"`: returns the last mapped standardized name
                    - `False`: returns all mapped standardized name.

                  When `keep` is `False`, the returned list of standardized names will contain nested lists in case of duplicates.

                  When a field is converted into return_field, keep marks which matches to keep when multiple return_field values map to the same field value.
            synonyms_field: A field containing the concatenated synonyms.
            organism: An Organism name or record.

        Returns:
            If `return_mapper` is `False`: a list of standardized names. Otherwise,
            a dictionary of mapped values with mappable synonyms as keys and
            standardized names as values.

        See Also:
            :meth:`~lamindb.core.CanValidate.add_synonym`
                Add synonyms.
            :meth:`~lamindb.core.CanValidate.remove_synonym`
                Remove synonyms.

        Examples:
            >>> import bionty as bt
            >>> bt.settings.organism = "human"
            >>> ln.save(bt.Gene.from_values(["A1CF", "A1BG", "BRCA2"], field="symbol"))
            >>> gene_synonyms = ["A1CF", "A1BG", "FANCD1", "FANCD20"]
            >>> standardized_names = bt.Gene.standardize(gene_synonyms)
            >>> standardized_names
            ['A1CF', 'A1BG', 'BRCA2', 'FANCD20']
        """
        pass

    def add_synonym(
        self,
        synonym: str | ListLike,
        force: bool = False,
        save: bool | None = None,
    ):
        """Add synonyms to a record.

        Args:
            synonym
            force
            save

        See Also:
            :meth:`~lamindb.core.CanValidate.remove_synonym`
                Remove synonyms.

        Examples:
            >>> import bionty as bt
            >>> bt.CellType.from_source(name="T cell").save()
            >>> lookup = bt.CellType.lookup()
            >>> record = lookup.t_cell
            >>> record.synonyms
            'T-cell|T lymphocyte|T-lymphocyte'
            >>> record.add_synonym("T cells")
            >>> record.synonyms
            'T cells|T-cell|T-lymphocyte|T lymphocyte'
        """
        pass

    def remove_synonym(self, synonym: str | ListLike):
        """Remove synonyms from a record.

        Args:
            synonym: The synonym value.

        See Also:
            :meth:`~lamindb.core.CanValidate.add_synonym`
                Add synonyms

        Examples:
            >>> import bionty as bt
            >>> bt.CellType.from_source(name="T cell").save()
            >>> lookup = bt.CellType.lookup()
            >>> record = lookup.t_cell
            >>> record.synonyms
            'T-cell|T lymphocyte|T-lymphocyte'
            >>> record.remove_synonym("T-cell")
            'T lymphocyte|T-lymphocyte'
        """
        pass

    def set_abbr(self, value: str):
        """Set value for abbr field and add to synonyms.

        Args:
            value: A value for an abbreviation.

        See Also:
            :meth:`~lamindb.core.CanValidate.add_synonym`
                Add synonyms.

        Examples:
            >>> import bionty as bt
            >>> bt.ExperimentalFactor.from_source(name="single-cell RNA sequencing").save()
            >>> scrna = bt.ExperimentalFactor.filter(name="single-cell RNA sequencing").one()
            >>> scrna.abbr
            None
            >>> scrna.synonyms
            'single-cell RNA-seq|single-cell transcriptome sequencing|scRNA-seq|single cell RNA sequencing'
            >>> scrna.set_abbr("scRNA")
            >>> scrna.abbr
            'scRNA'
            >>> scrna.synonyms
            'scRNA|single-cell RNA-seq|single cell RNA sequencing|single-cell transcriptome sequencing|scRNA-seq'
            >>> scrna.save()
        """
        pass


class HasParents:
    """Base class for hierarchical registries (ontologies)."""

    def view_parents(
        self,
        field: StrField | None = None,
        with_children: bool = False,
        distance: int = 5,
    ):
        """View parents in a graph.

        Args:
            field: Field to display on graph
            with_children: Also show children.
            distance: Maximum distance still shown.

        There are two types of registries with a `parents` field:

        - Ontological hierarchies: :class:`~lamindb.ULabel` (project & sub-project), :class:`~bionty.CellType` (cell type & subtype), ...
        - Procedural/temporal hierarchies: :class:`~lamindb.Transform` (preceding transform & successing transform), ...

        See Also:
            - :doc:`docs:data-flow`
            - :doc:`/tutorial`

        Examples:
            >>> import bionty as bt
            >>> bt.Tissue.from_source(name="subsegmental bronchus").save()
            >>> record = bt.Tissue.filter(name="respiratory tube").one()
            >>> record.view_parents()
            >>> tissue.view_parents(with_children=True)
        """
        pass


# rename to Registry once we're through a transition period starting 2024-07-20
class RecordMeta(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        return new_class

    # below creates a sensible auto-complete behavior that differs across the
    # class and instance level in Jupyter Editors it doesn't have any effect for
    # static type analyzer like pylance used in VSCode
    def __dir__(cls):
        # this is needed to bring auto-complete on the class-level back
        # https://laminlabs.slack.com/archives/C04FPE8V01W/p1717535625268849
        # Filter class attributes, excluding instance methods

        exclude_instance_methods = IS_RUN_FROM_IPYTHON
        # https://laminlabs.slack.com/archives/C04FPE8V01W/p1721134595920959

        def include_attribute(attr_name, attr_value):
            if attr_name.startswith("__"):
                return False
            if exclude_instance_methods and callable(attr_value):
                return isinstance(attr_value, (classmethod, staticmethod, type))
            return True

        result = [
            attr_name
            for attr_name, attr_value in cls.__dict__.items()
            if include_attribute(attr_name, attr_value)
        ]
        # Add non-dunder attributes from RecordMeta
        for attr in dir(RecordMeta):
            if not attr.startswith("__") and attr not in result:
                result.append(attr)
        return result

    def __repr__(cls) -> str:
        """Shows fields.

        Divided into several parts:
        1. Header
        2. Basic fields where we first show class specific fields and then base class fields
        3. Relational fields where we show class specific relational fields and then base class fields
        4. External schema fields where we show loaded schemas such as Bionty, wetlab and others
        """

        def _get_type_for_field(field_name: str) -> str:
            field = cls._meta.get_field(field_name)
            related_model_name = (
                field.related_model.__name__
                if hasattr(field, "related_model") and field.related_model
                else None
            )
            return (
                related_model_name if related_model_name else field.get_internal_type()
            )

        def _get_base_class_fields(cls: models.Model) -> list[str]:
            return [
                field.name
                for base in cls.__bases__
                if hasattr(base, "_meta")
                for field in base._meta.get_fields()
            ]

        def _reorder_fields_by_class(fields_to_order: list[Field]) -> list[Field]:
            """Reorders the fields so that base class fields come last."""
            non_base_class_fields = [
                field
                for field in fields_to_order
                if field.name not in _get_base_class_fields(cls)
            ]
            found_base_class_fields = [
                field
                for field in fields_to_order
                if field.name in _get_base_class_fields(cls)
            ]
            return non_base_class_fields + found_base_class_fields

        # ---Header---
        repr_str = f"{colors.green(cls.__name__)}\n"

        # ---Basic fields---
        basic_fields = [
            field
            for field in cls._meta.get_fields()
            if not (
                isinstance(field, ManyToOneRel)
                or isinstance(field, ManyToManyRel)
                or isinstance(field, ManyToManyField)
                or isinstance(field, ForeignKey)
                or field.name.startswith("_")
            )
        ]
        basic_fields = _reorder_fields_by_class(basic_fields)

        repr_str += f"  {colors.italic('Basic fields')}\n"
        if basic_fields:
            repr_str += "".join(
                [
                    f"    .{field_name.name}: {_get_type_for_field(field_name.name)}\n"
                    for field_name in basic_fields
                ]
            )

        # ---Relational fields---
        relational_fields = (ManyToOneRel, ManyToManyRel, ManyToManyField, ForeignKey)

        class_specific_relational_fields = [
            field
            for field in cls._meta.fields + cls._meta.many_to_many
            if isinstance(field, relational_fields)
            and not field.name.startswith("links_")
        ]

        non_class_specific_relational_fields = [
            field
            for field in cls._meta.get_fields()
            if isinstance(field, relational_fields)
            and not field.name.startswith("links_")
        ]
        non_class_specific_relational_fields = _reorder_fields_by_class(
            non_class_specific_relational_fields
        )

        # Ensure that class specific fields (e.g. Artifact) come before non-class specific fields (e.g. collection)
        filtered_non_class_specific = [
            field
            for field in non_class_specific_relational_fields
            if field not in class_specific_relational_fields
        ]
        ordered_relational_fields = (
            class_specific_relational_fields + filtered_non_class_specific
        )

        non_external_schema_fields = []
        external_schema_fields = []
        for field in ordered_relational_fields:
            field_name = repr(field).split(": ")[1][:-1]
            if field_name.count(".") == 1 and "lnschema_core" not in field_name:
                external_schema_fields.append(field)
            else:
                non_external_schema_fields.append(field)

        def _get_related_field_type(field) -> str:
            field_type = (
                field.related_model.__get_name_with_schema__()
                .replace(
                    "Artifact", ""
                )  # some fields have an unnecessary 'Artifact' in their name
                .replace(
                    "Collection", ""
                )  # some fields have an unnecessary 'Collection' in their name
            )
            return (
                _get_type_for_field(field.name)
                if not field_type.strip()
                else field_type
            )

        non_external_schema_fields_formatted = [
            f"    .{field.name}: {_get_related_field_type(field)}\n"
            for field in non_external_schema_fields
        ]
        external_schema_fields_formatted = [
            f"    .{field.name}: {_get_related_field_type(field)}\n"
            for field in external_schema_fields
        ]

        # Non-external relational fields
        if non_external_schema_fields:
            repr_str += f"  {colors.italic('Relational fields')}\n"
            repr_str += "".join(non_external_schema_fields_formatted)

        # External relational fields
        external_schemas = set()
        for field in external_schema_fields_formatted:
            field_type = field.split(":")[1].split()[0]
            external_schemas.add(field_type.split(".")[0])

        if external_schemas:
            # We want Bionty to show up before other schemas
            external_schemas = (
                ["bionty"] + sorted(external_schemas - {"bionty"})  # type: ignore
                if "bionty" in external_schemas
                else sorted(external_schemas)
            )
            for ext_schema in external_schemas:
                ext_schema_fields = [
                    field
                    for field in external_schema_fields_formatted
                    if ext_schema in field
                ]

                if ext_schema_fields:
                    repr_str += (
                        f"  {colors.italic(f'{ext_schema.capitalize()} fields')}\n"
                    )
                    repr_str += "".join(ext_schema_fields)

        repr_str = repr_str.rstrip("\n")

        return repr_str

    def from_values(
        cls,
        values: ListLike,
        field: StrField | None = None,
        create: bool = False,
        organism: Record | str | None = None,
        source: Record | None = None,
        mute: bool = False,
    ) -> list[Record]:
        """Bulk create validated records by parsing values for an identifier (a name. n id, etc.).

        Args:
            values: A list of values for an identifier, e.g.
                `["name1", "name2"]`.
            field: A `Record` field to look up, e.g., `bt.CellMarker.name`.
            create: Whether to create records if they don't exist.
            organism: A `bionty.Organism` name or record.
            source: A `bionty.Source` record.
            mute: Do not show logging.

        Returns:
            A list of validated records. For bionty registries. lso returns knowledge-coupled records.

        Notes:
            For more info, see tutorial: :doc:`bio-registries`.

        Examples:

            Bulk create from non-validated values will log warnings & returns empty list:

            >>> ulabels = ln.ULabel.from_values(["benchmark", "prediction", "test"], field="name")
            >>> assert len(ulabels) == 0

            Bulk create records from validated values returns the corresponding existing records:

            >>> ln.save([ln.ULabel(name=name) for name in ["benchmark", "prediction", "test"]])
            >>> ulabels = ln.ULabel.from_values(["benchmark", "prediction", "test"], field="name")
            >>> assert len(ulabels) == 3

            Bulk create records from public reference:

            >>> import bionty as bt
            >>> records = bt.CellType.from_values(["T cell", "B cell"], field="name")
            >>> records
        """
        pass

    def lookup(
        cls,
        field: StrField | None = None,
        return_field: StrField | None = None,
    ) -> NamedTuple:
        """Return an auto-complete object for a field.

        Args:
            field: The field to look up the values for. Defaults to first string field.
            return_field: The field to return. If `None`, returns the whole record.

        Returns:
            A `NamedTuple` of lookup information of the field values with a
            dictionary converter.

        See Also:
            :meth:`~lamindb.core.Record.search`

        Examples:
            >>> import bionty as bt
            >>> bt.settings.organism = "human"
            >>> bt.Gene.from_source(symbol="ADGB-DT").save()
            >>> lookup = bt.Gene.lookup()
            >>> lookup.adgb_dt
            >>> lookup_dict = lookup.dict()
            >>> lookup_dict['ADGB-DT']
            >>> lookup_by_ensembl_id = bt.Gene.lookup(field="ensembl_gene_id")
            >>> genes.ensg00000002745
            >>> lookup_return_symbols = bt.Gene.lookup(field="ensembl_gene_id", return_field="symbol")
        """
        pass

    def filter(cls, **expressions) -> QuerySet:
        """Query records (see :doc:`records`).

        Args:
            expressions: Fields and values passed as Django query expressions.

        Returns:
            A :class:`~lamindb.core.QuerySet`.

        See Also:
            - Guide: :doc:`records`
            - Django documentation: `Queries <https://docs.djangoproject.com/en/4.2/topics/db/queries/>`__

        Examples:
            >>> ln.ULabel(name="my ulabel").save()
            >>> ulabel = ln.ULabel.filter(name="my ulabel").one()
        """
        pass

    def get(cls, idlike: int | str) -> Record:
        """Get a single record.

        Args:
            idlike: Either a uid stub.  uid or an integer id.

        Returns:
            A record.

        See Also:
            - Guide: :doc:`records`
            - Django documentation: `Queries <https://docs.djangoproject.com/en/4.2/topics/db/queries/>`__

        Examples:
            >>> ulabel = ln.ULabel.get("2riu039")
        """
        pass

    def df(
        cls, include: str | list[str] | None = None, join: str = "inner"
    ) -> pd.DataFrame:
        """Convert to ``pd.DataFrame``.

        By default, shows all direct fields, except ``created_at``.

        If you'd like to include related fields, use parameter ``include``.

        Args:
            include: Related fields to include as columns. Takes strings of
                form ``"labels__name"``, ``"cell_types__name"``, etc. or a list
                of such strings.
            join: The `join` parameter of `pandas`.

        Examples:
            >>> labels = [ln.ULabel(name="Label {i}") for i in range(3)]
            >>> ln.save(labels)
            >>> ln.ULabel.filter().df(include=["created_by__name"])
        """
        pass

    def search(
        cls,
        string: str,
        *,
        field: StrField | None = None,
        limit: int | None = 20,
        case_sensitive: bool = False,
    ) -> QuerySet:
        """Search.

        Args:
            string: The input string to match against the field ontology values.
            field: The field or fields to search. Search all string fields by default.
            limit: Maximum amount of top results to return.
            case_sensitive: Whether the match is case sensitive.

        Returns:
            A sorted `DataFrame` of search results with a score in column `score`.
            If `return_queryset` is `True`.  `QuerySet`.

        See Also:
            :meth:`~lamindb.core.Record.filter`
            :meth:`~lamindb.core.Record.lookup`

        Examples:
            >>> ulabels = ln.ULabel.from_values(["ULabel1", "ULabel2", "ULabel3"], field="name")
            >>> ln.save(ulabels)
            >>> ln.ULabel.search("ULabel2")
        """
        pass

    def using(
        cls,
        instance: str,
    ) -> QuerySet:
        """Use a non-default LaminDB instance.

        Args:
            instance: An instance identifier of form "account_handle/instance_name".

        Examples:
            >>> ln.ULabel.using("account_handle/instance_name").search("ULabel7", field="name")
                        uid    score
            name
            ULabel7  g7Hk9b2v  100.0
            ULabel5  t4Jm6s0q   75.0
            ULabel6  r2Xw8p1z   75.0
        """
        pass

    def __get_schema_name__(cls) -> str:
        schema_module_name = cls.__module__.split(".")[0]
        schema_name = schema_module_name.replace("lnschema_", "")
        return schema_name

    def __get_name_with_schema__(cls) -> str:
        schema_name = cls.__get_schema_name__()
        if schema_name == "core":
            schema_prefix = ""
        else:
            schema_prefix = f"{schema_name}."
        return f"{schema_prefix}{cls.__name__}"


class Record(models.Model, metaclass=RecordMeta):
    """Record base class.

    Extends ``django.db.models.Model``.

    Why does LaminDB call it `Record` and not `Model`? The term "Record" can't lead to
    confusion with statistical, machine learning or biological models.
    """

    def save(self, *args, **kwargs) -> Record:
        """Save.

        Always saves to the default database.
        """
        # we need this here because we're using models also from plain
        # django outside of lamindb
        super().save(*args, **kwargs)
        return self

    class Meta:
        abstract = True


class FeatureManager:
    """Feature manager."""

    pass


class ParamManager:
    """Param manager."""

    pass


class FeatureManagerArtifact(FeatureManager):
    """Feature manager."""

    pass


class FeatureManagerCollection(FeatureManager):
    """Feature manager."""

    pass


class ParamManagerArtifact(ParamManager):
    """Param manager."""

    pass


class ParamManagerRun(ParamManager):
    """Param manager."""

    pass


class HasFeatures:
    """Base class linking features, in particular, for :class:`~lamindb.Artifact` & :class:`~lamindb.Collection`."""

    features: FeatureManager = FeatureManager  # type: ignore
    """Feature manager.

    Features denote dataset dimensions, i.e., the variables that measure labels
    & numbers.

    Annotate with features & values::

       artifact.features.add_values({
            "species": organism,  # here, organism is an Organism record
            "scientist": ['Barbara McClintock', 'Edgar Anderson'],
            "temperature": 27.6,
            "study": "Study 0: initial plant gathering"
       })

    Query for features & values::

        ln.Artifact.features.filter(scientist="Barbara McClintock")

    Features may or may not be part of the artifact content in storage. For
    instance, the :class:`~lamindb.Curate` flow validates the columns of a
    `DataFrame`-like artifact and annotates it with features corresponding to
    these columns. `artifact.features.add_values`, by contrast, does not
    validate the content of the artifact.

    """

    @property
    def labels(self) -> LabelManager:
        """Label manager.

        To annotate with labels, you typically use the registry-specific accessors,
        for instance :attr:`~lamindb.Artifact.ulabels`::

            candidate_marker_study = ln.ULabel(name="Candidate marker study").save()
            artifact.ulabels.add(candidate_marker_study)

        Similarly, you query based on these accessors::

            ln.Artifact.filter(ulabels__name="Candidate marker study").all()

        The `.labels` accessor allows you to associate labels of any registry with features::

            study = ln.Feature(name="study", dtype="cat").save()
            artifact.labels.add(candidate_marker_study, study)
        """
        from lamindb.core._label_manager import LabelManager

        return LabelManager(self)

    def describe(self) -> None:
        """Describe relations of data record.

        Examples:
            >>> ln.Artifact(ln.core.datasets.file_jpg_paradisi05(), description="paradisi05").save()
            >>> artifact = ln.Artifact.filter(description="paradisi05").one()
            >>> ln.save(ln.ULabel.from_values(["image", "benchmark", "example"], field="name"))
            >>> ulabels = ln.ULabel.filter(name__in=["image", "benchmark", "example"]).all()
            >>> artifact.ulabels.set(ulabels)
            >>> artifact.describe()
        """
        pass


class HasParams:
    """Base class linking params."""

    params: ParamManager = ParamManager  # type: ignore
    """Param manager.

    What `.features` is to dataset-like artifacts, `.params` is to model-like artifacts.

    Annotate with params & values::

        artifact.params.add_values({
            "hidden_size": 32,
            "bottleneck_size": 16,
            "batch_size": 32
        })
    """


# -------------------------------------------------------------------------------------
# A note on required fields at the Record level
#
# As Django does most of its validation on the Form-level, it doesn't offer functionality
# for validating the integrity of an Record object upon instantation (similar to pydantic)
#
# For required fields, we define them as commonly done on the SQL level together
# with a validator in Record (validate_required_fields)
#
# This goes against the Django convention, but goes with the SQLModel convention
# (Optional fields can be null on the SQL level, non-optional fields cannot)
#
# Due to Django's convention where CharFieldAttr has pre-configured (null=False, default=""), marking
# a required field necessitates passing `default=None`. Without the validator it would trigger
# an error at the SQL-level, with it, it triggers it at instantiation

# -------------------------------------------------------------------------------------
# A note on class and instance methods of core Record
#
# All of these are defined and tested within lamindb, in files starting with _{orm_name}.py

# -------------------------------------------------------------------------------------
# A note on maximal lengths of char fields
#
# 100 characters:
#     "Raindrops pitter-pattered on the windowpane, blurring the"
#     "city lights outside, curled up with a mug."
# A good maximal length for a name (title).
#
# 150 characters: We choose this for name maximal length because some users like long names.
#
# 255 characters:
#     "In creating a precise 255-character paragraph, one engages in"
#     "a dance of words, where clarity meets brevity. Every syllable counts,"
#     "illustrating the skill in compact expression, ensuring the essence of the"
#     "message shines through within the exacting limit."
# This is a good maximal length for a description field.


class User(Record, CanValidate):
    """Users.

    All data in this registry is synched from `lamin.ai` to ensure a universal
    user identity. There is no need to manually create records.

    Examples:

        Query a user by handle:

        >>> user = ln.User.filter(handle="testuser1").one()
        >>> user
    """

    _name_field: str = "handle"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, db_index=True, max_length=8, default=None)
    """Universal id, valid across DB instances."""
    handle: str = CharField(max_length=30, unique=True, db_index=True, default=None)
    """Universal handle, valid across DB instances (required)."""
    name: str = CharField(max_length=150, db_index=True, null=True, default=None)
    """Name (optional)."""  # has to match hub specification, where it's also optional
    created_at: datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at: datetime = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""

    @overload
    def __init__(
        self,
        handle: str,
        email: str,
        name: str | None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class Storage(Record, TracksRun, TracksUpdates):
    """Storage locations.

    A storage location is either a directory/folder (local or in the cloud) or
    an entire S3/GCP bucket.

    A LaminDB instance can manage and link multiple storage locations. But any
    storage location is managed by *at most one* LaminDB instance.

    .. dropdown:: Managed vs. linked storage locations

        The LaminDB instance can update & delete artifacts in managed storage
        locations but merely read artifacts in linked storage locations.

        When you transfer artifacts from another instance, the default is to
        only copy metadata into the target instance, but merely link the data.

        The `instance_uid` field indicates the managing LaminDB instance of a
        storage location.

        When you delete a LaminDB instance, you'll be warned about data in managed
        storage locations while data in linked storage locations is ignored.

    See Also:
        :attr:`~lamindb.core.Settings.storage`
            Default storage.
        :attr:`~lamindb.setup.core.StorageSettings`
            Storage settings.

    Examples:

        Configure the default storage location upon initiation of a LaminDB instance::

            lamin init --storage ./mydata # or "s3://my-bucket" or "gs://my-bucket"

        View the default storage location:

        >>> ln.settings.storage
        PosixPath('/home/runner/work/lamindb/lamindb/docs/guide/mydata')

        Dynamically change the default storage:

        >>> ln.settings.storage = "./storage_2" # or a cloud bucket
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    _name_field: str = "root"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, max_length=12, default=base62_12, db_index=True)
    """Universal id, valid across DB instances."""
    # we are very conservative here with 255 characters
    root: str = CharField(max_length=255, db_index=True, unique=True, default=None)
    """Root path of storage. n s3 path.  local path, etc. (required)."""
    description: str = CharField(max_length=255, db_index=True, null=True, default=None)
    """A description of what the storage location is used for (optional)."""
    type: str = CharField(max_length=30, db_index=True)
    """Can be "local" vs. "s3" vs. "gs"."""
    region: str = CharField(max_length=64, db_index=True, null=True, default=None)
    """Cloud storage region, if applicable."""
    instance_uid: str = CharField(max_length=12, db_index=True, null=True, default=None)
    """Instance that manages this storage location."""

    @overload
    def __init__(
        self,
        root: str,
        type: str,
        region: str | None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

    @property
    def path(self) -> Path | UPath:
        """Bucket or folder path.

        Cloud storage bucket:

        >>> ln.Storage("s3://my-bucket").save()

        Directory/folder in cloud storage:

        >>> ln.Storage("s3://my-bucket/my-directory").save()

        Local directory/folder:

        >>> ln.Storage("./my-directory").save()
        """
        pass


class Transform(Record, HasParents, IsVersioned):
    """Data transformations.

    A transform can refer to a Python function, a script, notebook, or a
    pipeline. If you execute a transform, you generate a run
    (:class:`~lamindb.Run`). A run has input and output data.

    A pipeline is typically created with a workflow tool (Nextflow, Snakemake,
    Prefect, Flyte, MetaFlow, redun, Airflow, ...) and stored in a versioned
    repository.

    Transforms are versioned so that a given transform maps 1:1 to a specific
    version of code.

    .. dropdown:: Can I sync transforms to git?

        If you switch on
        :attr:`~lamindb.core.Settings.sync_git_repo` a script-like transform is
        synched to its hashed state in a git repository upon calling `ln.track()`.

    The definition of transforms and runs is consistent the OpenLineage
    specification where a :class:`~lamindb.Transform` record would be called a
    "job" and a :class:`~lamindb.Run` record a "run".

    Args:
        name: `str` A name or title.
        key: `str | None = None` A short name or path-like semantic key.
        version: `str | None = None` A version.
        type: `TransformType | None = "pipeline"` See :class:`~lamindb.core.types.TransformType`.
        is_new_version_of: `Transform | None = None` An old version of the transform.

    See Also:
        :meth:`~lamindb.track`
            Globally track a script, notebook or pipeline run.
        :class:`~lamindb.Run`
            Executions of transforms.

    Notes:
        - :doc:`docs:track`
        - :doc:`docs:data-flow`
        - :doc:`docs:redun`
        - :doc:`docs:nextflow`
        - :doc:`docs:snakemake`

    Examples:

        Create a transform for a pipeline:

        >>> transform = ln.Transform(name="Cell Ranger", version="7.2.0", type="pipeline")
        >>> transform.save()

        Create a transform from a notebook:

        >>> ln.track()

        View parents of a transform:

        >>> transform.view_parents()
    """

    class Meta(Record.Meta, IsVersioned.Meta):
        abstract = False

    _len_stem_uid: int = 12
    _len_full_uid: int = 16
    _name_field: str = "name"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(
        unique=True, db_index=True, max_length=_len_full_uid, default=None
    )
    """Universal id."""
    name: str = CharField(max_length=150, db_index=True, null=True, default=None)
    """A name or title. For instance.  pipeline name, notebook title, etc."""
    key: str = CharField(max_length=120, db_index=True, null=True, default=None)
    """A key for concise reference & versioning (optional)."""
    description: str = CharField(max_length=255, null=True, default=None)
    """A description (optional)."""
    type: TransformType = CharField(
        max_length=20,
        db_index=True,
        default="pipeline",
    )
    """:class:`~lamindb.core.types.TransformType` (default `"pipeline"`)."""
    _source_code_artifact: Artifact = models.ForeignKey(
        "Artifact", PROTECT, default=None, null=True, related_name="_source_code_of"
    )
    """Source code of the transform if stored as artifact within LaminDB.

    .. versionchanged:: 0.75
       Made private and deprecated for future removal.
    """
    source_code: str | None = TextField(null=True, default=None)
    """Source code of the transform.

    .. versionchanged:: 0.75
       The `source_code` field is no longer an artifact, but a text field.
    """
    hash: str | None = CharField(
        max_length=HASH_LENGTH, db_index=True, null=True, default=None
    )
    reference: str = CharField(max_length=255, db_index=True, null=True, default=None)
    """Reference for the transform, e.g..  URL."""
    reference_type: str = CharField(
        max_length=25, db_index=True, null=True, default=None
    )
    """Type of reference, e.g., 'url' or 'doi'."""
    ulabels: ULabel = models.ManyToManyField("ULabel", related_name="transforms")
    parents: Transform = models.ManyToManyField(
        "self", symmetrical=False, related_name="children"
    )
    """Parent transforms (predecessors) in data flow.

    These are auto-populated whenever a transform loads an artifact or collection as run input.
    """
    created_at: datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at: datetime = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by: User = models.ForeignKey(User, PROTECT, default=current_user_id)
    """Creator of record. :class:`~lamindb.User`"""

    @overload
    def __init__(
        self,
        name: str,
        key: str | None = None,
        version: str | None = None,
        type: TransformType | None = None,
        is_new_version_of: Transform | None = None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

    @property
    def latest_run(self) -> Run:
        """The latest run of this transform."""
        pass


class Param(Record, CanValidate, TracksRun, TracksUpdates):
    """Parameters of runs & models akin to Feature for datasets."""

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    _name_field: str = "name"

    name: str = CharField(max_length=100, db_index=True)
    dtype: str = CharField(max_length=64, db_index=True, default=None)
    """Data type ("number", "cat", "int", "float", "bool", "datetime").

    For categorical types, can define from which registry values are
    sampled, e.g., `cat[ULabel]` or `cat[bionty.CellType]`.
    """


class ParamValue(Record):
    """Run parameter values akin to FeatureValue for artifacts."""

    class Meta:
        unique_together = ("param", "value")

    _name_field: str = "value"

    param: Param = models.ForeignKey(Param, CASCADE)
    value: Any = models.JSONField()  # stores float, integer, boolean or datetime
    # it'd be confusing and hard to populate a run here because these
    # values are typically created upon creating a run
    # hence, ParamValue does _not_ inherit from TracksRun but manually
    # adds created_at & created_by
    # because ParamValue cannot be updated, we don't need updated_at
    created_at: datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    created_by: User = models.ForeignKey(User, PROTECT, default=current_user_id)
    """Creator of record. :class:`~lamindb.User`"""


class Run(Record, HasParams):
    """Runs of transforms.

    Args:
        transform: `Transform` A :class:`~lamindb.Transform` record.
        reference: `str | None = None` For instance. n external ID or a download URL.
        reference_type: `str | None = None` For instance, `redun_id`, `nextflow_id` or `url`.

    See Also:
        :meth:`~lamindb.track`
            Track global run & transform records for a notebook or pipeline.

    Notes:
        See guide: :doc:`docs:data-flow`.

        A run can have inputs and outputs:

        - References to outputs are stored in the `run` field of registries.
        - References to inputs are stored in the `input_of` field of :class:`~lamindb.Artifact` and :class:`~lamindb.Collection`.

    Examples:

        >>> ln.Transform(name="Cell Ranger", version="7.2.0", type="pipeline").save()
        >>> transform = ln.Transform.filter(name="Cell Ranger", version="7.2.0").one()
        >>> run = ln.Run(transform)

        Create a global run context:

        >>> ln.track(transform=transform)
        >>> ln.core.run_context.run  # global available run

        Track a notebook run:

        >>> ln.track()  # Jupyter notebook metadata is automatically parsed
        >>> ln.core.context.run
    """

    _name_field: str = "started_at"

    params: ParamManager = ParamManagerRun  # type: ignore

    id: int = models.BigAutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, db_index=True, max_length=20, default=base62_20)
    """Universal id, valid across DB instances."""
    transform = models.ForeignKey(Transform, CASCADE, related_name="runs")
    """The transform :class:`~lamindb.Transform` that is being run."""
    started_at: datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    """Start time of run."""
    finished_at: datetime = models.DateTimeField(db_index=True, null=True, default=None)
    """Finished time of run."""
    created_by: User = models.ForeignKey(User, CASCADE, default=current_user_id)
    """Creator of run. :class:`~lamindb.User`"""
    _param_values: ParamValue = models.ManyToManyField(
        ParamValue, through="RunParamValue", related_name="runs"
    )
    """Parameter values."""
    # we don't want to make below a OneToOne because there could be the same trivial report
    # generated for many different runs
    report: Artifact = models.ForeignKey(
        "Artifact", PROTECT, default=None, null=True, related_name="report_of"
    )
    """Report of run, e.g.. n html file."""
    environment: Artifact = models.ForeignKey(
        "Artifact", PROTECT, default=None, null=True, related_name="environment_of"
    )
    """Computational environment for the run.

    For instance.  `Dockerfile`.  docker image.  `requirements.txt`. n `environment.yml`, etc.
    """
    is_consecutive: bool = models.BooleanField(null=True, default=None)
    """Indicates whether code was consecutively executed. Is relevant for notebooks."""
    reference: str = CharField(max_length=255, db_index=True, null=True, default=None)
    """A reference like a URL or external ID (such as from a workflow manager)."""
    reference_type: str = CharField(
        max_length=25, db_index=True, null=True, default=None
    )
    """Type of reference, e.g..  workflow manager execution ID."""
    created_at: datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of first creation. Mismatches ``started_at`` if the run is re-run."""

    @overload
    def __init__(
        self,
        transform: Transform,
        reference: str | None = None,
        reference_type: str | None = None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class ULabel(Record, HasParents, CanValidate, TracksRun, TracksUpdates):
    """Universal labels.

    Args:
        name: `str` A name.
        description: `str` A description.
        reference: `str | None = None` For instance. n external ID or a URL.
        reference_type: `str | None = None` For instance, `"url"`.

    A `ULabel` record provides the easiest way to annotate a dataset
    with a label: `"My project"`, `"curated"`, or `"Batch X"`:

        >>> my_project = ULabel(name="My project")
        >>> my_project.save()
        >>> artifact.ulabels.add(my_project)

    Often, a ulabel is measured *within* a dataset. For instance, an artifact
    might characterize 2 species of the Iris flower (`"setosa"` &
    `"versicolor"`) measured by a `"species"` feature. Use the
    :class:`~lamindb.Curate` flow to automatically parse, validate, and
    annotate with labels that are contained in `DataFrame` or `AnnData`
    artifacts.

    See :doc:`tutorial2` to learn more.

    .. note::

        If you work with complex entities like cell lines, cell types, tissues,
        etc., consider using the pre-defined biological registries in
        :mod:`bionty` to label artifacts & collections.

        If you work with biological samples, likely, the only sustainable way of
        tracking metadata, is to create a custom schema module.

    See Also:
        :meth:`~lamindb.Feature`
            Dimensions of measurement for artifacts & collections.
        :attr:`~lamindb.core.HasFeatures.labels`
            Label manager of an artifact or collection.

    Examples:

        Create a new label:

        >>> my_project = ln.ULabel(name="My project")
        >>> my_project.save()

        Label a artifact without associating it to a feature:

        >>> ulabel = ln.ULabel.filter(name="My project").one()
        >>> artifact = ln.Artifact("./myfile.csv")
        >>> artifact.save()
        >>> artifact.ulabels.add(ulabel)

        Organize labels in a hierarchy:

        >>> ulabels = ln.ULabel.lookup()  # create a lookup
        >>> is_project = ln.ULabel(name="is_project")  # create a super-category `is_project`
        >>> is_project.save()
        >>> ulabels.my_project.parents.add(is_project)

        Query by `ULabel`:

        >>> ln.Artifact.filter(ulabels=project).first()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    _name_field: str = "name"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, db_index=True, max_length=8, default=base62_8)
    """A universal random id, valid across DB instances."""
    name: str = CharField(max_length=150, db_index=True, unique=True, default=None)
    """Name or title of ulabel (required)."""
    description: str = TextField(null=True, default=None)
    """A description (optional)."""
    reference: str = CharField(max_length=255, db_index=True, null=True, default=None)
    """A reference like URL or external ID."""
    reference_type: str = CharField(
        max_length=25, db_index=True, null=True, default=None
    )
    """Type of reference, e.g., donor_id from Vendor X."""
    parents: ULabel = models.ManyToManyField(
        "self", symmetrical=False, related_name="children"
    )
    """Parent labels, useful to hierarchically group labels (optional)."""

    @overload
    def __init__(
        self,
        name: str,
        description: str | None = None,
        reference: str | None = None,
        reference_type: str | None = None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass


class Feature(Record, CanValidate, TracksRun, TracksUpdates):
    """Dataset dimensions.

    Features denote dataset dimensions, i.e., the variables that measure labels &
    numbers.

    The `Feature` registry helps to

    1. manage metadata of features
    2. annotate datasets by whether they measured a feature

    Learn more: :doc:`tutorial2`.

    Args:
        name: `str` Name of the feature, typically.  column name.
        type: `str | list[Type[Record]]` Data type ("number", "cat", "int", "float", "bool", "datetime").
            For categorical types, can define from which registry values are
            sampled, e.g., `cat[ULabel]` or `cat[bionty.CellType]`.
        unit: `str | None = None` Unit of measure, ideally SI (`"m"`, `"s"`, `"kg"`, etc.) or `"normalized"` etc.
        description: `str | None = None` A description.
        synonyms: `str | None = None` Bar-separated synonyms.

    Note:

        For more control, you can use :mod:`bionty` registries to manage basic
        biological entities like genes, proteins & cell markers. Or you define
        custom registries to manage high-level derived features like gene sets.

    See Also:
        :meth:`~lamindb.Feature.from_df`
            Create feature records from DataFrame.
        :attr:`~lamindb.core.HasFeatures.features`
            Feature manager of an artifact or collection.
        :class:`~lamindb.ULabel`
            Universal labels.
        :class:`~lamindb.FeatureSet`
            Feature sets.

    Example:

        >>> ln.Feature("cell_type_by_expert", dtype="cat", description="Expert cell type annotation").save()

    Hint:

        *Features* and *labels* denote two ways of using entities to organize data:

        1. A feature qualifies *what* is measured, i.e..  numerical or categorical random variable
        2. A label *is* a measured value, i.e..  category

        Consider annotating a dataset by that it measured expression of 30k
        genes: genes relate to the dataset as feature identifiers through a
        feature set with 30k members. Now consider annotating the artifact by
        whether that it measured the knock-out of 3 genes: here, the 3 genes act
        as labels of the dataset.

        Re-shaping data can introduce ambiguity among features & labels. If this
        happened. sk yourself what the joint measurement was: a feature
        qualifies variables in a joint measurement. The canonical data matrix
        lists jointly measured variables in the columns.

    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    _name_field: str = "name"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, db_index=True, max_length=12, default=base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=150, db_index=True, default=None, unique=True)
    """Name of feature (required)."""
    dtype: str = CharField(max_length=64, db_index=True, default=None)
    """Data type ("number", "cat", "int", "float", "bool", "datetime").

    For categorical types, can define from which registry values are
    sampled, e.g., `cat[ULabel]` or `cat[bionty.CellType]`.
    """
    unit: str = CharField(max_length=30, db_index=True, null=True, default=None)
    """Unit of measure, ideally SI (`m`, `s`, `kg`, etc.) or 'normalized' etc. (optional)."""
    description: str = TextField(db_index=True, null=True, default=None)
    """A description."""
    synonyms: str = TextField(null=True, default=None)
    """Bar-separated (|) synonyms (optional)."""
    # we define the below ManyToMany on the feature model because it parallels
    # how other registries (like Gene, Protein, etc.) relate to FeatureSet
    # it makes the API more consistent
    feature_sets: FeatureSet = models.ManyToManyField(
        "FeatureSet", through="FeatureSetFeature", related_name="features"
    )
    """Feature sets linked to this feature."""

    @overload
    def __init__(
        self,
        name: str,
        type: str | list[type[Record]],
        unit: str | None,
        description: str | None,
        synonyms: str | None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    @classmethod
    def from_df(cls, df: pd.DataFrame, field: FieldAttr | None = None) -> RecordsList:
        """Create Feature records for columns."""
        pass

    def save(self, *args, **kwargs) -> Feature:
        """Save."""
        pass


class FeatureValue(Record, TracksRun):
    """Non-categorical features values.

    Categorical feature values are stored in their respective registries:
    :class:`~lamindb.ULabel`, :class:`~bionty.CellType`, etc.

    Unlike for ULabel, in `FeatureValue`, values are grouped by features. nd
    not by an ontological hierarchy.
    """

    class Meta(Record.Meta, TracksRun.Meta):
        abstract = False
        unique_together = ("feature", "value")

    _name_field: str = "value"

    feature: Feature = models.ForeignKey(Feature, CASCADE, null=True, default=None)
    value: Any = models.JSONField()


class FeatureSet(Record, TracksRun):
    """Feature sets.

    Stores references to sets of :class:`~lamindb.Feature` and other registries
    that may be used to identify features (e.g., class:`~bionty.Gene` or
    class:`~bionty.Protein`).

    .. dropdown:: Why does LaminDB model feature sets, not just features?

        1. Performance: Imagine you measure the same panel of 20k transcripts in
           1M samples. By modeling the panel as a feature set, you can link all
           your artifacts against one feature set and only need to store 1M
           instead of 1M x 20k = 20B links.
        2. Interpretation: Model protein panels, gene panels, etc.
        3. Data integration: Feature sets provide the currency that determines whether two collections can be easily concatenated.

        These reasons do not hold for label sets. Hence, LaminDB does not model label sets.

    Args:
        features: `Iterable[Record]` An iterable of :class:`~lamindb.Feature`
            records to hash, e.g., `[Feature(...), Feature(...)]`. Is turned into
            a set upon instantiation. If you'd like to pass values, use
            :meth:`~lamindb.FeatureSet.from_values` or
            :meth:`~lamindb.FeatureSet.from_df`.
        dtype: `str | None = None` The simple type. Defaults to
            `None` for sets of :class:`~lamindb.Feature` records. nd otherwise
            defaults to `"number"` (e.g., for sets of :class:`~bionty.Gene`).
        name: `str | None = None` A name.

    Note:

        A feature set is identified by the hash of the feature uids in the set.

        A `slot` provides a string key to access feature sets. It's typically the accessor within the registered data object, here `pd.DataFrame.columns`.


    See Also:
        :meth:`~lamindb.FeatureSet.from_values`
            Create from values.
        :meth:`~lamindb.FeatureSet.from_df`
            Create from dataframe columns.

    Examples:

        Create a featureset from df with types:

        >>> df = pd.DataFrame({"feat1": [1, 2], "feat2": [3.1, 4.2], "feat3": ["cond1", "cond2"]})
        >>> feature_set = ln.FeatureSet.from_df(df)

        Create a featureset from features:

        >>> features = ln.Feature.from_values(["feat1", "feat2"], type=float)
        >>> feature_set = ln.FeatureSet(features)

        Create a featureset from feature values:

        >>> import bionty as bt
        >>> feature_set = ln.FeatureSet.from_values(adata.var["ensemble_id"], Gene.ensembl_gene_id, orgaism="mouse")
        >>> feature_set.save()

        Link a feature set to an artifact:

        >>> artifact.features.add_feature_set(feature_set, slot="var")

        Link features to an artifact (will create a featureset under the hood):

        >>> artifact.features.add_values(features)
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    _name_field: str = "name"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, db_index=True, max_length=20, default=None)
    """A universal id (hash of the set of feature values)."""
    name: str = CharField(max_length=150, null=True, default=None)
    """A name (optional)."""
    n = models.IntegerField()
    """Number of features in the set."""
    dtype: str = CharField(max_length=64, null=True, default=None)
    """Data type, e.g., "number", "float", "int". Is `None` for :class:`~lamindb.Feature`.

    For :class:`~lamindb.Feature`, types are expected to be heterogeneous and defined on a per-feature level.
    """
    registry: str = CharField(max_length=120, db_index=True)
    """The registry that stores the feature identifiers, e.g., `'core.Feature'` or `'bionty.Gene'`.

    Depending on the registry, `.members` stores, e.g. `Feature` or `Gene` records.
    """
    hash: str = CharField(
        max_length=HASH_LENGTH, default=None, db_index=True, null=True, unique=True
    )
    """The hash of the set."""

    @overload
    def __init__(
        self,
        features: Iterable[Record],
        dtype: str | None = None,
        name: str | None = None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    @classmethod
    def from_values(  # type: ignore
        cls,
        values: ListLike,
        field: FieldAttr = Feature.name,
        type: str | None = None,
        name: str | None = None,
        mute: bool = False,
        organism: Record | str | None = None,
        source: Record | None = None,
        raise_validation_error: bool = True,
    ) -> FeatureSet:
        """Create feature set for validated features.

        Args:
            values: A list of values, like feature names or ids.
            field: The field of a reference registry to map values.
            type: The simple type. Defaults to
                `None` if reference registry is :class:`~lamindb.Feature`, defaults to
                `"float"` otherwise.
            name: A name.
            organism: An organism to resolve gene mapping.
            source: A public ontology to resolve feature identifier mapping.
            raise_validation_error: Whether to raise a validation error if some values are not valid.

        Raises:
            ValidationError: If some values are not valid.

        Examples:

            >>> features = ["feat1", "feat2"]
            >>> feature_set = ln.FeatureSet.from_values(features)

            >>> genes = ["ENS980983409", "ENS980983410"]
            >>> feature_set = ln.FeatureSet.from_values(features, bt.Gene.ensembl_gene_id, float)
        """
        pass

    @classmethod
    def from_df(
        cls,
        df: pd.DataFrame,
        field: FieldAttr = Feature.name,
        name: str | None = None,
        mute: bool = False,
        organism: Record | str | None = None,
        source: Record | None = None,
    ) -> FeatureSet | None:
        """Create feature set for validated features."""
        pass

    def save(self, *args, **kwargs) -> FeatureSet:
        """Save."""
        pass

    @property
    def members(self) -> QuerySet:
        """A queryset for the individual records of the set."""
        pass


class Artifact(Record, HasFeatures, HasParams, IsVersioned, TracksRun, TracksUpdates):
    """Datasets & models stored as files, folders, or arrays.

    Artifacts manage data in local or remote storage (:doc:`/tutorial`).

    Some artifacts are array-like, e.g., when stored as `.parquet`, `.h5ad`,
    `.zarr`, or `.tiledb`.

    Args:
        data: `UPathStr` A path to a local or remote folder or file.
        type: `Literal["dataset", "model"] | None = None` The artifact type.
        key: `str | None = None` A relative path within default storage,
            e.g., `"myfolder/myfile.fcs"`.
        description: `str | None = None` A description.
        version: `str | None = None` A version string.
        is_new_version_of: `Artifact | None = None` A previous version of the artifact.
        run: `Run | None = None` The run that creates the artifact.

    .. dropdown:: Typical storage formats & their API accessors

        Arrays:

        - Table: `.csv`, `.tsv`, `.parquet`, `.ipc` ⟷ `DataFrame`, `pyarrow.Table`
        - Curated matrix: `.h5ad`, `.h5mu`, `.zrad` ⟷ `AnnData`, `MuData`
        - Generic array: HDF5 group, zarr group, TileDB store ⟷ HDF5, zarr, TileDB loaders

        Non-arrays:

        - Image: `.jpg`, `.png` ⟷ `np.ndarray`, ...
        - Fastq: `.fastq` ⟷ /
        - VCF: `.vcf` ⟷ /
        - QC: `.html` ⟷ /

        You'll find these values in the `suffix` & `accessor` fields.

        LaminDB makes some default choices (e.g., serialize a `DataFrame` as a
        `.parquet` file).

    See Also:
        :class:`~lamindb.Storage`
            Storage locations for artifacts.
        :class:`~lamindb.Collection`
            Collections of artifacts.
        :meth:`~lamindb.Artifact.from_df`
            Create an artifact from a `DataFrame`.
        :meth:`~lamindb.Artifact.from_anndata`
            Create an artifact from an `AnnData`.

    Examples:

        Create an artifact from a path to a file or folder:

        >>> artifact = ln.Artifact("s3://my_bucket/my_folder/my_file.csv", description="My file")
        >>> artifact = ln.Artifact("./my_local_file.jpg", description="My image")
        >>> artifact = ln.Artifact("s3://my_bucket/my_folder", description="My folder")
        >>> artifact = ln.Artifact("./my_local_folder", description="My local folder")

        .. dropdown:: Why does the API look this way?

            It's inspired by APIs building on AWS S3.

            Both boto3 and quilt select a bucket (akin to default storage in LaminDB) and define a target path through a `key` argument.

            In `boto3 <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/upload_file.html>`__::

                # signature: S3.Bucket.upload_file(filepath, key)
                import boto3
                s3 = boto3.resource('s3')
                bucket = s3.Bucket('mybucket')
                bucket.upload_file('/tmp/hello.txt', 'hello.txt')

            In `quilt3 <https://docs.quiltdata.com/api-reference/bucket>`__::

                # signature: quilt3.Bucket.put_file(key, filepath)
                import quilt3
                bucket = quilt3.Bucket('mybucket')
                bucket.put_file('hello.txt', '/tmp/hello.txt')


        Make a new version of an artifact:

        >>> # a non-versioned artifact
        >>> artifact = ln.Artifact(df1, description="My dataframe")
        >>> artifact.save()
        >>> # version an artifact
        >>> new_artifact = ln.Artifact(df2, is_new_version_of=artifact)
        >>> assert new_artifact.stem_uid == artifact.stem_uid
        >>> assert artifact.version == "1"
        >>> assert new_artifact.version == "2"

    """

    class Meta(Record.Meta, IsVersioned.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    _len_full_uid: int = 20
    _len_stem_uid: int = 16
    features: FeatureManager = FeatureManagerArtifact  # type: ignore
    params: ParamManager = ParamManagerArtifact  # type: ignore
    _name_field: str = "description"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, db_index=True, max_length=_len_full_uid)
    """A universal random id (20-char base62 ~ UUID), valid across DB instances."""
    description: str = CharField(max_length=255, db_index=True, null=True, default=None)
    """A description."""
    storage: Storage = models.ForeignKey(Storage, PROTECT, related_name="artifacts")
    """Storage location, e.g. an S3 or GCP bucket or a local directory."""
    key: str = CharField(max_length=255, db_index=True, null=True, default=None)
    """Storage key, the relative path within the storage location."""
    suffix: str = CharField(max_length=30, db_index=True, default=None)
    # Initially, we thought about having this be nullable to indicate folders
    # But, for instance, .zarr is stored in a folder that ends with a .zarr suffix
    """Path suffix or empty string if no canonical suffix exists.

    This is either a file suffix (`".csv"`, `".h5ad"`, etc.) or the empty string "".
    """
    type: ArtifactType | None = CharField(
        max_length=20,
        db_index=True,
        default=None,
        null=True,
    )
    """:class:`~lamindb.core.types.ArtifactType` (default `None`)."""
    _accessor: str = CharField(
        max_length=64, db_index=True, null=True, default=None, db_column="accessor"
    )
    """Default backed or memory accessor, e.g., DataFrame, AnnData."""
    size: int = models.BigIntegerField(null=True, db_index=True)
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    hash: str = CharField(
        max_length=HASH_LENGTH, db_index=True, null=True, default=None
    )
    """Hash or pseudo-hash of artifact content.

    Useful to ascertain integrity and avoid duplication.
    """
    _hash_type: str = CharField(
        max_length=30, db_index=True, null=True, default=None, db_column="hash_type"
    )
    """Type of hash."""
    n_objects: int = models.BigIntegerField(default=None, null=True, db_index=True)
    """Number of objects.

    Typically, this denotes the number of files in an artifact.
    """
    n_observations: int = models.BigIntegerField(default=None, null=True, db_index=True)
    """Number of observations.

    Typically, this denotes the first array dimension.
    """
    ulabels: ULabel = models.ManyToManyField(
        ULabel, through="ArtifactULabel", related_name="artifacts"
    )
    """The ulabels measured in the artifact (:class:`~lamindb.ULabel`)."""
    transform: Transform = models.ForeignKey(
        Transform, PROTECT, related_name="output_artifacts", null=True, default=None
    )
    """:class:`~lamindb.Transform` whose run created the artifact."""
    run: Run = models.ForeignKey(
        Run, PROTECT, related_name="output_artifacts", null=True, default=None
    )
    """:class:`~lamindb.Run` that created the artifact."""
    input_of_runs: Run = models.ManyToManyField(Run, related_name="input_artifacts")
    """Runs that use this artifact as an input."""
    # if the artifact is replicated or update in a new run, we link the previous
    # run in previous_runs
    _previous_runs: Run = models.ManyToManyField(
        "Run", related_name="output_artifacts_with_later_updates"
    )
    """Sequence of runs that created or updated the record."""
    feature_sets: FeatureSet = models.ManyToManyField(
        FeatureSet, related_name="artifacts", through="ArtifactFeatureSet"
    )
    """The feature sets measured in the artifact (:class:`~lamindb.FeatureSet`)."""
    _feature_values: FeatureValue = models.ManyToManyField(
        FeatureValue, through="ArtifactFeatureValue"
    )
    """Non-categorical feature values for annotation."""
    _param_values: ParamValue = models.ManyToManyField(
        ParamValue, through="ArtifactParamValue", related_name="artifacts"
    )
    """Parameter values."""
    visibility: int = models.SmallIntegerField(
        db_index=True, choices=VisibilityChoice.choices, default=1
    )
    """Visibility of artifact record in queries & searches (1 default, 1 hidden, -1 trash)."""
    _key_is_virtual: bool = models.BooleanField(db_column="key_is_virtual")
    """Indicates whether `key` is virtual or part of an actual file path."""

    @overload
    def __init__(
        self,
        data: UPathStr,
        type: ArtifactType | None = None,
        key: str | None = None,
        description: str | None = None,
        is_new_version_of: Artifact | None = None,
        run: Run | None = None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    @property
    def path(self) -> Path:
        """Path.

        File in cloud storage, here AWS S3:

        >>> artifact = ln.Artifact("s3://my-bucket/my-file.csv").save()
        >>> artifact.path
        S3Path('s3://my-bucket/my-file.csv')

        File in local storage:

        >>> ln.Artifact("./myfile.csv", description="myfile").save()
        >>> artifact = ln.Artifact.filter(description="myfile").one()
        >>> artifact.path
        PosixPath('/home/runner/work/lamindb/lamindb/docs/guide/mydata/myfile.csv')
        """
        pass

    @classmethod
    def from_df(
        cls,
        df: pd.DataFrame,
        key: str | None = None,
        description: str | None = None,
        run: Run | None = None,
        version: str | None = None,
        is_new_version_of: Artifact | None = None,
        **kwargs,
    ) -> Artifact:
        """Create from ``DataFrame``, validate & link features.

        For more info, see tutorial: :doc:`/tutorial`.

        Args:
            df: A `DataFrame` object.
            key: A relative path within default storage,
                e.g., `"myfolder/myfile.parquet"`.
            description: A description.
            version: A version string.
            is_new_version_of: An old version of the artifact.
            run: The run that creates the artifact.

        See Also:
            :meth:`~lamindb.Collection`
                Track collections.
            :class:`~lamindb.Feature`
                Track features.

        Examples:
            >>> df = ln.core.datasets.df_iris_in_meter_batch1()
            >>> df.head()
              sepal_length sepal_width petal_length petal_width iris_organism_code
            0        0.051       0.035        0.014       0.002                 0
            1        0.049       0.030        0.014       0.002                 0
            2        0.047       0.032        0.013       0.002                 0
            3        0.046       0.031        0.015       0.002                 0
            4        0.050       0.036        0.014       0.002                 0
            >>> artifact = ln.Artifact.from_df(df, description="Iris flower collection batch1")
            >>> artifact.save()
        """
        pass

    @classmethod
    def from_anndata(
        cls,
        adata: AnnData | UPathStr,
        key: str | None = None,
        description: str | None = None,
        run: Run | None = None,
        version: str | None = None,
        is_new_version_of: Artifact | None = None,
        **kwargs,
    ) -> Artifact:
        """Create from ``AnnData``, validate & link features.

        Args:
            adata: An `AnnData` object or a path of AnnData-like.
            key: A relative path within default storage,
                e.g., `"myfolder/myfile.h5ad"`.
            description: A description.
            version: A version string.
            is_new_version_of: An old version of the artifact.
            run: The run that creates the artifact.

        See Also:

            :meth:`~lamindb.Collection`
                Track collections.
            :class:`~lamindb.Feature`
                Track features.

        Examples:
            >>> import bionty as bt
            >>> bt.settings.organism = "human"
            >>> adata = ln.core.datasets.anndata_with_obs()
            >>> artifact = ln.Artifact.from_anndata(adata, description="mini anndata with obs")
            >>> artifact.save()
        """
        pass

    @classmethod
    def from_mudata(
        cls,
        mdata: MuData,
        key: str | None = None,
        description: str | None = None,
        run: Run | None = None,
        version: str | None = None,
        is_new_version_of: Artifact | None = None,
        **kwargs,
    ) -> Artifact:
        """Create from ``MuData``, validate & link features.

        Args:
            mdata: An `MuData` object.
            key: A relative path within default storage,
                e.g., `"myfolder/myfile.h5mu"`.
            description: A description.
            version: A version string.
            is_new_version_of: An old version of the artifact.
            run: The run that creates the artifact.

        See Also:
            :meth:`~lamindb.Collection`
                Track collections.
            :class:`~lamindb.Feature`
                Track features.

        Examples:
            >>> import bionty as bt
            >>> bt.settings.organism = "human"
            >>> mdata = ln.core.datasets.mudata_papalexi21_subset()
            >>> artifact = ln.Artifact.from_mudata(mdata, description="a mudata object")
            >>> artifact.save()
        """
        pass

    @classmethod
    def from_dir(
        cls,
        path: UPathStr,
        key: str | None = None,
        *,
        run: Run | None = None,
    ) -> list[Artifact]:
        """Create a list of artifact objects from a directory.

        Hint:
            If you have a high number of files (several 100k) and don't want to
            track them individually, create a single :class:`~lamindb.Artifact` via
            ``Artifact(path)`` for them. See, e.g., :doc:`docs:rxrx`.

        Args:
            path: Source path of folder.
            key: Key for storage destination. If `None` and
                directory is in a registered location. n inferred `key` will
                reflect the relative position. If `None` and directory is outside
                of a registered storage location, the inferred key defaults to `path.name`.
            run: A `Run` object.

        Examples:
            >>> dir_path = ln.core.datasets.generate_cell_ranger_files("sample_001", ln.settings.storage)
            >>> artifacts = ln.Artifact.from_dir(dir_path)
            >>> ln.save(artifacts)
        """
        pass

    def replace(
        self,
        data: UPathStr,
        run: Run | None = None,
        format: str | None = None,
    ) -> None:
        """Replace artifact content.

        Args:
            data: A file path.
            run: The run that created the artifact gets
                auto-linked if ``ln.track()`` was called.

        Examples:
            Say we made a change to the content of an artifact, e.g., edited the image
            `paradisi05_laminopathic_nuclei.jpg`.

            This is how we replace the old file in storage with the new file:

            >>> artifact.replace("paradisi05_laminopathic_nuclei.jpg")
            >>> artifact.save()

            Note that this neither changes the storage key nor the filename.

            However, it will update the suffix if it changes.
        """
        pass

    def open(
        self, is_run_input: bool | None = None
    ) -> AnnDataAccessor | BackedAccessor | SOMACollection | SOMAExperiment:
        """Return a cloud-backed data object.

        Notes:
            For more info, see tutorial: :doc:`/arrays`.

        Examples:

            Read AnnData in backed mode from cloud:

            >>> artifact = ln.Artifact.filter(key="lndb-storage/pbmc68k.h5ad").one()
            >>> artifact.open()
            AnnData object with n_obs × n_vars = 70 × 765 backed at 's3://lamindb-ci/lndb-storage/pbmc68k.h5ad'
        """
        pass

    def load(
        self, is_run_input: bool | None = None, stream: bool = False, **kwargs
    ) -> Any:
        """Stage and load to memory.

        Returns in-memory representation if possible, e.g.. n `AnnData` object for an `h5ad` file.

        Examples:

            Load as a `DataFrame`:

            >>> df = ln.core.datasets.df_iris_in_meter_batch1()
            >>> ln.Artifact.from_df(df, description="iris").save()
            >>> artifact = ln.Artifact.filter(description="iris").one()
            >>> artifact.load().head()
            sepal_length sepal_width petal_length petal_width iris_organism_code
            0        0.051       0.035        0.014       0.002                 0
            1        0.049       0.030        0.014       0.002                 0
            2        0.047       0.032        0.013       0.002                 0
            3        0.046       0.031        0.015       0.002                 0
            4        0.050       0.036        0.014       0.002                 0

            Load as an `AnnData`:

            >>> artifact.load()
            AnnData object with n_obs × n_vars = 70 × 765

            Fall back to :meth:`~lamindb.Artifact.cache` if no in-memory representation is configured:

            >>> artifact.load()
            PosixPath('/home/runner/work/lamindb/lamindb/docs/guide/mydata/.lamindb/jb7BY5UJoQVGMUOKiLcn.jpg')
        """
        pass

    def cache(self, is_run_input: bool | None = None) -> Path:
        """Download cloud artifact to local cache.

        Follows synching logic: only caches an artifact if it's outdated in the local cache.

        Returns a path to a locally cached on-disk object (say.  `.jpg` file).

        Examples:

            Sync file from cloud and return the local path of the cache:

            >>> artifact.cache()
            PosixPath('/home/runner/work/Caches/lamindb/lamindb-ci/lndb-storage/pbmc68k.h5ad')
        """
        pass

    def delete(
        self, permanent: bool | None = None, storage: bool | None = None
    ) -> None:
        """Delete.

        A first call to `.delete()` puts an artifact into the trash (sets `visibility` to `-1`).

        A second call permanently deletes the artifact.

        FAQ: :doc:`docs:faq/storage`

        Args:
            permanent: Permanently delete the artifact (skip trash).
            storage: Indicate whether you want to delete the artifact in storage.

        Examples:

            For an `Artifact` object `artifact`, call:

            >>> artifact.delete()
        """
        pass

    def save(self, upload: bool | None = None, **kwargs) -> Artifact:
        """Save to database & storage.

        Args:
            upload: Trigger upload to cloud storage in instances with hybrid
                storage mode.

        Examples:
            >>> artifact = ln.Artifact("./myfile.csv", description="myfile")
            >>> artifact.save()
        """
        pass

    def restore(self) -> None:
        """Restore from trash.

        Examples:

            For any `Artifact` object `artifact`, call:

            >>> artifact.restore()
        """
        pass


# auto-generated through choices()
delattr(Artifact, "get_visibility_display")


class Collection(Record, HasFeatures, IsVersioned, TracksRun, TracksUpdates):
    """Collections of artifacts.

    For more info: :doc:`/tutorial`.

    Args:
        data: `List[Artifact]` A list of artifacts.
        name: `str` A name.
        description: `str | None = None` A description.
        version: `str | None = None` A version string.
        is_new_version_of: `Collection | None = None` An old version of the collection.
        run: `Run | None = None` The run that creates the collection.
        meta: `Artifact | None = None` An artifact that defines metadata for the collection.
        reference: `str | None = None` For instance. n external ID or a URL.
        reference_type: `str | None = None` For instance, `"url"`.

    See Also:
        :class:`~lamindb.Artifact`

    Examples:

        Create a collection from a collection of :class:`~lamindb.Artifact` objects:

        >>> collection = ln.Collection([artifact1. rtifact2], name="My collection")
        >>> collection.save()

        If you have more than 100k artifacts, consider creating a collection directly from the
        directory without creating File records (e.g., here :doc:`docs:rxrx`):

        >>> collection = ln.Artifact("s3://my-bucket/my-images/", name="My collection", meta=df)
        >>> collection.save()

        Make a new version of a collection:

        >>> # a non-versioned collection
        >>> collection = ln.Collection(df1, description="My dataframe")
        >>> collection.save()
        >>> # create new collection from old collection and version both
        >>> new_collection = ln.Collection(df2, is_new_version_of=collection)
        >>> assert new_collection.stem_uid == collection.stem_uid
        >>> assert collection.version == "1"
        >>> assert new_collection.version == "2"
    """

    class Meta(Record.Meta, IsVersioned.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    _len_full_uid: int = 20
    _len_stem_uid: int = 16
    features = FeatureManagerCollection  # type: ignore
    _name_field: str = "name"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(
        unique=True, db_index=True, max_length=_len_full_uid, default=base62_20
    )
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=150, db_index=True, default=None)
    """Name or title of collection (required)."""
    description: str = TextField(null=True, default=None)
    """A description."""
    hash: str = CharField(
        max_length=HASH_LENGTH, db_index=True, null=True, default=None
    )
    """Hash of collection content. 86 base64 chars allow to store 64 bytes, 512 bits."""
    reference: str = CharField(max_length=255, db_index=True, null=True, default=None)
    """A reference like URL or external ID."""
    # also for reference_type here, we allow an extra long max_length
    reference_type: str = CharField(
        max_length=25, db_index=True, null=True, default=None
    )
    """Type of reference, e.g., cellxgene Census collection_id."""
    feature_sets: FeatureSet = models.ManyToManyField(
        "FeatureSet", related_name="collections", through="CollectionFeatureSet"
    )
    """The feature sets measured in this collection (see :class:`~lamindb.FeatureSet`)."""
    ulabels: ULabel = models.ManyToManyField(
        "ULabel", through="CollectionULabel", related_name="collections"
    )
    """ULabels sampled in the collection (see :class:`~lamindb.Feature`)."""
    transform: Transform = models.ForeignKey(
        Transform, PROTECT, related_name="output_collections", null=True, default=None
    )
    """:class:`~lamindb.Transform` whose run created the collection."""
    run: Run = models.ForeignKey(
        Run, PROTECT, related_name="output_collections", null=True, default=None
    )
    """:class:`~lamindb.Run` that created the `collection`."""
    input_of_runs: Run = models.ManyToManyField(Run, related_name="input_collections")
    """Runs that use this collection as an input."""
    _previous_runs: Run = models.ManyToManyField(
        "Run", related_name="output_collections_with_later_updates"
    )
    """Sequence of runs that created or updated the record."""
    artifacts: Artifact = models.ManyToManyField(
        "Artifact", related_name="collections", through="CollectionArtifact"
    )
    """Artifacts in collection."""
    meta_artifact: Artifact | None = models.OneToOneField(
        "Artifact", PROTECT, null=True, unique=True, related_name="meta_of_collection"
    )
    """An artifact that stores metadata that indexes the collection."""
    visibility: int = models.SmallIntegerField(
        db_index=True, choices=VisibilityChoice.choices, default=1
    )
    """Visibility of collection record in queries & searches (1 default, 1 hidden, -1 trash)."""

    @overload
    def __init__(
        self,
        artifacts: list[Artifact],
        name: str,
        version: str,
        description: str | None = None,
        meta: Any | None = None,
        reference: str | None = None,
        reference_type: str | None = None,
        run: Run | None = None,
        is_new_version_of: Collection | None = None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    def mapped(
        self,
        layers_keys: str | list[str] | None = None,
        obs_keys: str | list[str] | None = None,
        obsm_keys: str | list[str] | None = None,
        join: Literal["inner", "outer"] | None = "inner",
        encode_labels: bool | list[str] = True,
        unknown_label: str | dict[str, str] | None = None,
        cache_categories: bool = True,
        parallel: bool = False,
        dtype: str | None = None,
        stream: bool = False,
        is_run_input: bool | None = None,
    ) -> MappedCollection:
        """Return a map-style dataset.

        Returns a `pytorch map-style dataset
        <https://pytorch.org/docs/stable/data.html#map-style-datasets>`__ by
        virtually concatenating `AnnData` arrays.

        If your `AnnData` collection is in the cloud, move them into a local
        cache first via :meth:`~lamindb.Collection.cache`.

        `__getitem__` of the `MappedCollection` object takes a single integer index
        and returns a dictionary with the observation data sample for this index from
        the `AnnData` objects in the collection. The dictionary has keys for `layers_keys`
        (`.X` is in `"X"`), `obs_keys`, `obsm_keys` (under `f"obsm_{key}"`) and also `"_store_idx"`
        for the index of the `AnnData` object containing this observation sample.

        .. note::

            For a guide, see :doc:`docs:scrna5`.

            This method currently only works for collections of `AnnData` artifacts.

        Args:
            layers_keys: Keys from the ``.layers`` slot. ``layers_keys=None`` or ``"X"`` in the list
                retrieves ``.X``.
            obsm_keys: Keys from the ``.obsm`` slots.
            obs_keys: Keys from the ``.obs`` slots.
            join: `"inner"` or `"outer"` virtual joins. If ``None`` is passed,
                does not join.
            encode_labels: Encode labels into integers.
                Can be a list with elements from ``obs_keys``.
            unknown_label: Encode this label to -1.
                Can be a dictionary with keys from ``obs_keys`` if ``encode_labels=True``
                or from ``encode_labels`` if it is a list.
            cache_categories: Enable caching categories of ``obs_keys`` for faster access.
            parallel: Enable sampling with multiple processes.
            dtype: Convert numpy arrays from ``.X``, ``.layers`` and ``.obsm``
            stream: Whether to stream data from the array backend.
            is_run_input: Whether to track this collection as run input.

        Examples:
            >>> import lamindb as ln
            >>> from torch.utils.data import DataLoader
            >>> ds = ln.Collection.filter(description="my collection").one()
            >>> mapped = collection.mapped(label_keys=["cell_type", "batch"])
            >>> dl = DataLoader(mapped, batch_size=128, shuffle=True)
        """
        pass

    def cache(self, is_run_input: bool | None = None) -> list[UPath]:
        """Download cloud artifacts in collection to local cache.

        Follows synching logic: only caches outdated artifacts.

        Returns paths to locally cached on-disk artifacts.

        Args:
            is_run_input: Whether to track this collection as run input.
        """
        pass

    def load(
        self,
        join: Literal["inner", "outer"] = "outer",
        is_run_input: bool | None = None,
        **kwargs,
    ) -> Any:
        """Stage and load to memory.

        Returns in-memory representation if possible, e.g..  concatenated `DataFrame` or `AnnData` object.
        """
        pass

    def delete(self, permanent: bool | None = None) -> None:
        """Delete collection.

        Args:
            permanent: Whether to permanently delete the collection record (skips trash).

        Examples:

            For any `Collection` object `collection`, call:

            >>> collection.delete()
        """
        pass

    def save(self, using: str | None = None) -> Collection:
        """Save the collection and underlying artifacts to database & storage.

        Args:
            using: The database to which you want to save.

        Examples:
            >>> collection = ln.Collection("./myfile.csv", name="myfile")
            >>> collection.save()
        """
        pass

    def restore(self) -> None:
        """Restore collection record from trash.

        Examples:

            For any `Collection` object `collection`, call:

            >>> collection.restore()
        """
        pass

    @property
    def ordered_artifacts(self) -> QuerySet:
        """Ordered `QuerySet` of `.artifacts`.

        Accessing the many-to-many field `collection.artifacts` directly gives
        you non-deterministic order.

        Using the property `.ordered_artifacts` allows to iterate through a set
        that's ordered in the order of creation.
        """
        pass

    @property
    def data_artifact(self) -> Artifact | None:
        """Access to a single data artifact.

        If the collection has a single data & metadata artifact, this allows access via::

           collection.data_artifact  # first & only element of collection.artifacts
           collection.meta_artifact  # metadata

        """
        pass


# auto-generated through choices()
delattr(Collection, "get_visibility_display")


# -------------------------------------------------------------------------------------
# Link models


class LinkORM:
    pass


class FeatureSetFeature(Record, LinkORM):
    id: int = models.BigAutoField(primary_key=True)
    # we follow the lower() case convention rather than snake case for link models
    featureset: FeatureSet = models.ForeignKey(FeatureSet, CASCADE, related_name="+")
    feature: Feature = models.ForeignKey(Feature, PROTECT, related_name="+")


class ArtifactFeatureSet(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="links_feature_set"
    )
    # we follow the lower() case convention rather than snake case for link models
    featureset: FeatureSet = models.ForeignKey(
        FeatureSet, PROTECT, related_name="links_artifact"
    )
    slot: str = CharField(max_length=40, null=True, default=None)
    feature_ref_is_semantic: bool = models.BooleanField(
        null=True, default=None
    )  # like Feature name or Gene symbol or CellMarker name

    class Meta:
        unique_together = ("artifact", "featureset")


class CollectionFeatureSet(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    collection = models.ForeignKey(
        Collection, CASCADE, related_name="links_feature_set"
    )
    # we follow the lower() case convention rather than snake case for link models
    featureset: FeatureSet = models.ForeignKey(
        FeatureSet, PROTECT, related_name="links_collection"
    )
    slot: str = CharField(max_length=50, null=True, default=None)
    feature_ref_is_semantic: bool = models.BooleanField(
        null=True, default=None
    )  # like Feature name or Gene symbol or CellMarker name

    class Meta:
        unique_together = ("collection", "featureset")


class CollectionArtifact(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    collection: Collection = models.ForeignKey(
        Collection, CASCADE, related_name="links_artifact"
    )
    artifact: Artifact = models.ForeignKey(
        Artifact, PROTECT, related_name="links_collection"
    )

    class Meta:
        unique_together = ("collection", "artifact")


class ArtifactULabel(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="links_ulabel"
    )
    ulabel = models.ForeignKey(ULabel, PROTECT, related_name="links_artifact")
    feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="links_artifactulabel"
    )
    label_ref_is_name: bool = models.BooleanField(null=True, default=None)
    feature_ref_is_name: bool = models.BooleanField(null=True, default=None)

    class Meta:
        unique_together = ("artifact", "ulabel")


class CollectionULabel(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    collection: Collection = models.ForeignKey(
        Collection, CASCADE, related_name="links_ulabel"
    )
    ulabel: ULabel = models.ForeignKey(ULabel, PROTECT, related_name="links_collection")
    feature: Feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="links_collectionulabel"
    )
    label_ref_is_name: bool = models.BooleanField(null=True, default=None)
    feature_ref_is_name: bool = models.BooleanField(null=True, default=None)

    class Meta:
        unique_together = ("collection", "ulabel")


class ArtifactFeatureValue(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(Artifact, CASCADE, related_name="+")
    # we follow the lower() case convention rather than snake case for link models
    featurevalue = models.ForeignKey(FeatureValue, PROTECT, related_name="+")

    class Meta:
        unique_together = ("artifact", "featurevalue")


class RunParamValue(Record, LinkORM):
    id: int = models.BigAutoField(primary_key=True)
    run: Run = models.ForeignKey(Run, CASCADE, related_name="+")
    # we follow the lower() case convention rather than snake case for link models
    paramvalue: ParamValue = models.ForeignKey(ParamValue, PROTECT, related_name="+")

    class Meta:
        unique_together = ("run", "paramvalue")


class ArtifactParamValue(Record, LinkORM):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(Artifact, CASCADE, related_name="+")
    # we follow the lower() case convention rather than snake case for link models
    paramvalue: ParamValue = models.ForeignKey(ParamValue, PROTECT, related_name="+")

    class Meta:
        unique_together = ("artifact", "paramvalue")


# class Migration(Record):
#     app = CharField(max_length=255)
#     name = CharField(max_length=255)
#     applied: datetime = models.DateTimeField()

#     class Meta:
#         db_table = "django_migrations"
#         managed = False


# -------------------------------------------------------------------------------------
# Low-level logic needed in lamindb-setup

# Below is needed within lnschema-core because lamindb-setup already performs
# some logging


def format_field_value(value: datetime | str | Any) -> Any:
    if isinstance(value, datetime):
        value = value.strftime("%Y-%m-%d %H:%M:%S %Z")
    if isinstance(value, str):
        return f"'{value}'"
    else:
        return value


def __repr__(
    self: Record, include_foreign_keys: bool = True, exclude_field_names=None
) -> str:
    if exclude_field_names is None:
        exclude_field_names = ["id", "created_at"]
    field_names = [
        field.name
        for field in self._meta.fields
        if (
            not isinstance(field, models.ForeignKey)
            and field.name not in exclude_field_names
        )
    ]
    if include_foreign_keys:
        field_names += [
            f"{field.name}_id"
            for field in self._meta.fields
            if isinstance(field, models.ForeignKey)
        ]
    if "updated_at" in field_names:
        field_names.remove("updated_at")
        field_names.append("updated_at")
    if field_names[0] != "uid" and "uid" in field_names:
        field_names.remove("uid")
        field_names.insert(0, "uid")
    fields_str = {
        k: format_field_value(getattr(self, k)) for k in field_names if hasattr(self, k)
    }
    fields_joined_str = ", ".join(
        [f"{k}={fields_str[k]}" for k in fields_str if fields_str[k] is not None]
    )
    return f"{self.__class__.__name__}({fields_joined_str})"


# below is code to further format the repr of a record
#
# def format_repr(
#     record: Record, exclude_field_names: str | list[str] | None = None
# ) -> str:
#     if isinstance(exclude_field_names, str):
#         exclude_field_names = [exclude_field_names]
#     exclude_field_names_init = ["id", "created_at", "updated_at"]
#     if exclude_field_names is not None:
#         exclude_field_names_init += exclude_field_names
#     return record.__repr__(
#         include_foreign_keys=False, exclude_field_names=exclude_field_names_init
#     )


Record.__repr__ = __repr__  # type: ignore
Record.__str__ = __repr__  # type: ignore


def deferred_attribute__repr__(self):
    return f"FieldAttr({self.field.model.__name__}.{self.field.name})"


FieldAttr.__repr__ = deferred_attribute__repr__  # type: ignore


Registry = Record  # backward compat
