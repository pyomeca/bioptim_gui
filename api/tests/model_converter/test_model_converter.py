import os

import pytest

from bioptim_gui_api.model_converter.converter import *

BIOMODS_PATH = "test_biomods"  # to change depending on from where you run the test

WITHOUT_VISUAL_BASE_PATH = f"{BIOMODS_PATH}/without_visual/without_visual_base.bioMod"
WITH_VISUAL_BASE_PATH = f"{BIOMODS_PATH}/with_visual/with_visual_base.bioMod"


@pytest.mark.parametrize(
    ("position", "converter"),
    [
        ("straight", StraightConverter),
        ("pike", PikeConverter),
        ("tuck", TuckConverter),
    ],
)
def test_without_visual(position, converter):
    actual = converter.convert(WITHOUT_VISUAL_BASE_PATH)
    expected = open(f"{BIOMODS_PATH}/without_visual/good/{position}.bioMod", "r").read()
    assert actual == expected


@pytest.mark.parametrize(
    ("position", "converter"),
    [
        ("straight", StraightConverter),
        ("pike", PikeConverter),
        ("tuck", TuckConverter),
    ],
)
def test_without_visual_bad(position, converter):
    for reason in [
        "missing_marker",
        "missing_segment",
        "missing_marker_and_segment",
    ]:
        filepath = f"{BIOMODS_PATH}/without_visual/{reason}/{position}.bioMod"
        if os.path.exists(filepath):
            with pytest.raises(ValueError):
                converter.convert(filepath)


@pytest.mark.parametrize(
    ("position", "converter"),
    [
        ("straight", StraightWithVisualConverter),
        ("pike", PikeWithVisualConverter),
        ("tuck", TuckWithVisualConverter),
    ],
)
def test_with_visual(position, converter):
    actual = converter.convert(WITH_VISUAL_BASE_PATH)
    expected = open(f"{BIOMODS_PATH}/with_visual/good/{position}.bioMod", "r").read()
    assert actual == expected


@pytest.mark.parametrize(
    ("reason"),
    [
        "missing_marker",
        "missing_segment",
        "missing_marker_and_segment",
    ],
)
@pytest.mark.parametrize(
    ("position", "converter"),
    [
        ("straight", StraightWithVisualConverter),
        ("pike", PikeWithVisualConverter),
        ("tuck", TuckWithVisualConverter),
    ],
)
def test_with_visual_bad(position, converter, reason):
    filepath = f"{BIOMODS_PATH}/with_visual/{reason}/{position}.bioMod"
    if os.path.exists(filepath):
        with pytest.raises(ValueError):
            converter.convert(filepath)
