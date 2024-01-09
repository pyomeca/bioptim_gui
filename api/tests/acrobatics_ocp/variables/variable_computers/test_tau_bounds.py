import numpy as np
import pytest

from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.pike_acrobatics_variables import (
    PikeAcrobaticsVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.pike_with_visual_acrobatics_variables import (
    PikeAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.tuck_acrobatics_variables import (
    TuckAcrobaticsVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.tuck_with_visual_acrobatics_variables import (
    TuckAcrobaticsWithVisualVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.pike_acrobatics_variables import (
    PikeAcrobaticsVariables as BasePikeAcrobaticsVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.pike_with_visual_acrobatics_variables import (
    PikeAcrobaticsWithVisualVariables as BasePikeAcrobaticsWithVisualVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.straight_acrobatics_variables import (
    StraightAcrobaticsVariables as BaseStraightAcrobaticsVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables as BaseStraightAcrobaticsWithVisualVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.tuck_acrobatics_variables import (
    TuckAcrobaticsVariables as BaseTuckAcrobaticsVariables,
)
from tests.acrobatics_ocp.variables.variable_computers.tuck_with_visual_acrobatics_variables import (
    TuckAcrobaticsWithVisualVariables as BaseTuckAcrobaticsWithVisualVariables,
)


def test_tau_bounds_straight():
    expected_min = [-500.0, -500.0, -500.0, -500.0]
    expected_max = [500.0, 500.0, 500.0, 500.0]
    for nb_phases in range(1, 5):
        actual = StraightAcrobaticsVariables.get_tau_bounds(nb_phases)

        for i in range(nb_phases):
            assert np.allclose(actual[i]["min"], expected_min)
            assert np.allclose(actual[i]["max"], expected_max)


def test_tau_bounds_pike():
    expected_min = [-500.0] * 10
    expected_max = [500.0] * 10
    for nb_phases in range(1, 5):
        actual = PikeAcrobaticsVariables.get_tau_bounds(nb_phases)

        for i in range(nb_phases):
            assert np.allclose(actual[i]["min"], expected_min)
            assert np.allclose(actual[i]["max"], expected_max)


def test_tau_bounds_tuck():
    expected_min = [-500.0] * 11
    expected_max = [500.0] * 11
    for nb_phases in range(1, 5):
        actual = TuckAcrobaticsVariables.get_tau_bounds(nb_phases)

        for i in range(nb_phases):
            assert np.allclose(actual[i]["min"], expected_min)
            assert np.allclose(actual[i]["max"], expected_max)


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
    for nb_phases in range(1, 5):
        expected = baseline.get_tau_bounds(nb_phases)
        actual = variable_compute.get_tau_bounds(nb_phases)
        for i in range(nb_phases):
            assert np.allclose(actual[i]["min"], expected[i]["min"])
            assert np.allclose(actual[i]["max"], expected[i]["max"])
