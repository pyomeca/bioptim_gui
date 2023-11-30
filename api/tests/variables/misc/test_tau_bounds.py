from bioptim_gui_api.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import StraightAcrobaticsVariables
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import TuckAcrobaticsVariables


def test_tau_bounds():
    expected_min = [-500.0, -500.0, -500.0, -500.0]
    expected_max = [500.0, 500.0, 500.0, 500.0]
    actual = StraightAcrobaticsVariables.get_tau_bounds()
    actual_min, actual_max = actual["min"], actual["max"]
    assert actual_min == expected_min
    assert actual_max == expected_max


def test_tau_bounds():
    expected_min = [-500.0] * 10
    expected_max = [500.0] * 10
    actual = PikeAcrobaticsVariables.get_tau_bounds()
    actual_min, actual_max = actual["min"], actual["max"]
    assert actual_min == expected_min
    assert actual_max == expected_max


def test_tau_bounds():
    expected_min = [-500.0] * 11
    expected_max = [500.0] * 11
    actual = TuckAcrobaticsVariables.get_tau_bounds()
    actual_min, actual_max = actual["min"], actual["max"]
    assert actual_min == expected_min
    assert actual_max == expected_max
