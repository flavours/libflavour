from strictyaml import Map

from .fields import FieldFactory


def get_schema_for_type_identifier(type: str) -> Map:
    """
    returns the yaml schema for a widget type identifier
    """
    widgets = FieldFactory().get_widgets()
    for widget in widgets:
        if widgets[widget].identifier == type:
            return widgets[widget].schema()
