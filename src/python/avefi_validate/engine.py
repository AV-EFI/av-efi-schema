"""The schema engines behind ``get_schema_validator``.

Two engines can validate a record: the Rust ``jsonschema_rs`` crate when
it is installed, and the pure-Python ``jsonschema`` package otherwise.
They are selected at runtime; neither is exposed publicly, and callers
only ever see :class:`SchemaError`.

Keeping the engines behind one error type is what makes the report
stable across installations: the diagnostics are built from the
keyword, the expected value and a few structured details, never from
the wording an engine happens to use. ``params.keyword`` and
``params.expected`` are therefore identical whichever engine ran.

A record is validated against its own ``$defs`` branch, not against the
root union: the branch is the class named by the record's ``category``,
so the other branches cannot produce misleading errors and the
validator does no work that is thrown away.

"""

from dataclasses import dataclass, field
import logging
import os

log = logging.getLogger(__name__)

#: Environment variable that forces an engine. Intended for tests and
#: debugging; the default is the Rust engine when it is installed.
ENGINE_ENV = "AVEFFI_VALIDATE_ENGINE"


@dataclass
class SchemaError:
    """An engine-neutral schema violation.

    The fields mirror the parts of a ``jsonschema`` error that the
    validator consumes, so both engines can be handled the same way.

    ``details`` carries the structured facts a message may need but the
    schema does not state directly: the missing property of a
    ``required`` error, or the unexpected keys of an
    ``additionalProperties`` error.

    """

    absolute_path: tuple
    validator: str
    validator_value: object
    instance: object
    schema_path: tuple
    context: tuple = ()
    details: dict = field(default_factory=dict)


def _branch_names(schema: dict) -> tuple[str, ...]:
    """Return the ``$defs`` entries the root union is built from."""
    names = []
    for option in schema.get("anyOf") or ():
        if not isinstance(option, dict):
            continue
        ref = option.get("$ref")
        if not isinstance(ref, str) or not ref.startswith("#/$defs/"):
            continue
        name = ref.rsplit("/", 1)[-1]
        if name not in names:
            names.append(name)
    return tuple(names)


def _branch_schema(schema: dict, name: str) -> dict:
    """Return a schema that validates one record branch by itself."""
    wrapper = {"$defs": schema.get("$defs", {})}
    if "$schema" in schema:
        wrapper["$schema"] = schema["$schema"]
    wrapper["$ref"] = f"#/$defs/{name}"
    return wrapper


def _lookup(node, path):
    """Return the subschema at ``path`` or raise ``LookupError``."""
    for part in path:
        if isinstance(node, (list, tuple)):
            node = node[int(part)]
        elif isinstance(node, dict):
            node = node[part]
        else:
            raise LookupError(part)
    return node


class RustSchemaValidator:
    """Validate with ``jsonschema_rs`` and translate its errors."""

    engine = "rust"

    def __init__(self, schema: dict):
        import jsonschema_rs

        self._schema = schema
        self._root = jsonschema_rs.Draft201909Validator(
            schema, validate_formats=False
        )
        self._branches = {}
        for name in _branch_names(schema):
            wrapper = _branch_schema(schema, name)
            self._branches[name] = (
                wrapper,
                jsonschema_rs.Draft201909Validator(
                    wrapper, validate_formats=False
                ),
            )

    def iter_errors(self, instance):
        """Yield the violations of the root schema."""
        return [
            self._translate(error, self._schema)
            for error in self._root.iter_errors(instance)
        ]

    def iter_errors_for(self, instance, category):
        """Yield the violations of ``category``'s own branch."""
        entry = self._branches.get(category)
        if entry is None:
            return self.iter_errors(instance)
        wrapper, validator = entry
        return [
            self._translate(error, wrapper)
            for error in validator.iter_errors(instance)
        ]

    def _translate(self, error, schema):
        kind = error.kind
        keyword = kind.name
        try:
            details = dict(kind.as_dict())
        except (AttributeError, TypeError, ValueError):
            details = {}
        context_data = details.pop("context", None)
        schema_path = tuple(error.schema_path)
        try:
            expected = _lookup(schema, schema_path)
        except (LookupError, TypeError, ValueError):
            expected = getattr(kind, "value", None)
        context = ()
        if keyword in ("anyOf", "oneOf") and context_data:
            context = tuple(
                self._translate(child, schema)
                for group in context_data
                for child in (group if isinstance(group, list) else [group])
            )
        return SchemaError(
            absolute_path=tuple(error.instance_path),
            validator=keyword,
            validator_value=expected,
            instance=error.instance,
            schema_path=schema_path,
            context=context,
            details=details,
        )


class PythonSchemaValidator:
    """Validate with ``jsonschema`` and normalise its errors."""

    engine = "python"

    def __init__(self, schema: dict):
        from jsonschema.validators import validator_for

        self._schema = schema
        cls = validator_for(schema)
        cls.check_schema(schema)
        self._validator = cls(schema)
        self._branches = {}

    def iter_errors(self, instance):
        """Yield the violations of the root schema."""
        return _translate_python_errors(self._validator.iter_errors(instance))

    def iter_errors_for(self, instance, category):
        """Yield the violations of ``category``'s own branch."""
        if category not in (self._schema.get("$defs") or {}):
            return self.iter_errors(instance)
        validator = self._branches.get(category)
        if validator is None:
            validator = self._validator.evolve(
                schema=_branch_schema(self._schema, category)
            )
            self._branches[category] = validator
        return _translate_python_errors(validator.iter_errors(instance))


def _python_details(error) -> dict:
    """Return the structured facts behind one Python error."""
    if error.validator == "additionalProperties":
        parent = error.schema if isinstance(error.schema, dict) else {}
        properties = parent.get("properties") or {}
        instance = error.instance
        if isinstance(instance, dict):
            unexpected = [key for key in instance if key not in properties]
        else:
            unexpected = []
        return {"unexpected": unexpected}
    if error.validator == "required":
        missing = [
            str(prop)
            for prop in error.validator_value
            if prop not in (error.instance or {})
        ]
        if len(missing) == 1:
            return {"property": missing[0]}
    return {}


def _python_error(error, details: dict) -> SchemaError:
    """Translate one Python error, including its context."""
    return SchemaError(
        absolute_path=tuple(error.absolute_path),
        validator=error.validator,
        validator_value=error.validator_value,
        instance=error.instance,
        schema_path=tuple(error.schema_path),
        context=tuple(
            _python_error(child, _python_details(child))
            for child in error.context or ()
        ),
        details=details,
    )


def _translate_python_errors(errors) -> list[SchemaError]:
    """Translate a Python error stream, one error per missing property.

    ``jsonschema`` reports one ``required`` error per missing property,
    but its message is prose. The missing properties are known from the
    instance and the ``required`` list, so the errors are rebuilt from
    those, keeping the engine's order and producing one named property
    per error.

    """
    errors = list(errors)
    remaining = {}
    translated = []
    for error in errors:
        if error.validator == "required":
            key = (id(error.instance), tuple(error.absolute_schema_path))
            missing = remaining.get(key)
            if missing is None:
                missing = [
                    str(prop)
                    for prop in error.validator_value
                    if prop not in (error.instance or {})
                ]
                remaining[key] = missing
            prop = missing.pop(0) if missing else None
            details = {"property": prop} if prop is not None else {}
        else:
            details = _python_details(error)
        translated.append(_python_error(error, details))
    return translated


def build_schema_validator(schema: dict):
    """Return the preferred engine for ``schema``.

    The Rust engine wins when ``jsonschema_rs`` can be imported. The
    Python engine is the fallback, so a platform without a wheel still
    validates, only more slowly. ``AVEFFI_VALIDATE_ENGINE`` forces one
    of them; an unknown value is ignored with a warning.

    """
    requested = os.environ.get(ENGINE_ENV, "").strip().lower()
    if requested == "python":
        return PythonSchemaValidator(schema)
    if requested == "rust":
        return RustSchemaValidator(schema)
    if requested:
        log.warning(
            "ignoring unknown %s=%r; using the default engine",
            ENGINE_ENV,
            requested,
        )
    try:
        return RustSchemaValidator(schema)
    except ImportError:
        log.debug("jsonschema_rs is not installed; using the Python engine")
        return PythonSchemaValidator(schema)


def iter_schema_errors(schema_validator, document, category=None):
    """Return :class:`SchemaError` objects for any supported validator.

    Validators built here answer ``iter_errors_for`` and need no
    translation. A raw ``jsonschema`` validator passed by a caller only
    has ``iter_errors``; its errors are translated here so the rest of
    the validator sees one error type.

    """
    if category is not None and hasattr(schema_validator, "iter_errors_for"):
        return list(schema_validator.iter_errors_for(document, category))
    errors = list(schema_validator.iter_errors(document))
    if all(isinstance(error, SchemaError) for error in errors):
        return errors
    return _translate_python_errors(errors)
