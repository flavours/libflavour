__author__ = "Divio AG"
__email__ = "dennis.schwertel@divio.ch"
__version__ = "0.0.12"
__url__ = "https://www.divio.com"

import strictyaml

from .fields import FieldFactory
from .schema import schema_addon, schema_project
from .utils import get_schema_for_type_identifier


class Addon:
    yaml = None
    _data = None
    _config = None

    def __init__(self, yaml: str) -> None:
        self.yaml = yaml
        self._data = strictyaml.load(yaml, schema_addon)

        # Dynamically validate the configuration part of the yaml
        if "config" in self._data.data:
            for widget in self._data.data["config"]:
                self._data["config"][widget].revalidate(
                    get_schema_for_type_identifier(
                        self._data.data["config"][widget]["type"]
                    )
                )

    @property
    def data(self) -> dict:
        """
        returns the content of the yaml as a dict
        """
        return self._data.data

    @property
    def config(self) -> list:
        """
        returns a list of widgets for the configuration
        """
        if "config" not in self.data:
            return []
        return FieldFactory().load(self.data["config"])

    @property
    def config_json(self) -> list:
        """
        returns the config
        """
        addon_json = []
        for widget in self.config:
            addon_json.append(widget.data)
        return addon_json


class Project:
    yaml = None
    _data = None
    config = None

    def __init__(self, yaml: str) -> None:
        self.yaml = yaml
        self._data = strictyaml.load(yaml, schema_project)

        # Dynamically validate the configuration part of the yaml
        if "config" in self._data.data:
            for widget in self._data.data["config"]:
                self._data["config"][widget].revalidate(
                    get_schema_for_type_identifier(
                        self._data.data["config"][widget]["type"]
                    )
                )

            # If all is valid, generate the classes for the configuration
            ff = FieldFactory()
            self.config = ff.load(self._data.data["config"])

    @property
    def data(self) -> dict:
        return self._data.data
