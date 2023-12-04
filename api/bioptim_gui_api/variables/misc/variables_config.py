import copy

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
