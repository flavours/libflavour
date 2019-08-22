from pathlib import Path

import pytest
import strictyaml

import libflavour


yaml_example_files = [
    ("libflavour/test/data/example_addon.yaml", True),
    ("libflavour/test/data/example_addon_minimal.yaml", True),
    ("libflavour/test/data/example_addon_dependencies.yaml", True),
    ("libflavour/test/data/example_addon_minimal_error.yaml", False),
    ("libflavour/test/data/example_aldryn_redirect.yaml", True),
]

yaml_example_files_data = [
    (
        "libflavour/test/data/example_addon_data_1.yaml",
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
        },
    ),
    (
        "libflavour/test/data/example_addon_data_2.yaml",
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
        },
    ),
]


@pytest.mark.parametrize("yaml_filename, valid", yaml_example_files)
def test_validate_example_addon(yaml_filename, valid):
    with Path(yaml_filename).open() as f:
        if valid:
            libflavour.Addon(f.read())
        else:
            with pytest.raises(strictyaml.exceptions.YAMLValidationError):
                libflavour.Addon(f.read())


@pytest.mark.parametrize("yaml_filename, data", yaml_example_files_data)
def test_data_function(yaml_filename, data):
    with Path(yaml_filename).open() as f:
        addon = libflavour.Addon(f.read())
        assert addon.config[0].data == data
