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
@pytest.mark.parametrize("nb_somersaults", [2, 3, 4])
def test_qdot_init_same_as_baseline(variable_compute, baseline, nb_somersaults):
    expected = baseline.get_qdot_init(nb_somersaults)
    actual = variable_compute.get_qdot_init(nb_somersaults)
    assert actual == expected
