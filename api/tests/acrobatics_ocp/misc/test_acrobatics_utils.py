import pytest

from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_utils import acrobatics_phase_names


# P pike
# S somersault
# K kick out
# T twist
# D Decorative
# L landing
@pytest.mark.parametrize(
    ("half_twists", "phases_str"),
    [
        ([0, 0], "PSKDL"),
        ([1, 0], "TPSKDL"),
        ([0, 1], "PSKTL"),
        ([1, 1], "TPSKTL"),
        ([0, 0, 0], "PSKDL"),
        ([0, 0, 1], "PSKTL"),
        ([0, 1, 0], "PSKTPSKDL"),
        ([0, 1, 1], "PSKTPSKTL"),
        ([1, 0, 0], "TPSKDL"),
        ([1, 0, 1], "TPSKTL"),
        ([1, 1, 0], "TPSKTPSKDL"),
        ([0, 0, 0, 0], "PSKDL"),
        ([0, 0, 0, 1], "PSKTL"),
        ([0, 0, 1, 0], "PSKTPSKDL"),
        ([0, 0, 1, 1], "PSKTPSKTL"),
        ([0, 1, 0, 0], "PSKTPSKDL"),
        ([0, 1, 0, 1], "PSKTPSKTL"),
        ([0, 1, 1, 0], "PSKTPSKTPSKDL"),
        ([0, 1, 1, 1], "PSKTPSKTPSKTL"),
        ([1, 0, 0, 0], "TPSKDL"),
        ([1, 0, 0, 1], "TPSKTL"),
        ([1, 0, 1, 0], "TPSKTPSKDL"),
        ([1, 0, 1, 1], "TPSKTPSKTL"),
        ([1, 1, 0, 0], "TPSKTPSKDL"),
        ([1, 1, 0, 1], "TPSKTPSKTL"),
        ([1, 1, 1, 0], "TPSKTPSKTPSKDL"),
        ([1, 1, 1, 1], "TPSKTPSKTPSKTL"),
    ],
)
def test_phases_names_pike(half_twists, phases_str):
    nb_somersaults = len(half_twists)
    position = "pike"
    names = acrobatics_phase_names(nb_somersaults, position, half_twists)
    assert len(names) == len(phases_str)

    for i, name in enumerate(names):
        assert phases_str[i] == name[0]


@pytest.mark.parametrize(
    ("half_twists", "expected_number_of_phase", "phases_str"),
    [
        ([0, 0], 3, ["Somersault 1", "Somersault 2", "Landing"]),
        ([1, 0], 3, ["Somersault 1", "Somersault 2", "Landing"]),
        ([0, 1], 3, ["Somersault 1", "Somersault 2", "Landing"]),
        ([1, 1], 3, ["Somersault 1", "Somersault 2", "Landing"]),
        ([0, 0, 0], 4, ["Somersault 1", "Somersault 2", "Somersault 3", "Landing"]),
        ([0, 0, 1], 4, ["Somersault 1", "Somersault 2", "Somersault 3", "Landing"]),
    ],
)
def test_phase_names_straight(half_twists, expected_number_of_phase, phases_str):
    nb_somersaults = len(half_twists)
    position = "straight"
    names = acrobatics_phase_names(nb_somersaults, position, half_twists)
    assert len(names) == expected_number_of_phase

    for i, name in enumerate(names):
        assert phases_str[i] == name
