from bioptim_gui_api.model_converter.pike_to_straight import pike_to_straight
from bioptim_gui_api.model_converter.pike_to_tuck import pike_to_tuck

PIKE_PATH = "test_biomods/pike.bioMod"
TUCK_PATH = "test_biomods/tuck.bioMod"
STRAIGHT_PATH = "test_biomods/straight.bioMod"


def test_pike_to_tuck():
    with open(TUCK_PATH, "r") as f:
        expected = f.read()

    actual = pike_to_tuck(PIKE_PATH)

    assert actual == expected


def test_pike_to_straight():
    with open(STRAIGHT_PATH, "r") as f:
        expected = f.read()

    actual = pike_to_straight(PIKE_PATH)

    assert actual == expected
