import attr

from libflavour.exceptions import ValidationError
from strictyaml import Bool, Int, Map, Optional, Str

from .base import NOT_SET, BaseField


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

    def to_python(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValidationError(f"{value} is not an integer")

    def validate(self):
        super().validate()

        if self.value is NOT_SET:
            return

        if self.min is not None and self.value < self.min:
            raise ValidationError(
                f"{self.value} is lower than the minimum value ({self.min})"
            )
        if self.max is not None and self.value > self.max:
            raise ValidationError(
                f"{self.value} is higher than the maximum value ({self.max})"
            )


@attr.s
class StringField(BaseField):
    identifier = "scalar/string"

    def __str__(self):
        return f"{self.label} - String - {self.visibility} "

    @classmethod
    def schema(cls):
        return Map({**super().schema()._validator, Optional("default"): Str()})

    def to_python(self, value):
        return str(value)


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

    def to_python(self, value):
        if str(value).lower() in ["1", "true", "yes", "y", "on"]:
            return True
        elif str(value).lower() in ["0", "false", "no", "n", "off"]:
            return False
        raise ValidationError(f"{value} is not a boolean value")
