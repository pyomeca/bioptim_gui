from enum import Enum

import numpy as np


class BioptimVariable(str, Enum):
    STATE_VARIABLE = "state_variables"
    CONTROL_VARIABLE = "control_variables"


def maximum_fig_arms_angle(half_twists: list) -> float:
    """
    # FIG Code of Points 14.5, arms to stop twisting rotation
    Moving arms away from the body is acceptable to stop a twisting rotation. The maximum of the angle
    between the trunk and the arms should be:
    Barani, Full, multiple somersaults with ½ out movements 45°
    More than full twist and all other multiple twisting somersaults 90°
    """
    nb_somersaults = len(half_twists)
    half_twist_out = half_twists[-1]

    if (nb_somersaults == 1 and half_twist_out > 2) or (nb_somersaults > 1 and half_twist_out >= 2):
        return np.deg2rad(90)
    return np.deg2rad(45)


def var_bounds_list(data: dict, variable_name: str, var_type: BioptimVariable) -> list[dict]:
    """
    Return the list of all phases bounds (min and max) and interpolation type for the given variable

    Parameters
    ----------
    data: dict
        The data from OCP
    variable_name: str
        The name of the variable to get the bounds
    var_type: BioptimVariable
        The type of variable to get the bounds

    Returns
    -------
    list[dict]
        The list of all phases bounds (min and max) and interpolation type for the given variable
    """
    bounds = []

    for phase in data["phases_info"]:
        for var in phase[var_type.value]:
            if var["name"] == variable_name:
                bounds.append(
                    {
                        "min": var["bounds"]["min_bounds"],
                        "max": var["bounds"]["max_bounds"],
                        "interpolation_type": var["bounds_interpolation_type"],
                    }
                )

    return bounds


def var_initial_guess_list(data: dict, variable_name: str, var_type: BioptimVariable) -> list[dict]:
    """
    Return the list of all phases initial guess and interpolation type for the given variable

    Parameters
    ----------
    data: dict
        The data from OCP
    variable_name: str
        The name of the variable to get the initial guess
    var_type: BioptimVariable
        The type of variable to get the initial guess

    Returns
    -------
    list[dict]
        The list of all phases initial guess and interpolation type for the given variable
    """
    init = []

    for phase in data["phases_info"]:
        for var in phase[var_type.value]:
            if var["name"] == variable_name:
                init.append(
                    {
                        "initial_guess": var["initial_guess"],
                        "interpolation_type": var["initial_guess_interpolation_type"],
                    }
                )

    return init
