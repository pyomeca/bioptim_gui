import os

import pytest

from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
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
    ("with_visual_criteria", "non_collision", "without_cone", "with_spine", "folder"),
    [
        (True, True, False, False, "with_collision_and_visual"),
        (True, True, True, False, "with_collision_and_visual_coneless"),
        (True, False, False, False, "with_visual"),
        (True, False, True, False, "with_visual_coneless"),
        (False, True, False, False, "with_collision"),
        (False, False, False, False, "vanilla"),
        (True, True, False, True, "everything"),
    ],
)
def test_good(position, with_visual_criteria, non_collision, without_cone, with_spine, folder):
    converter = get_converter(
        position, AdditionalCriteria(with_visual_criteria, non_collision, without_cone, with_spine)
    )
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
    ("with_visual_criteria", "non_collision", "without_cone", "folder"),
    [
        (True, True, False, "with_collision_and_visual"),
        (True, True, True, "with_collision_and_visual_coneless"),
        (True, False, False, "with_visual"),
        (True, False, True, "with_visual_coneless"),
        (False, True, False, "with_collision"),
        (False, False, False, "vanilla"),
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
def test_bad(position, with_visual_criteria, non_collision, without_cone, folder, reason):
    converter = get_converter(position, AdditionalCriteria(with_visual_criteria, non_collision, without_cone))
    filepath = f"{BIOMODS_PATH}/{folder}/{reason}/{position}.bioMod"

    if os.path.exists(filepath):
        with pytest.raises(ValueError):
            converter.convert(filepath)
