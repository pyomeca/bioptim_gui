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
@pytest.mark.parametrize("nb_somersaults", [2, 3, 4])
def test_qdot_init_same_as_baseline(variable_compute, baseline, nb_somersaults):
    q_bounds = variable_compute.get_q_bounds([0] * nb_somersaults, False)
    nb_phases = len(q_bounds)

    phase_durations = [0] * (nb_phases - 1) + [1.7]
    final_time = sum(phase_durations)

    expected = baseline.get_qdot_init(nb_somersaults, final_time)
    actual = variable_compute.get_qdot_init(nb_somersaults, phase_durations)
    assert actual == expected
