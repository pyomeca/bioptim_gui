import pytest

from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.pike_acrobatics_variables import (
    PikeAcrobaticsVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.tuck_acrobatics_variables import (
    TuckAcrobaticsVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.pike_acrobatics_variables import (
    PikeAcrobaticsVariables as BasePikeAcrobaticsVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.pike_with_visual_acrobatics_variables import (
    PikeAcrobaticsWithVisualVariables as BasePikeAcrobaticsWithVisualVariables,
    PikeAcrobaticsWithVisualVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.straight_acrobatics_variables import (
    StraightAcrobaticsVariables as BaseStraightAcrobaticsVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables as BaseStraightAcrobaticsWithVisualVariables,
    StraightAcrobaticsWithVisualVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.tuck_acrobatics_variables import (
    TuckAcrobaticsVariables as BaseTuckAcrobaticsVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.tuck_with_visual_acrobatics_variables import (
    TuckAcrobaticsWithVisualVariables as BaseTuckAcrobaticsWithVisualVariables,
    TuckAcrobaticsWithVisualVariables,
)


def test_tau_bounds_straight():
    expected_min = [-500.0, -500.0, -500.0, -500.0]
    expected_max = [500.0, 500.0, 500.0, 500.0]
    actual = StraightAcrobaticsVariables.get_tau_bounds()
    actual_min, actual_max = actual["min"], actual["max"]
    assert actual_min == expected_min
    assert actual_max == expected_max


def test_tau_bounds_pike():
    expected_min = [-500.0] * 10
    expected_max = [500.0] * 10
    actual = PikeAcrobaticsVariables.get_tau_bounds()
    actual_min, actual_max = actual["min"], actual["max"]
    assert actual_min == expected_min
    assert actual_max == expected_max


def test_tau_bounds_tuck():
    expected_min = [-500.0] * 11
    expected_max = [500.0] * 11
    actual = TuckAcrobaticsVariables.get_tau_bounds()
    actual_min, actual_max = actual["min"], actual["max"]
    assert actual_min == expected_min
    assert actual_max == expected_max


@pytest.mark.parametrize(
    ("variable_compute", "baseline"),
    [
        (StraightAcrobaticsVariables, BaseStraightAcrobaticsVariables),
        (PikeAcrobaticsVariables, BasePikeAcrobaticsVariables),
        (TuckAcrobaticsVariables, BaseTuckAcrobaticsVariables),
        (StraightAcrobaticsWithVisualVariables, BaseStraightAcrobaticsWithVisualVariables),
        (PikeAcrobaticsWithVisualVariables, BasePikeAcrobaticsWithVisualVariables),
        (TuckAcrobaticsWithVisualVariables, BaseTuckAcrobaticsWithVisualVariables),
    ],
)
def test_tau_bounds_same_as_baseline(variable_compute, baseline):
    expected = baseline.get_tau_bounds()
    actual = variable_compute.get_tau_bounds()
    assert actual == expected
