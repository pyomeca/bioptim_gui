from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import (
    TuckAcrobaticsVariables,
)


def test_q_bounds_quadruple_left_forward():
    actual = TuckAcrobaticsVariables.get_q_bounds(
        half_twists=[1, 0, 2, 4],
        prefer_left=True,
    )
    assert actual is not None


def test_q_init_quadruple_left_forward():
    actual = TuckAcrobaticsVariables.get_q_init(
        nb_phases=10,
        half_twists=[1, 0, 2, 4],
        prefer_left=True,
    )
    assert actual is not None


def test_qdot_bounds_quadruple_left_forward():
    actual = TuckAcrobaticsVariables.get_qdot_bounds(4, 4.0, True)

    assert actual is not None


def test_qdot_init():
    expected = [0.0] * 17
    actual = TuckAcrobaticsVariables.get_qdot_init()
    assert actual == expected


def test_tau_bounds():
    expected_min = [-500.0] * 11
    expected_max = [500.0] * 11
    actual = TuckAcrobaticsVariables.get_tau_bounds()
    actual_min, actual_max = actual["min"], actual["max"]
    assert actual_min == expected_min
    assert actual_max == expected_max


def test_tau_init():
    expected = [0.0] * 11
    actual = TuckAcrobaticsVariables.get_tau_init()
    assert actual == expected
