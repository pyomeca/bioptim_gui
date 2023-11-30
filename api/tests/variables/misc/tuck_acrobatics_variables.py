import numpy as np

from tests.variables.misc.pike_acrobatics_variables import (
    PikeAcrobaticsVariables,
)


class TuckAcrobaticsVariables(PikeAcrobaticsVariables):
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

    legs_xdofs = [XrotUpperLegs, XrotLowerLegs]

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
            [15, 15, 15],
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

    @classmethod
    def get_q_bounds(cls, half_twists: list, prefer_left: bool) -> dict:
        nb_somersaults = len(half_twists)

        x_bounds = super().get_q_bounds(half_twists, prefer_left)

        for i in range(len(x_bounds)):
            x_bounds[i]["min"][cls.XrotLowerLegs, :] = -0.15
            x_bounds[i]["max"][cls.XrotLowerLegs, :] = 0.15

        current_phase = -1

        # twist start
        if half_twists[0] > 0:
            current_phase += 1

        last_have_twist = True
        next_have_twist = half_twists[1] > 0
        for i in range(1, nb_somersaults):
            is_last_somersault = i == nb_somersaults - 1
            # tucking
            if last_have_twist:
                current_phase += 1

                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 0] = -0.2
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 0] = 0.2
                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 1] = -0.2
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 1] = 2.4 + 0.2
                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 2] = 2.4 - 0.2
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 2] = 2.4 + 0.2

            # somersaulting in tuck
            if i == nb_somersaults - 1 or next_have_twist:
                current_phase += 1

                x_bounds[current_phase]["min"][cls.XrotLowerLegs, :] = 2.4 - 0.2
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, :] = 2.4 + 0.2

            # kick out
            if next_have_twist or is_last_somersault:
                current_phase += 1

                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 0] = 2.4 - 0.2 - 0.01
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 0] = 2.4 + 0.2 + 0.01
                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 1] = -0.2 - 0.01
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 1] = 2.4 + 0.2 + 0.01
                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 2] = -0.15
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 2] = 0.15

            # twisting
            if next_have_twist:
                current_phase += 1

                x_bounds[current_phase]["min"][cls.XrotLowerLegs, :] = -0.15
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, :] = 0.15

            last_have_twist = next_have_twist
            next_have_twist = is_last_somersault or half_twists[i + 1] > 0

        # decorative
        if half_twists[-1] == 0:
            current_phase += 1

        # landing
        current_phase += 1

        x_bounds[current_phase]["min"][cls.XrotLowerLegs, :] = -0.15
        x_bounds[current_phase]["max"][cls.XrotLowerLegs, :] = 0.15

        return x_bounds
