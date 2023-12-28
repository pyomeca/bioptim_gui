import copy
from typing import Type

from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.misc.pike_acrobatics_variables_with_spine import PikeAcrobaticsVariablesWithSpine
from bioptim_gui_api.variables.misc.pike_with_visual_acrobatics_variables import PikeAcrobaticsWithVisualVariables
from bioptim_gui_api.variables.misc.pike_with_visual_acrobatics_variables_with_spine import (
    PikeAcrobaticsWithVisualVariablesWithSpine,
)
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import StraightAcrobaticsVariables
from bioptim_gui_api.variables.misc.straight_acrobatics_variables_with_spine import StraightAcrobaticsVariablesWithSpine
from bioptim_gui_api.variables.misc.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.variables.misc.straight_with_visual_acrobatics_variables_with_spine import (
    StraightAcrobaticsWithVisualVariablesWithSpine,
)
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import TuckAcrobaticsVariables
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables_with_spine import TuckAcrobaticsVariablesWithSpine
from bioptim_gui_api.variables.misc.tuck_with_visual_acrobatics_variables import TuckAcrobaticsWithVisualVariables
from bioptim_gui_api.variables.misc.tuck_with_visual_acrobatics_variables_with_spine import (
    TuckAcrobaticsWithVisualVariablesWithSpine,
)
from bioptim_gui_api.variables.misc.variables_utils import variables_zeros


def default_bounds_initial_guess(
    name: str,
    dimension: int = 1,
    bounds_interpolation_type: str = "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
    initial_guess_interpolation_type: str = "CONSTANT",
):
    """
    Return the default information for a variable
    """
    bounds = variables_zeros(dimension, bounds_interpolation_type)
    initial_guess = variables_zeros(dimension, initial_guess_interpolation_type)

    return {
        "name": f"{name}",
        "dimension": dimension,
        "bounds_interpolation_type": f"{bounds_interpolation_type}",
        "bounds": {"min_bounds": copy.deepcopy(bounds), "max_bounds": copy.deepcopy(bounds)},
        "initial_guess_interpolation_type": f"{initial_guess_interpolation_type}",
        "initial_guess": initial_guess,
    }


class DefaultVariablesConfig:
    """
    Default variables config depending on choosen dynamics

    Attributes
    ----------
    default_dummy_variables: dict
        The default dummy variables

    default_torque_driven_variables: dict
        The default torque driven variables

    """

    default_dummy_variables = {
        "state_variables": [
            default_bounds_initial_guess("coucou"),
        ],
        "control_variables": [
            default_bounds_initial_guess("tata"),
        ],
    }

    default_torque_driven_variables = {
        "state_variables": [
            default_bounds_initial_guess(
                "q",
                bounds_interpolation_type="CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                initial_guess_interpolation_type="LINEAR",
            ),
            default_bounds_initial_guess(
                "qdot",
                bounds_interpolation_type="CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                initial_guess_interpolation_type="CONSTANT",
            ),
        ],
        "control_variables": [
            default_bounds_initial_guess(
                "tau", bounds_interpolation_type="CONSTANT", initial_guess_interpolation_type="CONSTANT"
            ),
        ],
    }


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
