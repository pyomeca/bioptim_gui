import numpy as np

from bioptim_gui_api.variables.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)


class TuckAcrobaticsVariables(StraightAcrobaticsVariables):
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
    XrotLowerLegs = 16

    nb_q, nb_qdot, nb_tau = 17, 17, 11

    arm_dofs = [
        ZrotRightUpperArm,
        YrotRightUpperArm,
        ZrotRightLowerArm,
        XrotRightLowerArm,
        ZrotLeftUpperArm,
        YrotLeftUpperArm,
        ZrotLeftLowerArm,
        XrotLeftLowerArm,
    ]
    shoulder_dofs = [
        ZrotRightUpperArm,
        YrotRightUpperArm,
        ZrotLeftUpperArm,
        YrotLeftUpperArm,
    ]
    elbow_dofs = [
        ZrotRightLowerArm,
        XrotRightLowerArm,
        ZrotLeftLowerArm,
        XrotLeftLowerArm,
    ]

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
            [-np.pi, -np.pi, -np.pi],
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
            [np.pi, np.pi, np.pi],
        ]
    )
