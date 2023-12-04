import numpy as np

from bioptim_gui_api.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.misc.pike_with_visual_acrobatics_variables import PikeAcrobaticsWithVisualVariables
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import StraightAcrobaticsVariables
from bioptim_gui_api.variables.misc.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import TuckAcrobaticsVariables
from bioptim_gui_api.variables.misc.tuck_with_visual_acrobatics_variables import TuckAcrobaticsWithVisualVariables


def variables_zeros(dimension: int, interpolation_type: str) -> list:
    """
    Return a zero array with the appropriate dimension depending on the interpolation type

    Parameters
    ----------
    dimension: int
        The dimension of the variable
    interpolation_type: str
        The type of interpolation ("LINEAR", "CONSTANT", "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT")

    Returns
    -------
    The array of zeros
    """
    if interpolation_type == "LINEAR":
        return np.zeros((dimension, 2)).tolist()
    elif interpolation_type == "CONSTANT":
        return np.zeros((dimension, 1)).tolist()
    elif interpolation_type == "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT":
        return np.zeros((dimension, 3)).tolist()
    else:
        raise ValueError(f"Interpolation type {interpolation_type} not implemented")


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
