import copy

from bioptim_gui_api.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.misc.pike_with_visual_acrobatics_variables import PikeAcrobaticsWithVisualVariables
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import StraightAcrobaticsVariables
from bioptim_gui_api.variables.misc.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import TuckAcrobaticsVariables
from bioptim_gui_api.variables.misc.tuck_with_visual_acrobatics_variables import TuckAcrobaticsWithVisualVariables
from bioptim_gui_api.variables.misc.variables_utils import variables_zeros


def default_bounds_initial_guess(
    name: str,
    dimension: int = 1,
    bounds_interpolation_type: str = "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
    initial_guess_interpolation_type: str = "CONSTANT",
):
    bounds = variables_zeros(dimension, bounds_interpolation_type)
    initial_guess = variables_zeros(dimension, initial_guess_interpolation_type)

    return {
        "name": f"{name}",
        "dimension": 1,
        "bounds_interpolation_type": f"{bounds_interpolation_type}",
        "bounds": {"min_bounds": copy.deepcopy(bounds), "max_bounds": copy.deepcopy(bounds)},
        "initial_guess_interpolation_type": f"{initial_guess_interpolation_type}",
        "initial_guess": initial_guess,
    }


class DefaultVariablesConfig:
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
            default_bounds_initial_guess("q"),
            default_bounds_initial_guess("qdot"),
        ],
        "control_variables": [
            default_bounds_initial_guess("tau"),
        ],
    }


def get_variable_computer(position: str = "straight", with_visual_criteria: bool = False):
    with_visual = {
        "straight": StraightAcrobaticsWithVisualVariables,
        "tuck": TuckAcrobaticsWithVisualVariables,
        "pike": PikeAcrobaticsWithVisualVariables,
    }

    without_visual = {
        "straight": StraightAcrobaticsVariables,
        "tuck": TuckAcrobaticsVariables,
        "pike": PikeAcrobaticsVariables,
    }

    if with_visual_criteria:
        return with_visual[position]
    else:
        return without_visual[position]
