import numpy as np


class StraightAcrobaticsVariables:
    X = 0
    Y = 1
    Z = 2
    Xrot = 3
    Yrot = 4
    Zrot = 5
    ZrotRightUpperArm = 6
    YrotRightUpperArm = 7
    ZrotLeftUpperArm = 8
    YrotLeftUpperArm = 9

    nb_q, nb_qdot, nb_tau = 10, 10, 4
    tau_min, tau_max, tau_init = -500, 500, 0
    qdot_min, qdot_max = -10 * np.pi, 10 * np.pi

    arm_dofs = [
        ZrotRightUpperArm,
        YrotRightUpperArm,
        ZrotLeftUpperArm,
        YrotLeftUpperArm,
    ]

    shoulder_dofs = [
        ZrotRightUpperArm,
        YrotRightUpperArm,
        ZrotLeftUpperArm,
        YrotLeftUpperArm,
    ]

    elbow_dofs = []
    legs_xdofs = []

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
            [2.0, 2.0, 2.0],
            [3.0, 3.0, 3.0],
            [0.65, 0.65, 0.65],
            [0.05, 0.05, 0.05],
        ]
    )

    @classmethod
    def get_q_bounds(cls, half_twists: list, prefer_left: bool) -> dict:
        nb_somersaults = len(half_twists)
        is_forward = sum(half_twists) % 2 != 0
        x_bounds = [
            {
                "min": cls.q_min_bounds.copy(),
                "max": cls.q_max_bounds.copy(),
            }
            for _ in range(nb_somersaults + 1)  # + 1 for landing
        ]

        x_bounds[0]["min"][:, 0] = [0] * cls.nb_q
        x_bounds[0]["min"][: cls.Xrot, 0] = -0.001
        x_bounds[0]["min"][[cls.YrotRightUpperArm, cls.YrotLeftUpperArm], 0] = 2.9, -2.9

        x_bounds[0]["max"][:, 0] = [0] * cls.nb_q
        x_bounds[0]["max"][: cls.Xrot, 0] = 0.001
        x_bounds[0]["max"][[cls.YrotRightUpperArm, cls.YrotLeftUpperArm], 0] = 2.9, -2.9

        intermediate_min_bounds = cls.q_min_bounds.copy()[:, 0]
        intermediate_max_bounds = cls.q_max_bounds.copy()[:, 0]

        for phase in range(nb_somersaults):
            if phase != 0:
                # initial bounds, same as final bounds of previous phase
                x_bounds[phase]["min"][:, 0] = x_bounds[phase - 1]["min"][:, 2]
                x_bounds[phase]["max"][:, 0] = x_bounds[phase - 1]["max"][:, 2]

            # Intermediate bounds, same for every phase
            x_bounds[phase]["min"][:, 1] = intermediate_min_bounds
            x_bounds[phase]["max"][:, 1] = intermediate_max_bounds
            x_bounds[phase]["min"][:, 2] = intermediate_min_bounds
            x_bounds[phase]["max"][:, 2] = intermediate_max_bounds

            # somersaulting
            x_bounds[phase]["min"][cls.Xrot, 1] = 2 * np.pi * phase - 0.1
            x_bounds[phase]["max"][cls.Xrot, 1] = 2 * np.pi * (phase + 1) + 0.1
            x_bounds[phase]["min"][cls.Xrot, 2] = 2 * np.pi * (phase + 1) - 0.1
            x_bounds[phase]["max"][cls.Xrot, 2] = 2 * np.pi * (phase + 1) + 0.1

            # twisting
            x_bounds[phase]["min"][cls.Zrot, 1] = np.pi * sum(half_twists[:phase]) - np.pi / 4 - 0.2
            x_bounds[phase]["max"][cls.Zrot, 1] = np.pi * sum(half_twists[: phase + 1]) + np.pi / 4 + 0.2
            x_bounds[phase]["min"][cls.Zrot, 2] = np.pi * sum(half_twists[: phase + 1]) - np.pi / 4 - 0.2
            x_bounds[phase]["max"][cls.Zrot, 2] = np.pi * sum(half_twists[: phase + 1]) + np.pi / 4 + 0.2

        # bounds for last_somersault

        # keep 1/2 somersault before landing phase
        x_bounds[nb_somersaults - 1]["min"][cls.Xrot, 1] = 2 * np.pi * (nb_somersaults - 1) - 0.1
        x_bounds[nb_somersaults - 1]["max"][cls.Xrot, 1] = 2 * np.pi * nb_somersaults - np.pi / 2 + 0.1
        x_bounds[nb_somersaults - 1]["min"][cls.Xrot, 2] = 2 * np.pi * nb_somersaults - np.pi / 2 - 0.1
        x_bounds[nb_somersaults - 1]["max"][cls.Xrot, 2] = 2 * np.pi * nb_somersaults - np.pi / 2 + 0.1

        # twists must be done before landing
        x_bounds[nb_somersaults - 1]["min"][cls.Zrot, 2] = np.pi * sum(half_twists) - 0.1
        x_bounds[nb_somersaults - 1]["max"][cls.Zrot, 2] = np.pi * sum(half_twists) + 0.1

        # landing
        x_bounds[-1]["min"][:, 0] = x_bounds[-2]["min"][:, 2]
        x_bounds[-1]["max"][:, 0] = x_bounds[-2]["max"][:, 2]

        x_bounds[-1]["min"][:, 2] = np.zeros(cls.nb_q) - 0.1
        x_bounds[-1]["max"][:, 2] = np.zeros(cls.nb_q) + 0.1

        x_bounds[-1]["min"][[cls.X, cls.Y, cls.Z], 2] = [-0.01, -0.01, 0]
        x_bounds[-1]["max"][[cls.X, cls.Y, cls.Z], 2] = [0.01, 0.01, 0.01]

        # finish last half-somersault
        x_bounds[-1]["min"][cls.Xrot, 1] = 2 * np.pi * nb_somersaults - np.pi / 2 - 0.1
        x_bounds[-1]["max"][cls.Xrot, 1] = 2 * np.pi * nb_somersaults + 0.1
        x_bounds[-1]["min"][cls.Xrot, 2] = 2 * np.pi * nb_somersaults - 0.1
        x_bounds[-1]["max"][cls.Xrot, 2] = 2 * np.pi * nb_somersaults + 0.1

        # keep twists finished
        x_bounds[-1]["min"][cls.Zrot, :] = np.pi * sum(half_twists) - 0.1
        x_bounds[-1]["max"][cls.Zrot, :] = np.pi * sum(half_twists) + 0.1

        # tilt pi / 16
        x_bounds[-1]["min"][cls.Yrot, :] = -np.pi / 16
        x_bounds[-1]["max"][cls.Yrot, :] = np.pi / 16

        # arms
        x_bounds[-1]["min"][cls.YrotRightUpperArm, 0] = 0
        x_bounds[-1]["max"][cls.YrotRightUpperArm, 0] = np.pi / 8
        x_bounds[-1]["min"][cls.YrotRightUpperArm, 2] = 2.9 - 0.1
        x_bounds[-1]["max"][cls.YrotRightUpperArm, 2] = 2.9 + 0.1
        x_bounds[-1]["min"][cls.ZrotRightUpperArm, 2] = -0.1
        x_bounds[-1]["max"][cls.ZrotRightUpperArm, 2] = 0.1
        # Left arm
        x_bounds[-1]["min"][cls.YrotLeftUpperArm, 0] = -np.pi / 8
        x_bounds[-1]["max"][cls.YrotLeftUpperArm, 0] = 0
        x_bounds[-1]["min"][cls.YrotLeftUpperArm, 2] = -2.9 - 0.1
        x_bounds[-1]["max"][cls.YrotLeftUpperArm, 2] = -2.9 + 0.1
        x_bounds[-1]["min"][cls.ZrotLeftUpperArm, 2] = -0.1
        x_bounds[-1]["max"][cls.ZrotLeftUpperArm, 2] = 0.1

        if (not is_forward) or (not prefer_left):
            for i in range(len(x_bounds)):
                if not is_forward:
                    tmp = x_bounds[i]["min"][cls.Xrot].copy()
                    x_bounds[i]["min"][cls.Xrot] = -x_bounds[i]["max"][cls.Xrot]
                    x_bounds[i]["max"][cls.Xrot] = -tmp
                if not prefer_left:
                    tmp = x_bounds[i]["min"][cls.Zrot].copy()
                    x_bounds[i]["min"][cls.Zrot] = -x_bounds[i]["max"][cls.Zrot]
                    x_bounds[i]["max"][cls.Zrot] = -tmp

        return x_bounds

    @classmethod
    def get_q_init(cls, half_twists: list, prefer_left: bool = True) -> list:
        x_bounds = cls.get_q_bounds(half_twists, prefer_left)
        nb_phases = len(x_bounds)

        x_inits = np.zeros((nb_phases, 2, cls.nb_q))

        for phase in range(nb_phases):
            x_inits[phase, 0] = (x_bounds[phase]["min"][:, 0] + x_bounds[phase]["max"][:, 0]) / 2
            x_inits[phase, 1] = (x_bounds[phase]["min"][:, 2] + x_bounds[phase]["max"][:, 2]) / 2

        return x_inits

    @classmethod
    def get_qdot_bounds(cls, nb_phases: int, final_time: float, is_forward: bool) -> dict:
        vzinit = 9.81 / 2 * final_time  # vitesse initiale en z du CoM pour revenir a terre au temps final

        x_bounds = [
            {
                "min": np.zeros((cls.nb_qdot, 3)) + cls.qdot_min,
                "max": np.zeros((cls.nb_qdot, 3)) + cls.qdot_max,
            }
            for _ in range(nb_phases)
        ]

        # Initial bounds
        x_bounds[0]["min"][:, 0] = [0] * cls.nb_qdot
        x_bounds[0]["max"][:, 0] = [0] * cls.nb_qdot

        x_bounds[0]["min"][: cls.Z, 0] = -0.5
        x_bounds[0]["max"][: cls.Z, 0] = 0.5

        x_bounds[0]["min"][cls.Z, 0] = vzinit - 2
        x_bounds[0]["max"][cls.Z, 0] = vzinit + 2

        x_bounds[0]["min"][cls.Xrot, 0] = 0.5
        x_bounds[0]["max"][cls.Xrot, 0] = 20

        for phase in range(nb_phases):
            if phase != 0:
                # initial bounds, same as final bounds of previous phase
                x_bounds[phase]["min"][:, 0] = x_bounds[phase - 1]["min"][:, 2]
                x_bounds[phase]["max"][:, 0] = x_bounds[phase - 1]["max"][:, 2]

            x_bounds[phase]["min"][:, 1:] = -100
            x_bounds[phase]["max"][:, 1:] = 100

            x_bounds[phase]["min"][: cls.Z, 1:] = -10
            x_bounds[phase]["max"][: cls.Z, 1:] = 10

            x_bounds[phase]["min"][cls.Xrot, 1:] = 0.5
            x_bounds[phase]["max"][cls.Xrot, 1:] = 20

        if not is_forward:
            for i in range(len(x_bounds)):
                tmp = x_bounds[i]["min"][cls.Xrot].copy()
                x_bounds[i]["min"][cls.Xrot] = -x_bounds[i]["max"][cls.Xrot]
                x_bounds[i]["max"][cls.Xrot] = -tmp

        return x_bounds

    @classmethod
    def get_qdot_init(cls) -> list:
        return [0.0] * cls.nb_qdot

    @classmethod
    def get_tau_bounds(cls) -> dict:
        return {
            "min": [cls.tau_min] * cls.nb_tau,
            "max": [cls.tau_max] * cls.nb_tau,
        }

    @classmethod
    def get_tau_init(cls) -> list:
        return [cls.tau_init] * cls.nb_tau
