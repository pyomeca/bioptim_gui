import numpy as np

from bioptim_gui_api.variables.misc.pike_with_visual_acrobatics_variables import PikeAcrobaticsWithVisualVariables


class PikeAcrobaticsWithVisualVariablesWithSpine(PikeAcrobaticsWithVisualVariables):
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
    ZrotHead = 18
    XrotHead = 19
    ZrotEyes = 20
    XrotEyes = 21
    ZrotRightUpperArm = 22
    YrotRightUpperArm = 23
    ZrotRightLowerArm = 24
    XrotRightLowerArm = 25
    ZrotLeftUpperArm = 26
    YrotLeftUpperArm = 27
    ZrotLeftLowerArm = 28
    XrotLeftLowerArm = 29
    XrotUpperLegs = 30
    YrotUpperLegs = 31

    nb_q, nb_qdot, nb_tau = 32, 32, 26

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
