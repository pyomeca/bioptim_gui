from bioptim_gui_api.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import StraightAcrobaticsVariables
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import TuckAcrobaticsVariables


def test_tau_init():
    expected = [0.0, 0.0, 0.0, 0.0]
    actual = StraightAcrobaticsVariables.get_tau_init()
    assert actual == expected


def test_tau_init():
    expected = [0.0] * 10
    actual = PikeAcrobaticsVariables.get_tau_init()
    assert actual == expected


def test_tau_init():
    expected = [0.0] * 11
    actual = TuckAcrobaticsVariables.get_tau_init()
    assert actual == expected
