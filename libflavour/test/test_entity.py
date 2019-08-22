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
                "value": "default",
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
                "value": "default",
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
    )
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
                "type": "scalar/int",
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
                "value": 3,
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
