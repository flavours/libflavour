import attr
from strictyaml import Map, Optional, Str

from .scalar import BooleanField, IntegerField, StringField
from .service import DatabaseField


class FieldFactory:
    def __init__(self):
        self.widgets = {
            BooleanField.identifier: BooleanField,
            IntegerField.identifier: IntegerField,
            StringField.identifier: StringField,
            DatabaseField.identifier: DatabaseField,
        }

    def get_widgets(self):
        return self.widgets

    def load(self, data):
        """
        expects a list of addons with the underlying addon structure
        """
        ret = []
        for addon_name in data:
            widget_class = self.widgets[data[addon_name]["type"]]
            widget = widget_class(name=addon_name, **data[addon_name])
            ret.append(widget)
        return ret
