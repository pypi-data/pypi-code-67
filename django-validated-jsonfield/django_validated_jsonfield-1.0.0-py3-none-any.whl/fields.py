
import copy
import json

import jsonschema

try:
    from django.db.models import JSONField
else:
    from django.contrib.postgres.fields import JSONField

from django.contrib.staticfiles import finders
from django.core import checks, exceptions
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

#########################################################


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property_, subschema in properties.items():
            if "default" in subschema and not isinstance(instance, list):
                instance.setdefault(property_, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return jsonschema.validators.extend(
        validator_class, {"properties": set_defaults},
    )
ExtendedJsonValidatorWithDefault = extend_with_default(jsonschema.Draft7Validator)


class ValidatedJSONField(JSONField):
    """
    A models.JSONField subclass that supports the JSON schema validation.
    """

    @cached_property
    def _get_default(self):
        obj = {}
        if(self.json_validator_cls):
            self.json_validator_cls.validate(obj)
        return lambda: obj

    def run_validators(self, value):
        super().run_validators(value)

        if(self.json_validator_cls):
            errors = [ValidationError({str(error.path):error.message}) for error in self.json_validator_cls.iter_errors(value)]
            if(errors):
                raise ValidationError(errors)

    def __init__(self, *args, schema=None, default=None, blank=False, **kwargs):
        self.schema = schema
        if schema is not None:
            self.json_validator_cls = ExtendedJsonValidatorWithDefault(schema)
        else:
            self.json_validator_cls = None

        if(default is not None):
            print("#WARNING# ValidatedJSONField: default argument is not allowed, as default is taken from schema", default)

        if(blank):
            print("#WARNING# ValidatedJSONField: blank argument can't be set to True otherwise validation is not run")

        super().__init__(*args, blank=False, default=None, **kwargs)
