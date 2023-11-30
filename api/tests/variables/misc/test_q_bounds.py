import numpy as np
import pytest

from bioptim_gui_api.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.misc.pike_with_visual_acrobatics_variables import PikeAcrobaticsWithVisualVariables
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import StraightAcrobaticsVariables
from bioptim_gui_api.variables.misc.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import TuckAcrobaticsVariables
from bioptim_gui_api.variables.misc.tuck_with_visual_acrobatics_variables import TuckAcrobaticsWithVisualVariables
from tests.variables.baseline.pike_acrobatics_variables import PikeAcrobaticsVariables as BasePikeAcrobaticsVariables
from tests.variables.baseline.pike_with_visual_acrobatics_variables import (
    PikeAcrobaticsWithVisualVariables as BasePikeAcrobaticsWithVisualVariables,
)
from tests.variables.baseline.straight_acrobatics_variables import (
    StraightAcrobaticsVariables as BaseStraightAcrobaticsVariables,
)
from tests.variables.baseline.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables as BaseStraightAcrobaticsWithVisualVariables,
)
from tests.variables.baseline.tuck_acrobatics_variables import TuckAcrobaticsVariables as BaseTuckAcrobaticsVariables
from tests.variables.baseline.tuck_with_visual_acrobatics_variables import (
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
def test_q_bounds(variable_compute, baseline, prefer_left, half_twist):
    expected = baseline.get_q_bounds(half_twist, prefer_left)
    actual = variable_compute.get_q_bounds(half_twist, prefer_left)

    assert len(expected) == len(actual)

    for i in range(len(expected)):
        assert np.allclose(expected[i]["min"], actual[i]["min"])
        assert np.allclose(expected[i]["max"], actual[i]["max"])
