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
    "yaml_filename, data, updated_data", yaml_example_files_data
)
def test_update_data(yaml_filename, data, updated_data):
    with Path(yaml_filename).open() as f:
        addon = libflavour.Addon(f.read())
        assert addon.fields_json == data

        new_data = {"DJANGO_DIVIO_OTHERLANGUAGES": "it"}

        addon.update_fields(new_data)
        addon.validate()
        assert addon.fields_json == updated_data
