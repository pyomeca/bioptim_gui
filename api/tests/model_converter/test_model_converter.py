import os

import pytest

from bioptim_gui_api.model_converter.utils import get_converter

BIOMODS_PATH = "test_biomods"  # to change depending on from where you run the test


@pytest.mark.parametrize(
    "position",
    [
        "straight",
        "pike",
        "tuck",
    ],
)
@pytest.mark.parametrize(
    ("with_visual_criteria", "non_collision", "folder"),
    [
        (True, True, "with_collision_and_visual"),
        (True, False, "with_visual"),
        (False, True, "with_collision"),
        (False, False, "vanilla"),
    ],
)
def test_good(position, with_visual_criteria, non_collision, folder):
    converter = get_converter(position, with_visual_criteria, non_collision)
    actual = converter.convert(f"{BIOMODS_PATH}/{folder}/{folder}_base.bioMod")
    with open(f"{BIOMODS_PATH}/{folder}/good/{position}.bioMod", "r") as f:
        expected = f.read()
        assert actual == expected


@pytest.mark.parametrize(
    "position",
    [
        "straight",
        "pike",
        "tuck",
    ],
)
@pytest.mark.parametrize(
    ("with_visual_criteria", "non_collision", "folder"),
    [
        (True, True, "with_collision_and_visual"),
        (True, False, "with_visual"),
        (False, True, "with_collision"),
        (False, False, "vanilla"),
    ],
)
@pytest.mark.parametrize(
    "reason",
    [
        "missing_marker",
        "missing_segment",
        "missing_marker_and_segment",
    ],
)
def test_bad(position, with_visual_criteria, non_collision, folder, reason):
    converter = get_converter(position, with_visual_criteria, non_collision)
    filepath = f"{BIOMODS_PATH}/{folder}/{reason}/{position}.bioMod"

    if os.path.exists(filepath):
        with pytest.raises(ValueError):
            converter.convert(filepath)
