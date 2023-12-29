import numpy as np


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
