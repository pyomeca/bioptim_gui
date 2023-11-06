import numpy as np

from bioptim_gui_api.variables.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)


class PikeAcrobaticsVariables(StraightAcrobaticsVariables):
    X = 0
    Y = 1
    Z = 2
    Xrot = 3
    Yrot = 4
    Zrot = 5
    ZrotRightUpperArm = 6
    YrotRightUpperArm = 7
    ZrotRightLowerArm = 8
    XrotRightLowerArm = 9
    ZrotLeftUpperArm = 10
    YrotLeftUpperArm = 11
    ZrotLeftLowerArm = 12
    XrotLeftLowerArm = 13
    XrotUpperLegs = 14
    YrotUpperLegs = 15

    nb_q, nb_qdot, nb_tau = 16, 16, 10

    q_min_bounds = np.array(
        [
            [-1, -1, -1],
            [-1, -1, -1],
            [-0.1, -0.1, -0.1],
            [0, 0, 0],
            [-np.pi / 4, -np.pi / 4, -np.pi / 4],
            [0, 0, 0],
            [-0.65, -0.65, -0.65],
            [-0.05, -0.05, -0.05],
            [-1.8, -1.8, -1.8],
            [-2.65, -2.65, -2.65],
            [-2.0, -2.0, -2.0],
            [-3.0, -3.0, -3.0],
            [-1.1, -1.1, -1.1],
            [-2.65, -2.65, -2.65],
            [-2.7, -2.7, -2.7],
            [-0.1, -0.1, -0.1],
        ]
    )

    q_max_bounds = np.array(
        [
            [1, 1, 1],
            [1, 1, 1],
            [10, 10, 10],
            [0, 0, 0],
            [np.pi / 4, np.pi / 4, np.pi / 4],
            [0, 0, 0],
            [2.0, 2.0, 2.0],
            [3.0, 3.0, 3.0],
            [1.1, 1.1, 1.1],
            [0.0, 0.0, 0.0],
            [0.65, 0.65, 0.65],
            [0.05, 0.05, 0.05],
            [1.8, 1.8, 1.8],
            [0.0, 0.0, 0.0],
            [0.3, 0.3, 0.3],
            [0.1, 0.1, 0.1],
        ]
    )

    @classmethod
    def get_q_bounds(cls, half_twists: list, prefer_left: bool) -> dict:
        nb_somersaults = len(half_twists)
        bounds = []
        current_somersault = 1

        # twists
        if half_twists[0] > 0:
            bounds.append("T")

        last_have_twist = True
        next_have_twist = half_twists[1] > 0
        for i in range(1, nb_somersaults):
            is_last_somersault = i == nb_somersaults - 1
            # piking
            if last_have_twist:
                bounds.append("P")

            # somersaulting
            if i == nb_somersaults - 1 or next_have_twist:
                bounds.append("S")

            # kick out
            if next_have_twist or is_last_somersault:
                bounds.append("K")

            if next_have_twist:
                bounds.append("T")

            last_have_twist = next_have_twist
            next_have_twist = is_last_somersault or half_twists[i + 1] > 0

        # landing
        bounds.append("L")

        return bounds
