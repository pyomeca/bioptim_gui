from typing import NamedTuple

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
    if interpolation_type == "CONSTANT":
        return np.zeros((dimension, 1)).tolist()
    if interpolation_type == "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT":
        return np.zeros((dimension, 3)).tolist()
    raise ValueError(f"Interpolation type {interpolation_type} not implemented")


def bounds_after_interpolation_type_change(old_variable: dict, interpolation_type: str) -> None:
    """
    If the old and new interpolation type are the same, do nothing

    Any -> constant : use the average as new value
    Any -> linear: use first and last value as new value (the same if it was constant)
    Any -> constant_with_first_and_last_different:
        use first and last value as new value (the same if it was constant)
        use min(first, last) as intermediate value for min_bounds
        use max(first, last) as intermediate value for max_bounds

    Parameters
    ----------
    old_variable: dict
        The variable to modify
    new_interpolation_type: str
        The new interpolation type
    Returns
    -------
    None
    """
    if interpolation_type == old_variable["bounds_interpolation_type"]:
        return

    min_bound = np.array(old_variable["bounds"]["min_bounds"])
    max_bound = np.array(old_variable["bounds"]["max_bounds"])

    if interpolation_type == "CONSTANT":
        new_min_bounds = np.array([(min_bound[:, 0] + min_bound[:, -1]) / 2]).T
        new_max_bounds = np.array([(max_bound[:, 0] + max_bound[:, -1]) / 2]).T
        old_variable["bounds"]["min_bounds"] = np.round(new_min_bounds, 2).tolist()
        old_variable["bounds"]["max_bounds"] = np.round(new_max_bounds, 2).tolist()
    if interpolation_type == "LINEAR":
        old_variable["bounds"]["min_bounds"] = np.round(min_bound[:, [0, -1]], 2).tolist()
        old_variable["bounds"]["max_bounds"] = np.round(max_bound[:, [0, -1]], 2).tolist()
    if interpolation_type == "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT":
        min_bound_middle = np.minimum(min_bound[:, 0], min_bound[:, -1])
        new_min = np.column_stack((min_bound[:, 0], min_bound_middle, min_bound[:, -1]))
        old_variable["bounds"]["min_bounds"] = np.round(new_min, 2).tolist()

        max_bound_middle = np.maximum(max_bound[:, 0], max_bound[:, -1])
        new_max = np.column_stack((max_bound[:, 0], max_bound_middle, max_bound[:, -1]))
        old_variable["bounds"]["max_bounds"] = np.round(new_max, 2).tolist()

    old_variable["bounds_interpolation_type"] = interpolation_type


def init_guess_after_interpolation_type_change(old_variable: dict, interpolation_type: str) -> None:
    """
    Any -> constant : use the average as new value
    Any -> linear: use first and last value as new value (the same if it was constant)
    Any -> constant_with_first_and_last_different:
        use first[0] and last[-1] value as new value (the same if it was constant)
        use average as intermediate value

    Parameters
    ----------
    old_variable: dict
        The variable to modify
    new_interpolation_type: str
        The new interpolation type

    Returns
    -------
    None
    """
    if interpolation_type == old_variable["initial_guess_interpolation_type"]:
        return

    old_init_guess = np.array(old_variable["initial_guess"])

    if interpolation_type == "CONSTANT":
        new_init_guess = np.array([(old_init_guess[:, 0] + old_init_guess[:, -1]) / 2]).T
        old_variable["initial_guess"] = np.round(new_init_guess, 2).tolist()
    if interpolation_type == "LINEAR":
        old_variable["initial_guess"] = np.round(old_init_guess[:, [0, -1]], 2).tolist()
    if interpolation_type == "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT":
        middle_col = np.array([(old_init_guess[:, 0] + old_init_guess[:, -1]) / 2]).T
        new_init = np.column_stack((old_init_guess[:, 0], middle_col, old_init_guess[:, -1]))
        old_variable["initial_guess"] = np.round(new_init, 2).tolist()

    old_variable["initial_guess_interpolation_type"] = interpolation_type


class LooseValue(NamedTuple):
    """
    A value with a looseness
    """

    value: float
    looseness: float = 0.0


def define_loose_bounds(bound: np.ndarray, dof: int, node: int, loose_value: LooseValue) -> None:
    """
    Define the bounds with a looseness around a value, the min and max are modified so the values are value +- looseness

    Parameters
    ----------
    bound: np.ndarray
        The bound to modify
    dof: int
        The degree of freedom to modify
    node: int
        The node to modify (0,1,2 : START, MIDDLE, END)
    loose_value: LooseValue
        The value and looseness to set

    Returns
    -------
    None
    """
    value, looseness = loose_value.value, loose_value.looseness
    if node is None:
        bound["min"][dof, :] = value - looseness
        bound["max"][dof, :] = value + looseness
    else:
        bound["min"][dof, node] = value - looseness
        bound["max"][dof, node] = value + looseness
