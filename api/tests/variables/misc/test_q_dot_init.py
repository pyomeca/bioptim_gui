import pytest

from bioptim_gui_api.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import StraightAcrobaticsVariables
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import TuckAcrobaticsVariables
from tests.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables as BasePikeAcrobaticsVariables
from tests.variables.misc.pike_with_visual_acrobatics_variables import (
    PikeAcrobaticsWithVisualVariables as BasePikeAcrobaticsWithVisualVariables,
    PikeAcrobaticsWithVisualVariables,
)
from tests.variables.misc.straight_acrobatics_variables import (
    StraightAcrobaticsVariables as BaseStraightAcrobaticsVariables,
)
from tests.variables.misc.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables as BaseStraightAcrobaticsWithVisualVariables,
    StraightAcrobaticsWithVisualVariables,
)
from tests.variables.misc.tuck_acrobatics_variables import TuckAcrobaticsVariables as BaseTuckAcrobaticsVariables
from tests.variables.misc.tuck_with_visual_acrobatics_variables import (
    TuckAcrobaticsWithVisualVariables as BaseTuckAcrobaticsWithVisualVariables,
    TuckAcrobaticsWithVisualVariables,
)


def test_qdot_init_straight():
    expected = [0.0] * 10
    actual = StraightAcrobaticsVariables.get_qdot_init()
    assert actual == expected


def test_qdot_init_pike():
    expected = [0.0] * 17
    actual = TuckAcrobaticsVariables.get_qdot_init()
    assert actual == expected


def test_qdot_init_tuck():
    expected = [0.0] * 16
    actual = PikeAcrobaticsVariables.get_qdot_init()
    assert actual == expected


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
def test_qdot_init_same_as_baseline(variable_compute, baseline):
    expected = baseline.get_qdot_init()
    actual = variable_compute.get_qdot_init()
    assert actual == expected
