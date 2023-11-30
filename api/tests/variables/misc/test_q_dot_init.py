from bioptim_gui_api.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import StraightAcrobaticsVariables
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import TuckAcrobaticsVariables


def test_qdot_init():
    expected = [0.0] * 10
    actual = StraightAcrobaticsVariables.get_qdot_init()
    assert actual == expected


def test_qdot_init():
    expected = [0.0] * 17
    actual = TuckAcrobaticsVariables.get_qdot_init()
    assert actual == expected


def test_qdot_init():
    expected = [0.0] * 16
    actual = PikeAcrobaticsVariables.get_qdot_init()
    assert actual == expected
