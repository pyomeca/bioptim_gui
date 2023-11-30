import numpy as np

from tests.variables.misc.pike_acrobatics_variables import (
    PikeAcrobaticsVariables,
)


class PikeAcrobaticsWithVisualVariables(PikeAcrobaticsVariables):
    X = 0
    Y = 1
    Z = 2
    Xrot = 3
    Yrot = 4
    Zrot = 5
    ZrotHead = 6
    XrotHead = 7
    ZrotEyes = 8
    XrotEyes = 9
    ZrotRightUpperArm = 10
    YrotRightUpperArm = 11
    ZrotRightLowerArm = 12
    XrotRightLowerArm = 13
    ZrotLeftUpperArm = 14
    YrotLeftUpperArm = 15
    ZrotLeftLowerArm = 16
    XrotLeftLowerArm = 17
    XrotUpperLegs = 18
    YrotUpperLegs = 19

    nb_q, nb_qdot, nb_tau = 20, 20, 14

    q_min_bounds = np.array(
        [
            [-1, -1, -1],
            [-1, -1, -1],
            [-0.1, -0.1, -0.1],
            [0, 0, 0],
            [-np.pi / 4, -np.pi / 4, -np.pi / 4],
            [0, 0, 0],
            [-np.pi / 3, -np.pi / 3, -np.pi / 3],
            [-70 * np.pi / 180] * 3,
            [-np.pi / 8] * 3,
            [-np.pi / 6] * 3,
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
            [np.pi / 3, np.pi / 3, np.pi / 3],
            [np.pi / 8] * 3,
            [np.pi / 8] * 3,
            [np.pi / 6] * 3,
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
        bounds = super().get_q_bounds(half_twists, prefer_left)
        bounds[0]["min"][cls.ZrotHead, 0] = -0.1
        bounds[0]["max"][cls.ZrotHead, 0] = 0.1
        bounds[0]["min"][cls.XrotHead, 0] = -0.1
        bounds[0]["max"][cls.XrotHead, 0] = 0.1
        bounds[0]["min"][cls.ZrotEyes, 0] = -0.1
        bounds[0]["max"][cls.ZrotEyes, 0] = 0.1
        bounds[0]["min"][cls.XrotEyes, 0] = np.pi / 8 - 0.1
        bounds[0]["max"][cls.XrotEyes, 0] = np.pi / 8 + 0.1
        return bounds
