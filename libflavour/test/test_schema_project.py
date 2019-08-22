from pathlib import Path

import libflavour
import pytest
import strictyaml


yaml_example_files = [
    ("libflavour/test/data/example_project.yaml", True),
    ("libflavour/test/data/example_project_minimal_1.yaml", True),
    ("libflavour/test/data/example_project_minimal_1_error.yaml", False),
    ("libflavour/test/data/example_project_minimal_2.yaml", True),
    ("libflavour/test/data/example_project_minimal_2_error.yaml", False),
]


@pytest.mark.parametrize("yaml_filename, valid", yaml_example_files)
def test_validate_example_addon(yaml_filename, valid):
    with Path(yaml_filename).open() as f:
        if valid:
            libflavour.Application(f.read())
        else:
            with pytest.raises(strictyaml.exceptions.YAMLValidationError):
                libflavour.Application(f.read())


"""
yaml_example_files_addons = [
    (
        "libflavour/test/data/example_project.yaml",
        {
            "addon_example_1": OrderedDict(
                [
                    ("manager", "fam-python"),
                    ("hash", "abcd"),
                    (
                        "settings",
                        OrderedDict(
                            [
                                ("somevalue", "123"),
                                ("someothervalue", "123"),
                                ("database", "database1"),
                            ]
                        ),
                    ),
                ]
            ),
            "addon_example_2": OrderedDict([("manager", "fam-diviocloud-addon"),("hash", "abcd")]),
        },
    )
]
"""
