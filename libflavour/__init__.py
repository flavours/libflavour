__author__ = "Divio AG"
__email__ = "dennis.schwertel@divio.ch"
__version__ = "0.0.18"
__url__ = "https://www.divio.com"

import strictyaml

from . import schema
from .exceptions import ValidationError
from .fields import FieldFactory
from .fields.base import NOT_SET
from .utils import get_schema_for_type_identifier


class FlavourEntity:
    schema = None  # Overwritten in the childs
    yaml = None
    _data = None
    fields = []
    name = None
    version = None

    def __init__(self, yaml: str) -> None:
        self.yaml = yaml
        try:
            self._data = strictyaml.load(yaml, self.schema)

            # Dynamically validate the configuration part of the yaml
            if "config" in self._data.data:
                for widget in self._data.data["config"]:
                    self._data["config"][widget].revalidate(
                        get_schema_for_type_identifier(
                            self._data.data["config"][widget]["type"]
                        )
                    )

                self.fields = FieldFactory().load(self)
        except strictyaml.exceptions.YAMLValidationError as e:
            raise ValidationError(e)

        if "meta" in self._data.data:
            if "name" in self._data.data["meta"]:
                self.name = self._data.data["meta"]["name"]
            if "version" in self._data.data["meta"]:
                self.version = self._data.data["meta"]["version"]

    @property
    def data(self) -> dict:
        """
        returns the content of the yaml as a dict
        """
        return self._data.data

    @property
    def fields_json(self) -> list:
        """
        returns the config
        """
        addon_json = []
        for field in self.fields:
            addon_json.append(field.data)
        return addon_json

    def update_values(self, data: dict) -> None:
        """
        accepts a dictionary
        {
            "VARIABLE_NAME": "VALUE",
            "VARIABLE_NAME2": "OTHERVLAUE"
        }
        """

        for field in self.fields:
            if field.variable in data:
                field.value = data[field.variable]

    def get_values(self, include_defaults: bool = False) -> dict:
        """
        returns the current values of all fields as a dictionary, inverse
        of update_values
        {
            "VARIABLE_NAME": "VALUE",
            "VARIABLE_NAME2": "OTHERVLAUE"
        }
        """
        explicit_values = {
            field.variable: field.value
            for field in self.fields
            if field.value is not NOT_SET
        }
        if include_defaults:
            default_values = {
                field.variable: field.default
                for field in self.fields
                if field.default is not NOT_SET
            }
            default_values.update(explicit_values)
            return default_values
        return explicit_values

    def validate(self) -> dict:
        errors = {}
        for field in self.fields:
            try:
                field.validate()
            except Exception as e:
                errors[field.name] = str(e)
        return errors


class Addon(FlavourEntity):
    schema = schema.addon


class Application(FlavourEntity):
    schema = schema.application
