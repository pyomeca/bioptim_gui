import copy

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
