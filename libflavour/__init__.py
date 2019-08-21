__author__ = "Divio AG"
__email__ = "dennis.schwertel@divio.ch"
__version__ = "0.0.11"
__url__ = "https://www.divio.com"

import strictyaml

from .fields import FieldFactory
from .schema import schema_addon, schema_project
from .utils import get_schema_for_type_identifier


class Addon:
    yaml = None
    _data = None
    config = None

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

            # If all is valid, generate the classes for the configuration
            ff = FieldFactory()
            self.config = ff.load(self._data.data["config"])

    @property
    def data(self) -> dict:
        return self._data.data
