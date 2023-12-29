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
@pytest.mark.parametrize("prefer_left", [True, False])
@pytest.mark.parametrize(
    "half_twist",
    [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ],
)
def test_q_init(variable_compute, baseline, prefer_left, half_twist):
    expected = baseline.get_q_init(half_twist, prefer_left)
    actual = variable_compute.get_q_init(half_twist, prefer_left)

    assert len(expected) == len(actual)
    assert np.allclose(expected, actual)
