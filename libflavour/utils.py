from strictyaml import Map

from .fields import FieldFactory


def get_schema_for_type_identifier(type_: str) -> Map:
    """
    returns the yaml schema for a widget type identifier
    """
    return FieldFactory().get_widgets()[type_].schema()
