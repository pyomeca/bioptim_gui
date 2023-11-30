import pytest

from bioptim_gui_api.variables.misc.pike_acrobatics_variables import (
    PikeAcrobaticsVariables,
)


# P pike
# S somersault
# K kick out
# T twist
# W waiting
# L landing
@pytest.mark.parametrize(
    ("half_twists", "phases_str"),
    [
        ([0, 0], "PSKWL"),
        ([1, 0], "TPSKWL"),
        ([0, 1], "PSKTL"),
        ([1, 1], "TPSKTL"),
        ([0, 0, 0], "PSKWL"),
        ([0, 0, 1], "PSKTL"),
        ([0, 1, 0], "PSKTPSKWL"),
        ([0, 1, 1], "PSKTPSKTL"),
        ([1, 0, 0], "TPSKWL"),
        ([1, 0, 1], "TPSKTL"),
        ([1, 1, 0], "TPSKTPSKWL"),
        ([0, 0, 0, 0], "PSKWL"),
        ([0, 0, 0, 1], "PSKTL"),
        ([0, 0, 1, 0], "PSKTPSKWL"),
        ([0, 0, 1, 1], "PSKTPSKTL"),
        ([0, 1, 0, 0], "PSKTPSKWL"),
        ([0, 1, 0, 1], "PSKTPSKTL"),
        ([0, 1, 1, 0], "PSKTPSKTPSKWL"),
        ([0, 1, 1, 1], "PSKTPSKTPSKTL"),
        ([1, 0, 0, 0], "TPSKWL"),
        ([1, 0, 0, 1], "TPSKTL"),
        ([1, 0, 1, 0], "TPSKTPSKWL"),
        ([1, 0, 1, 1], "TPSKTPSKTL"),
        ([1, 1, 0, 0], "TPSKTPSKWL"),
        ([1, 1, 0, 1], "TPSKTPSKTL"),
        ([1, 1, 1, 0], "TPSKTPSKTPSKWL"),
        ([1, 1, 1, 1], "TPSKTPSKTPSKTL"),
    ],
)
def test_q_bounds_number(half_twists, phases_str):
    phases = PikeAcrobaticsVariables.get_q_bounds(
        half_twists=half_twists,
        prefer_left=False,
    )
    assert len(phases) == len(phases_str)
    # assert expected_number_of_phase == len(phases_str) # to check if the test is correctly written
    # assert "".join(phases) == phases_str
