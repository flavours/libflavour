import attr
from strictyaml import Bool, Int, Map, Optional, Str

from .base import BaseField


@attr.s
class IntegerField(BaseField):
    min = attr.ib(kw_only=True, default=None)
    max = attr.ib(kw_only=True, default=None)
    identifier = "scalar/int"

    def __str__(self):
        return f"{self.label} - Integer - {self.visibility} "

    @classmethod
    def schema(cls):
        return Map(
            {
                **super().schema()._validator,
                Optional("default"): Int(),
                Optional("min"): Int(),
                Optional("max"): Int(),
            }
        )

    @property
    def data(self):
        return {**super().data, "min": self.min, "max": self.max}


@attr.s
class StringField(BaseField):
    identifier = "scalar/string"

    def __str__(self):
        return f"{self.label} - String - {self.visibility} "

    @classmethod
    def schema(cls):
        return Map({**super().schema()._validator, Optional("default"): Str()})


@attr.s
class BooleanField(BaseField):
    identifier = "scalar/boolean"

    def __str__(self):
        return f"{self.label} - Boolean - {self.visibility}"

    @classmethod
    def schema(cls):
        return Map({**super().schema()._validator, Optional("default"): Bool()})
