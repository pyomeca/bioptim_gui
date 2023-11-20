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
