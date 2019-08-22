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

    def load(self, flavour_entity):
        """
        expects a list of addons with the underlying addon structure
        """
        ret = []
        for addon_name in flavour_entity.data["config"]:
            widget_class = self.widgets[
                flavour_entity.data["config"][addon_name]["type"]
            ]
            widget = widget_class(
                name=addon_name,
                parent=flavour_entity,
                **flavour_entity.data["config"][addon_name]
            )
            ret.append(widget)
        return ret
