import pytest

from bioptim_gui_api.acrobatics_ocp.acrobatics_utils import acrobatics_phase_names


# P pike
# S somersault
# K kick out
# T twist
# L landing
@pytest.mark.parametrize(
    ("half_twists", "expected_number_of_phase", "phases_str"),
    [
        ([0, 0], 4, "PSKL"),
        ([1, 0], 5, "TPSKL"),
        ([0, 1], 5, "PSKTL"),
        ([1, 1], 6, "TPSKTL"),
        ([0, 0, 0], 4, "PSKL"),
        ([0, 0, 1], 5, "PSKTL"),
        ([0, 1, 0], 8, "PSKTPSKL"),
        ([0, 1, 1], 9, "PSKTPSKTL"),
        ([1, 0, 0], 5, "TPSKL"),
        ([1, 0, 1], 6, "TPSKTL"),
        ([1, 1, 0], 9, "TPSKTPSKL"),
        ([0, 0, 0, 0], 4, "PSKL"),
        ([0, 0, 0, 1], 5, "PSKTL"),
        ([0, 0, 1, 0], 8, "PSKTPSKL"),
        ([0, 0, 1, 1], 9, "PSKTPSKTL"),
        ([0, 1, 0, 0], 8, "PSKTPSKL"),
        ([0, 1, 0, 1], 9, "PSKTPSKTL"),
        ([0, 1, 1, 0], 12, "PSKTPSKTPSKL"),
        ([0, 1, 1, 1], 13, "PSKTPSKTPSKTL"),
        ([1, 0, 0, 0], 5, "TPSKL"),
        ([1, 0, 0, 1], 6, "TPSKTL"),
        ([1, 0, 1, 0], 9, "TPSKTPSKL"),
        ([1, 0, 1, 1], 10, "TPSKTPSKTL"),
        ([1, 1, 0, 0], 9, "TPSKTPSKL"),
        ([1, 1, 0, 1], 10, "TPSKTPSKTL"),
        ([1, 1, 1, 0], 13, "TPSKTPSKTPSKL"),
        ([1, 1, 1, 1], 14, "TPSKTPSKTPSKTL"),
    ],
)
def test_phases_names_pike(half_twists, expected_number_of_phase, phases_str):
    nb_somersaults = len(half_twists)
    position = "pike"
    names = acrobatics_phase_names(nb_somersaults, position, half_twists)
    assert len(names) == expected_number_of_phase

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
