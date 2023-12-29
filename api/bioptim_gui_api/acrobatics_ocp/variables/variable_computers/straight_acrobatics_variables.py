import numpy as np

from bioptim_gui_api.acrobatics_ocp.variables.utils import maximum_fig_arms_angle
from bioptim_gui_api.utils.format_utils import invert_min_max
from bioptim_gui_api.variables.misc.variables_utils import define_loose_bounds, LooseValue


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
            [-1] * 3,
            [-1] * 3,
            [-0.1] * 3,
            [0] * 3,
            [-np.pi / 4] * 3,
            [0] * 3,
            [-0.65] * 3,
            [-0.05] * 3,
            [-2.0] * 3,
            [-3.0] * 3,
        ]
    )

    q_max_bounds = np.array(
        [
            [1] * 3,
            [1] * 3,
            [15] * 3,
            [0] * 3,
            [np.pi / 4] * 3,
            [0] * 3,
            [2.0] * 3,
            [3.0] * 3,
            [0.65] * 3,
            [0.05] * 3,
        ]
    )

    @classmethod
    def _fill_init_phase(cls, x_bounds: np.ndarray) -> None:
        x_bounds[0]["min"][:, 0] = [0] * cls.nb_q
        x_bounds[0]["min"][: cls.Xrot, 0] = -0.001
        x_bounds[0]["min"][[cls.YrotRightUpperArm, cls.YrotLeftUpperArm], 0] = 2.9, -2.9

        x_bounds[0]["max"][:, 0] = [0] * cls.nb_q
        x_bounds[0]["max"][: cls.Xrot, 0] = 0.001
        x_bounds[0]["max"][[cls.YrotRightUpperArm, cls.YrotLeftUpperArm], 0] = 2.9, -2.9

    @classmethod
    def _fill_somersault_phase(cls, x_bounds: np.ndarray, phase: int, half_twists: list) -> None:
        nb_somersaults = len(half_twists)

        if phase != 0:
            # initial bounds, same as final bounds of previous phase
            x_bounds[phase]["min"][:, 0] = x_bounds[phase - 1]["min"][:, 2]
            x_bounds[phase]["max"][:, 0] = x_bounds[phase - 1]["max"][:, 2]

        intermediate_min_bounds = cls.q_min_bounds.copy()[:, 0]
        intermediate_max_bounds = cls.q_max_bounds.copy()[:, 0]

        # Intermediate bounds, same for every phase
        x_bounds[phase]["min"][:, 1] = intermediate_min_bounds
        x_bounds[phase]["max"][:, 1] = intermediate_max_bounds
        x_bounds[phase]["min"][:, 2] = intermediate_min_bounds
        x_bounds[phase]["max"][:, 2] = intermediate_max_bounds

        # somersaulting
        x_bounds[phase]["min"][cls.Xrot, 1] = 2 * np.pi * phase - 0.1
        x_bounds[phase]["max"][cls.Xrot, 1] = 2 * np.pi * (phase + 1) + 0.1
        define_loose_bounds(x_bounds[phase], cls.Xrot, 2, LooseValue(2 * np.pi * (phase + 1), 0.1))

        # twisting
        x_bounds[phase]["min"][cls.Zrot, 1] = np.pi * sum(half_twists[:phase]) - np.pi / 4 - 0.2
        x_bounds[phase]["max"][cls.Zrot, 1] = np.pi * sum(half_twists[: phase + 1]) + np.pi / 4 + 0.2
        define_loose_bounds(
            x_bounds[phase], cls.Zrot, 2, LooseValue(np.pi * sum(half_twists[: phase + 1]), np.pi / 4 + 0.2)
        )

        if phase == nb_somersaults - 1:
            # bounds for last_somersault
            # keep 1/2 somersault before landing phase
            x_bounds[nb_somersaults - 1]["min"][cls.Xrot, 1] = 2 * np.pi * (nb_somersaults - 1) - 0.1
            x_bounds[nb_somersaults - 1]["max"][cls.Xrot, 1] = 2 * np.pi * nb_somersaults - np.pi / 2 + 0.1
            define_loose_bounds(
                x_bounds[nb_somersaults - 1], cls.Xrot, 2, LooseValue(2 * np.pi * nb_somersaults - np.pi / 2, 0.1)
            )

            # twists must be done before landing
            define_loose_bounds(x_bounds[nb_somersaults - 1], cls.Zrot, 2, LooseValue(np.pi * sum(half_twists), 0.1))

    @classmethod
    def _fill_landing_phase(cls, x_bounds, half_twists: list) -> dict:
        nb_somersaults = len(half_twists)

        # Pelvis translations
        x_bounds[-1]["min"][[cls.X, cls.Y, cls.Z], 2] = [-0.01, -0.01, 0]
        x_bounds[-1]["max"][[cls.X, cls.Y, cls.Z], 2] = [0.01, 0.01, 0.01]

        # Somersault
        x_bounds[-1]["min"][cls.Xrot, 1] = 2 * np.pi * nb_somersaults - np.pi / 2 - 0.1
        x_bounds[-1]["max"][cls.Xrot, 1] = 2 * np.pi * nb_somersaults + 0.1
        define_loose_bounds(x_bounds[-1], cls.Xrot, 2, LooseValue(2 * np.pi * nb_somersaults, 0.1))

        # Tilt
        define_loose_bounds(x_bounds[-1], cls.Yrot, None, LooseValue(0.0, np.pi / 16))
        # Twist
        define_loose_bounds(x_bounds[-1], cls.Zrot, None, LooseValue(np.pi * sum(half_twists), 0.1))

        # FIG Code of Points 14.5, arms to stop twisting rotation
        max_angle = maximum_fig_arms_angle(half_twists)
        # Right arm
        x_bounds[-1]["min"][cls.YrotRightUpperArm, 0] = 0
        x_bounds[-1]["max"][cls.YrotRightUpperArm, 0] = max_angle
        define_loose_bounds(x_bounds[-1], cls.YrotRightUpperArm, 2, LooseValue(2.9, 0.1))
        define_loose_bounds(x_bounds[-1], cls.ZrotRightUpperArm, 2, LooseValue(0.0, 0.1))
        # Left arm
        x_bounds[-1]["min"][cls.YrotLeftUpperArm, 0] = -max_angle
        x_bounds[-1]["max"][cls.YrotLeftUpperArm, 0] = 0
        define_loose_bounds(x_bounds[-1], cls.YrotLeftUpperArm, 2, LooseValue(-2.9, 0.1))
        define_loose_bounds(x_bounds[-1], cls.ZrotLeftUpperArm, 2, LooseValue(0.0, 0.1))

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

        cls._fill_init_phase(x_bounds)

        for phase in range(nb_somersaults):
            cls._fill_somersault_phase(x_bounds, phase, half_twists)

        cls._fill_landing_phase(x_bounds, half_twists)

        if not is_forward:
            invert_min_max(x_bounds, cls.Xrot)
        if not prefer_left:
            invert_min_max(x_bounds, cls.Zrot)

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
    def _fill_qdot_initial(cls, x_bounds: np.ndarray, final_time: float) -> None:
        vzinit = 9.81 / 2 * final_time  # vitesse initiale en z du CoM pour revenir a terre au temps final

        x_bounds[0]["min"][:, 0] = [0] * cls.nb_qdot
        x_bounds[0]["max"][:, 0] = [0] * cls.nb_qdot

        x_bounds[0]["min"][: cls.Z, 0] = -0.5
        x_bounds[0]["max"][: cls.Z, 0] = 0.5

        x_bounds[0]["min"][cls.Z, 0] = vzinit - 2
        x_bounds[0]["max"][cls.Z, 0] = vzinit + 2

        x_bounds[0]["min"][cls.Xrot, 0] = 0.5
        x_bounds[0]["max"][cls.Xrot, 0] = 200.0

    @classmethod
    def _fill_qdot_intermediary(cls, x_bounds: np.ndarray) -> None:
        nb_phases = len(x_bounds)
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
            x_bounds[phase]["max"][cls.Xrot, 1:] = 200.0

    @classmethod
    def get_qdot_bounds(cls, nb_phases: int, final_time: float, is_forward: bool) -> dict:
        x_bounds = [
            {
                "min": np.zeros((cls.nb_qdot, 3)) + cls.qdot_min,
                "max": np.zeros((cls.nb_qdot, 3)) + cls.qdot_max,
            }
            for _ in range(nb_phases)
        ]

        # Initial bounds
        cls._fill_qdot_initial(x_bounds, final_time)

        cls._fill_qdot_intermediary(x_bounds)

        if not is_forward:
            invert_min_max(x_bounds, cls.Xrot)

        return x_bounds

    @classmethod
    def get_qdot_init(cls, nb_somersaults: int, final_time: float) -> list:
        vzinit = 9.81 / 2 * final_time

        qdot_init = [0.0] * cls.nb_qdot
        qdot_init[cls.Xrot] = 2 * np.pi * nb_somersaults
        qdot_init[cls.Z] = vzinit

        return qdot_init

    @classmethod
    def get_tau_bounds(cls) -> dict:
        return {
            "min": [cls.tau_min] * cls.nb_tau,
            "max": [cls.tau_max] * cls.nb_tau,
        }

    @classmethod
    def get_tau_init(cls) -> list:
        return [cls.tau_init] * cls.nb_tau
