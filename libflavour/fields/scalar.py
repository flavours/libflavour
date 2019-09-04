import attr

from libflavour.exceptions import ValidationError
from strictyaml import Bool, Int, Map, Optional, Str

from .base import BaseField


@attr.s
class IntegerField(BaseField):
    min = attr.ib(kw_only=True, default=None)
    max = attr.ib(kw_only=True, default=None)
    identifier = "scalar/integer"

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

    def validate(self):
        super().validate()
        # check if we can int cast it
        try:
            int(self.value)
        except ValueError:
            raise ValidationError("Not a integer")

        if self.min and self.value < self.min:
            raise ValidationError("Value is lower than the minimum value")
        if self.max and self.value > self.max:
            raise ValidationError("Value is higher than the maximum value")


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
        return Map(
            {**super().schema()._validator, Optional("default"): Bool()}
        )
