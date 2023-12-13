import numpy as np

from bioptim_gui_api.variables.misc.straight_acrobatics_variables import StraightAcrobaticsVariables


class StraightAcrobaticsVariablesWithSpine(StraightAcrobaticsVariables):
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
    ZrotLeftUpperArm = 20
    YrotLeftUpperArm = 21

    nb_q, nb_qdot, nb_tau = 22, 22, 16

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
            [-0.65, -0.65, -0.65],
            [-0.05, -0.05, -0.05],
            [-2.0, -2.0, -2.0],
            [-3.0, -3.0, -3.0],
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
            [0.65, 0.65, 0.65],
            [0.05, 0.05, 0.05],
        ]
    )
