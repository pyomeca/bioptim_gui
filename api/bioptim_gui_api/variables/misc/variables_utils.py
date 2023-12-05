import numpy as np


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
    else:
        return np.deg2rad(45)


def define_loose_bounds(bound: np.ndarray, dof: int, node: int, bound_value: float, looseness: float = 0.0) -> None:
    if node is None:
        bound["min"][dof, :] = bound_value - looseness
        bound["max"][dof, :] = bound_value + looseness
    else:
        bound["min"][dof, node] = bound_value - looseness
        bound["max"][dof, node] = bound_value + looseness
