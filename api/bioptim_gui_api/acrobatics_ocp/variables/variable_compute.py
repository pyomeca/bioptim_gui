from typing import Type

from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.pike_acrobatics_variables import (
    PikeAcrobaticsVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.pike_acrobatics_variables_with_spine import (
    PikeAcrobaticsVariablesWithSpine,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.pike_with_visual_acrobatics_variables import (
    PikeAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.pike_with_visual_acrobatics_variables_with_spine import (
    PikeAcrobaticsWithVisualVariablesWithSpine,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.straight_acrobatics_variables_with_spine import (
    StraightAcrobaticsVariablesWithSpine,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.straight_with_visual_acrobatics_variables_with_spine import (
    StraightAcrobaticsWithVisualVariablesWithSpine,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.tuck_acrobatics_variables import (
    TuckAcrobaticsVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.tuck_acrobatics_variables_with_spine import (
    TuckAcrobaticsVariablesWithSpine,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.tuck_with_visual_acrobatics_variables import (
    TuckAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.tuck_with_visual_acrobatics_variables_with_spine import (
    TuckAcrobaticsWithVisualVariablesWithSpine,
)


def get_variable_computer(
    position: str = "straight", additional_criteria: AdditionalCriteria = None
) -> Type[StraightAcrobaticsVariables]:
    """
    Return the variable computer (to compute bounds and initial_guess for q, qdot, tau) depending on the position and
    the visual criteria and spine criteria.

    Parameters
    ----------
    position: str
        The position ("straight", "tuck", "pike")
    additional_criteria: AdditionalCriteria
        The additional criteria (e.g. with_visual_criteria, collision_constraint, without_cone)

    Returns
    -------
    The variable computer
    """

    visual_spine_position_to_converter = {
        (False, False, "straight"): StraightAcrobaticsVariables,
        (False, False, "tuck"): TuckAcrobaticsVariables,
        (False, False, "pike"): PikeAcrobaticsVariables,
        (True, False, "straight"): StraightAcrobaticsWithVisualVariables,
        (True, False, "tuck"): TuckAcrobaticsWithVisualVariables,
        (True, False, "pike"): PikeAcrobaticsWithVisualVariables,
        (False, True, "straight"): StraightAcrobaticsVariablesWithSpine,
        (False, True, "tuck"): TuckAcrobaticsVariablesWithSpine,
        (False, True, "pike"): PikeAcrobaticsVariablesWithSpine,
        (True, True, "straight"): StraightAcrobaticsWithVisualVariablesWithSpine,
        (True, True, "tuck"): TuckAcrobaticsWithVisualVariablesWithSpine,
        (True, True, "pike"): PikeAcrobaticsWithVisualVariablesWithSpine,
    }

    return visual_spine_position_to_converter[
        (additional_criteria.with_visual_criteria, additional_criteria.with_spine, position)
    ]
