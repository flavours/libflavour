from pathlib import Path

import libflavour
import pytest


yaml_example_files_data = [
    (
        "libflavour/test/data/example_addon_data_3.yaml",
        [
            {
                "type": "scalar/string",
                "name": "languages",
                "label": "Languages",
                "helptext": "helptext",
                "variable": "DJANGO_DIVIO_LANGUAGES",
                "default": "default",
                "visibility": 0,
                "readonly": False,
                "required": True,
                "value": None,
            },
            {
                "type": "scalar/string",
                "name": "otherlanguages",
                "label": "Languages",
                "helptext": "helptext",
                "variable": "DJANGO_DIVIO_OTHERLANGUAGES",
                "visibility": 0,
                "readonly": False,
                "required": False,
                "value": None,
            },
        ],
        {"DJANGO_DIVIO_OTHERLANGUAGES": "it"},
        [
            {
                "type": "scalar/string",
                "name": "languages",
                "label": "Languages",
                "helptext": "helptext",
                "variable": "DJANGO_DIVIO_LANGUAGES",
                "default": "default",
                "visibility": 0,
                "readonly": False,
                "required": True,
                "value": None,
            },
            {
                "type": "scalar/string",
                "name": "otherlanguages",
                "label": "Languages",
                "helptext": "helptext",
                "variable": "DJANGO_DIVIO_OTHERLANGUAGES",
                "visibility": 0,
                "readonly": False,
                "required": False,
                "value": "it",
            },
        ],
    ),
    (
        "libflavour/test/data/example_addon_data_5.yaml",
        [
            {
                "type": "scalar/string",
                "name": "required_without_default",
                "label": "Required without default",
                "helptext": "",
                "variable": "DJANGO_DIVIO_REQUIRED_WITHOUT_DEFAULT",
                "visibility": 0,
                "readonly": False,
                "required": True,
                "value": None,
            }
        ],
        {"DJANGO_DIVIO_REQUIRED_WITHOUT_DEFAULT": "a"},
        [
            {
                "type": "scalar/string",
                "name": "required_without_default",
                "label": "Required without default",
                "helptext": "",
                "variable": "DJANGO_DIVIO_REQUIRED_WITHOUT_DEFAULT",
                "visibility": 0,
                "readonly": False,
                "required": True,
                "value": "a",
            }
        ],
    ),
]


@pytest.mark.parametrize(
    "yaml_filename, data, update_values, updated_data", yaml_example_files_data
)
def test_update_data(yaml_filename, data, update_values, updated_data):
    with Path(yaml_filename).open() as f:
        addon = libflavour.Addon(f.read())
        assert addon.fields_json == data
        addon.update_values(update_values)
        addon.validate()
        assert addon.fields_json == updated_data


yaml_example_files_data_2 = [
    (
        "libflavour/test/data/example_addon_data_2.yaml",
        [
            {
                "type": "scalar/integer",
                "name": "languages",
                "label": "Languages",
                "helptext": "helptext",
                "variable": "SOME_OTHER_NAME",
                "default": 3,
                "visibility": 0,
                "readonly": False,
                "required": True,
                "min": 4,
                "max": None,
                "value": None,
            }
        ],
        {"SOME_OTHER_NAME": "it"},
    )
]


@pytest.mark.parametrize(
    "yaml_filename, data, update_values", yaml_example_files_data_2
)
def test_update_data_2(yaml_filename, data, update_values):
    with Path(yaml_filename).open() as f:
        addon = libflavour.Addon(f.read())
        assert addon.fields_json == data
        addon.validate() == {}
        addon.update_values(update_values)
        addon.validate() == {"languages": "Not a integer"}


get_values_test_data = [
    (
        "libflavour/test/data/example_addon_data_2.yaml",
        {},
        {},
        {"SOME_OTHER_NAME": 3},
    ),
    (
        "libflavour/test/data/example_addon_data_2.yaml",
        {"languages": 47},
        {"SOME_OTHER_NAME": 47},
        {"SOME_OTHER_NAME": 47},
    ),
    (
        "libflavour/test/data/example_addon_data_3.yaml",
        {},
        {},
        {"DJANGO_DIVIO_LANGUAGES": "default"},
    ),
    (
        "libflavour/test/data/example_addon_data_3.yaml",
        {"otherlanguages": "en"},
        {"DJANGO_DIVIO_OTHERLANGUAGES": "en"},
        {
            "DJANGO_DIVIO_LANGUAGES": "default",
            "DJANGO_DIVIO_OTHERLANGUAGES": "en",
        },
    ),
    (
        "libflavour/test/data/example_addon_data_3.yaml",
        {"languages": "it", "otherlanguages": "en"},
        {"DJANGO_DIVIO_LANGUAGES": "it", "DJANGO_DIVIO_OTHERLANGUAGES": "en"},
        {"DJANGO_DIVIO_LANGUAGES": "it", "DJANGO_DIVIO_OTHERLANGUAGES": "en"},
    ),
]


@pytest.mark.parametrize(
    "yaml_filename, data, expected_values, expected_with_defaults",
    get_values_test_data,
)
def test_get_values(
    yaml_filename, data, expected_values, expected_with_defaults
):
    yaml_text = Path(yaml_filename).read_text()
    addon = libflavour.Addon(yaml_text)
    for field in addon.fields:
        if field.name in data:
            field.value = data[field.name]
    assert addon.get_values(include_defaults=False) == expected_values
    assert addon.get_values(include_defaults=True) == expected_with_defaults


validation_test_data = [
    (
        "libflavour/test/data/example_addon_data_4.yaml",
        {},
        {
            "boolean": "This is a required field",
            "positive_integer": "This is a required field",
        },
        {},
    ),
    (
        "libflavour/test/data/example_addon_data_4.yaml",
        {"BOOL": "invalid", "PLUS_INT": -5, "MINUS_INT": 47},
        {
            "boolean": "invalid is not a boolean value",
            "positive_integer": "-5 is lower than the minimum value (0)",
            "negative_integer": "47 is higher than the maximum value (0)",
        },
        {},
    ),
    (
        "libflavour/test/data/example_addon_data_4.yaml",
        {"BOOL": "Yes", "PLUS_INT": "32", "MINUS_INT": "-3"},
        {},
        {"BOOL": True, "PLUS_INT": 32, "MINUS_INT": -3},
    ),
]


@pytest.mark.parametrize(
    "yaml_filename, data, expected_errors, expected_values",
    validation_test_data,
)
def test_validation(yaml_filename, data, expected_errors, expected_values):
    yaml_text = Path(yaml_filename).read_text()
    addon = libflavour.Addon(yaml_text)
    addon.update_values(data)
    assert addon.validate() == expected_errors
    if expected_values:
        assert addon.get_values() == expected_values
