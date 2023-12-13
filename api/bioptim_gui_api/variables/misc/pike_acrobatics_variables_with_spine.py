import numpy as np

from bioptim_gui_api.variables.misc.pike_acrobatics_variables import PikeAcrobaticsVariables


class PikeAcrobaticsVariablesWithSpine(PikeAcrobaticsVariables):
    X = 0
    Y = 1
    Z = 2
    Xrot = 3
    Yrot = 4
    Zrot = 5
    XrotStomach = 6
    YrotStomach = 7
    ZrotStomach = 8
    XrotRib = 9
    YrotRib = 10
    ZrotRib = 11
    XrotNipple = 12
    YrotNipple = 13
    ZrotNipple = 14
    XrotShoulder = 15
    YrotShoulder = 16
    ZrotShoulder = 17
    ZrotRightUpperArm = 18
    YrotRightUpperArm = 19
    ZrotRightLowerArm = 20
    XrotRightLowerArm = 21
    ZrotLeftUpperArm = 22
    YrotLeftUpperArm = 23
    ZrotLeftLowerArm = 24
    XrotLeftLowerArm = 25
    XrotUpperLegs = 26
    YrotUpperLegs = 27

    nb_q, nb_qdot, nb_tau = 28, 28, 22

    q_min_bounds = np.array(
        [
            [-1, -1, -1],
            [-1, -1, -1],
            [-0.1, -0.1, -0.1],
            [0, 0, 0],
            [-np.pi / 4, -np.pi / 4, -np.pi / 4],
            [0, 0, 0],
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
            [-np.pi / 12] * 3,
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
            [15, 15, 15],
            [0, 0, 0],
            [np.pi / 4, np.pi / 4, np.pi / 4],
            [0, 0, 0],
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
            [np.pi / 12] * 3,
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
