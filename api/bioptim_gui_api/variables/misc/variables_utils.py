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
