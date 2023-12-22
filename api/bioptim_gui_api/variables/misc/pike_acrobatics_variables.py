import numpy as np

from bioptim_gui_api.utils.format_utils import invert_min_max
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)
from bioptim_gui_api.variables.misc.variables_utils import define_loose_bounds, LooseValue


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

    legs_xdofs = [XrotUpperLegs]

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
            [-1.8] * 3,
            [-2.65] * 3,
            [-2.0] * 3,
            [-3.0] * 3,
            [-1.1] * 3,
            [-2.65] * 3,
            [-2.7] * 3,
            [-0.1] * 3,
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
            [1.1] * 3,
            [0.0] * 3,
            [0.65] * 3,
            [0.05] * 3,
            [1.8] * 3,
            [0.0] * 3,
            [0.3] * 3,
            [0.1] * 3,
        ]
    )

    @classmethod
    def _fill_init_phase(cls, x_bounds: np.ndarray, half_twists: list) -> None:
        x_bounds[0]["min"][:, 0] = [0] * cls.nb_q
        x_bounds[0]["max"][:, 0] = [0] * cls.nb_q

        x_bounds[0]["min"][: cls.Xrot, 0] = -0.001
        x_bounds[0]["max"][: cls.Xrot, 0] = 0.001
        # arm position up
        define_loose_bounds(x_bounds[0], cls.YrotRightUpperArm, 0, LooseValue(2.9, 0.0))
        define_loose_bounds(x_bounds[0], cls.YrotLeftUpperArm, 0, LooseValue(-2.9, 0.0))

        x_bounds[0]["min"][:, 1] = cls.q_min_bounds.copy()[:, 0]
        x_bounds[0]["max"][:, 1] = cls.q_max_bounds.copy()[:, 0]

        # somersaulting
        x_bounds[0]["min"][cls.Xrot, 1] = -0.1
        x_bounds[0]["max"][cls.Xrot, 1] = 2 * np.pi + 0.1

        x_bounds[0]["min"][cls.Xrot, 2] = np.pi / 2 - 0.1
        x_bounds[0]["max"][cls.Xrot, 2] = 2 * np.pi + 0.1

        # twisting
        x_bounds[0]["min"][cls.Zrot, 1] = -0.2
        x_bounds[0]["max"][cls.Zrot, 1] = np.pi * half_twists[0] + 0.2

        x_bounds[0]["min"][cls.Zrot, 2] = np.pi * half_twists[0] - 0.2 - np.pi / 4
        x_bounds[0]["max"][cls.Zrot, 2] = np.pi * half_twists[0] + 0.2

    @classmethod
    def _fill_position_phase(cls, x_bounds: list, i: int, half_twists: list) -> None:
        # acrobatics starts with pike
        if len(x_bounds) == 1:
            x_bounds[0]["min"][:, 0] = [0] * cls.nb_q
            x_bounds[0]["max"][:, 0] = [0] * cls.nb_q

            x_bounds[0]["min"][: cls.Xrot, 0] = -0.001
            x_bounds[0]["max"][: cls.Xrot, 0] = 0.001
            # arm position up
            define_loose_bounds(x_bounds[0], cls.YrotRightUpperArm, 0, LooseValue(2.9, 0.0))
            define_loose_bounds(x_bounds[0], cls.YrotLeftUpperArm, 0, LooseValue(-2.9, 0.0))

            x_bounds[0]["min"][:, 1] = cls.q_min_bounds.copy()[:, 0]
            x_bounds[0]["max"][:, 1] = cls.q_max_bounds.copy()[:, 0]

            # somersaulting
            x_bounds[0]["min"][cls.Xrot, 1] = -0.1
            x_bounds[0]["max"][cls.Xrot, 1] = 3 / 4 * np.pi

            x_bounds[0]["min"][cls.Xrot, 2] = np.pi / 4 - 0.1
            x_bounds[0]["max"][cls.Xrot, 2] = 3 / 4 * np.pi

            # twisting
            define_loose_bounds(x_bounds[0], cls.Zrot, 1, LooseValue(0.0, 0.2))
            define_loose_bounds(x_bounds[0], cls.Zrot, 2, LooseValue(0.0, 0.2))

        else:
            # initial bounds, same as final bounds of previous phase
            for b in 0, 1, 2:
                x_bounds[-1]["min"][:, b] = x_bounds[-2]["min"][:, 2]
                x_bounds[-1]["max"][:, b] = x_bounds[-2]["max"][:, 2]

            half_twists_till_now = sum(half_twists[:i])
            if half_twists_till_now != 0:
                define_loose_bounds(x_bounds[-1], cls.Zrot, 2, LooseValue(np.pi * half_twists_till_now, 0.2))

            if sum(half_twists[: i + 1]) == sum(half_twists):
                x_bounds[-1]["min"][cls.Zrot, 1] = np.pi * half_twists_till_now - 0.2 - np.pi / 4
                x_bounds[-1]["max"][cls.Zrot, 1] = np.pi * half_twists_till_now + 0.2

            # legs
            define_loose_bounds(x_bounds[-1], cls.XrotUpperLegs, 0, LooseValue(0.0, 0.2))

        x_bounds[-1]["min"][cls.XrotUpperLegs, 1] = -2.4 - 0.2
        x_bounds[-1]["max"][cls.XrotUpperLegs, 1] = 0.2
        define_loose_bounds(x_bounds[-1], cls.XrotUpperLegs, 2, LooseValue(-2.4, 0.2))
        # Hips sides
        define_loose_bounds(x_bounds[-1], cls.YrotUpperLegs, 2, LooseValue(0.0, 0.1))

    @classmethod
    def _fill_somersault_phase(cls, x_bounds: list, phase: int, half_twists: list) -> None:
        nb_somersaults = len(half_twists)
        for b in 0, 1, 2:
            x_bounds[-1]["min"][:, b] = x_bounds[-2]["min"][:, 2]
            x_bounds[-1]["max"][:, b] = x_bounds[-2]["max"][:, 2]

        # somersaulting in pike, for all no-twist somersaults, starting from last pike
        x_bounds[-1]["max"][cls.Xrot, 1:] = min(
            2 * np.pi * (phase + 1) + 0.2,
            2 * np.pi * nb_somersaults - np.pi + 0.2,
        )
        x_bounds[-1]["min"][cls.Xrot, 2] = 2 * np.pi * phase - 0.2

        # tilt pi / 8
        define_loose_bounds(x_bounds[-1], cls.Yrot, None, LooseValue(0.0, np.pi / 8))

        # twisting
        # should be good with the end of twist from previous phase

        # rot legs, hips
        define_loose_bounds(x_bounds[-1], cls.XrotUpperLegs, None, LooseValue(-2.4, 0.2))
        # Hips sides
        define_loose_bounds(x_bounds[-1], cls.YrotUpperLegs, 2, LooseValue(0.0, 0.1))

    @classmethod
    def _fill_kickout_phase(cls, x_bounds: list, i: int, half_twists: list) -> None:
        nb_somersaults = len(half_twists)
        for b in 0, 1, 2:
            x_bounds[-1]["min"][:, b] = x_bounds[-2]["min"][:, 2]
            x_bounds[-1]["max"][:, b] = x_bounds[-2]["max"][:, 2]

        # somersaulting
        x_bounds[-1]["max"][cls.Xrot, 1:] = min(
            2 * np.pi * (i + 1) + 0.2,
            2 * np.pi * nb_somersaults - np.pi + 0.2,
        )

        # tilt pi / 4
        define_loose_bounds(x_bounds[-1], cls.Yrot, None, LooseValue(0.0, np.pi / 4))

        # twisting
        x_bounds[-1]["min"][cls.Zrot, 1:] = np.pi * sum(half_twists[:i]) - 0.2
        x_bounds[-1]["max"][cls.Zrot, 1:] = (
            np.pi * sum(half_twists[: i + 1]) + 0.2 - (np.pi * half_twists[i] / 2 if half_twists[i] != 0 else 0)
        )

        # Hips flexion
        define_loose_bounds(x_bounds[-1], cls.XrotUpperLegs, 0, LooseValue(-2.4, 0.2 + 0.01))
        x_bounds[-1]["min"][cls.XrotUpperLegs, 1] = -2.4 - 0.2 - 0.01
        x_bounds[-1]["max"][cls.XrotUpperLegs, 1] = 0.35
        define_loose_bounds(x_bounds[-1], cls.XrotUpperLegs, 2, LooseValue(0.0, 0.35))

    @classmethod
    def _fill_twist_phase(cls, x_bounds: list, i: int, half_twists: list, is_last_somersault: bool) -> None:
        nb_somersaults = len(half_twists)
        for b in 0, 1, 2:
            x_bounds[-1]["min"][:, b] = x_bounds[-2]["min"][:, 2]
            x_bounds[-1]["max"][:, b] = x_bounds[-2]["max"][:, 2]

        if is_last_somersault:
            # tilt pi /8
            define_loose_bounds(x_bounds[-1], cls.Yrot, None, LooseValue(0.0, np.pi / 8))

            # somersault 1/4 left at then end
            x_bounds[-1]["max"][cls.Xrot, 1] = 2 * np.pi * nb_somersaults - np.pi / 2 + 0.2
            define_loose_bounds(x_bounds[-1], cls.Xrot, 2, LooseValue(2 * np.pi * nb_somersaults - np.pi / 2, 0.2))

            # finish twist
            x_bounds[-1]["min"][cls.Zrot, 1] = sum(half_twists[:-1]) * np.pi - 0.2
            x_bounds[-1]["max"][cls.Zrot, 1] = sum(half_twists) * np.pi + 0.2
            define_loose_bounds(x_bounds[-1], cls.Zrot, 2, LooseValue(sum(half_twists) * np.pi, 0.2))

            # Right arm
            x_bounds[-1]["min"][cls.YrotRightUpperArm, 2] = 0
            x_bounds[-1]["max"][cls.YrotRightUpperArm, 2] = np.pi / 8
            # Left arm
            x_bounds[-1]["min"][cls.YrotLeftUpperArm, 2] = -np.pi / 8
            x_bounds[-1]["max"][cls.YrotLeftUpperArm, 2] = 0

            # Right elbow
            x_bounds[-1]["min"][cls.ZrotRightLowerArm : cls.XrotRightLowerArm + 1, 2] = -0.1
            x_bounds[-1]["max"][cls.ZrotRightLowerArm : cls.XrotRightLowerArm + 1, 2] = 0.1
            # Left elbow
            x_bounds[-1]["min"][cls.ZrotLeftLowerArm : cls.XrotLeftLowerArm + 1, 2] = -0.1
            x_bounds[-1]["max"][cls.ZrotLeftLowerArm : cls.XrotLeftLowerArm + 1, 2] = 0.1

        else:
            # somersaulting
            x_bounds[-1]["max"][cls.Xrot, 1] = 2 * np.pi * (i + 1) + 0.2

            x_bounds[-1]["min"][cls.Xrot, 2] = 2 * np.pi * i - 0.2
            x_bounds[-1]["max"][cls.Xrot, 2] = 2 * np.pi * (i + 1) + 0.2

            # tilt pi / 4
            define_loose_bounds(x_bounds[-1], cls.Yrot, 2, LooseValue(0.0, np.pi / 4))

            # twisting
            half_twist_till_now = sum(half_twists[:i])
            if half_twist_till_now != 0:
                x_bounds[-1]["min"][cls.Zrot, 1] = np.pi * half_twist_till_now - 0.2
                x_bounds[-1]["max"][cls.Zrot, 1] = np.pi * sum(half_twists[: i + 1]) + 0.2
                x_bounds[-1]["min"][cls.Zrot, 2] = np.pi * sum(half_twists[: i + 1]) - 0.2 - np.pi / 4
                x_bounds[-1]["max"][cls.Zrot, 2] = np.pi * sum(half_twists[: i + 1]) + 0.2
            else:
                x_bounds[-1]["min"][cls.Zrot, 1] = np.pi * half_twist_till_now - 0.2
                x_bounds[-1]["max"][cls.Zrot, 1] = np.pi * sum(half_twists[: i + 1]) + 0.2
                x_bounds[-1]["min"][cls.Zrot, 2] = np.pi * sum(half_twists[: i + 1]) - 0.2 - np.pi / 4
                x_bounds[-1]["max"][cls.Zrot, 2] = np.pi * sum(half_twists[: i + 1]) + 0.2

        # Hips flexion
        define_loose_bounds(x_bounds[-1], cls.XrotUpperLegs, None, LooseValue(0.0, 0.35))

    @classmethod
    def _fill_waiting_phase(cls, x_bounds: list, nb_somersaults: int) -> None:
        for b in 0, 1, 2:
            x_bounds[-1]["min"][:, b] = x_bounds[-2]["min"][:, 2]
            x_bounds[-1]["max"][:, b] = x_bounds[-2]["max"][:, 2]

        # left arm
        x_bounds[-1]["min"][cls.YrotLeftUpperArm, 1] = -np.pi / 4
        define_loose_bounds(x_bounds[-1], cls.ZrotLeftUpperArm, 1, LooseValue(0.0, np.pi / 4))

        # right arm
        x_bounds[-1]["max"][cls.YrotRightUpperArm, 1] = np.pi / 4
        define_loose_bounds(x_bounds[-1], cls.ZrotRightUpperArm, 1, LooseValue(0.0, np.pi / 4))

        # somersaulting
        x_bounds[-1]["max"][cls.Xrot, 1] = 2 * np.pi * nb_somersaults - np.pi / 2 + 0.2
        define_loose_bounds(x_bounds[-1], cls.Xrot, 2, LooseValue(2 * np.pi * nb_somersaults - np.pi / 2, 0.2))

    @classmethod
    def _fill_landing_phase(cls, x_bounds, half_twists: list) -> dict:
        nb_somersaults = len(half_twists)
        x_bounds[-1]["min"][:, 0] = x_bounds[-2]["min"][:, 2]
        x_bounds[-1]["max"][:, 0] = x_bounds[-2]["max"][:, 2]

        super()._fill_landing_phase(x_bounds, half_twists)

        # avoid too forward on somersault caused by hip
        x_bounds[-1]["min"][cls.Xrot, 2] = nb_somersaults * np.pi * 2 - 0.55
        x_bounds[-1]["max"][cls.Xrot, 2] = nb_somersaults * np.pi * 2 - 0.45

        # Right elbow
        x_bounds[-1]["min"][cls.ZrotRightLowerArm : cls.XrotRightLowerArm + 1, 2] = -0.1
        x_bounds[-1]["max"][cls.ZrotRightLowerArm : cls.XrotRightLowerArm + 1, 2] = 0.1
        # Left elbow
        x_bounds[-1]["min"][cls.ZrotLeftLowerArm : cls.XrotLeftLowerArm + 1, 2] = -0.1
        x_bounds[-1]["max"][cls.ZrotLeftLowerArm : cls.XrotLeftLowerArm + 1, 2] = 0.1

        # Hips flexion
        x_bounds[-1]["min"][cls.XrotUpperLegs, :] = -0.60
        x_bounds[-1]["max"][cls.XrotUpperLegs, :] = 0.35
        x_bounds[-1]["min"][cls.XrotUpperLegs, 0] = 0
        x_bounds[-1]["max"][cls.XrotUpperLegs, 0] = 0.35
        x_bounds[-1]["min"][cls.XrotUpperLegs, 2] = -0.55
        x_bounds[-1]["max"][cls.XrotUpperLegs, 2] = -0.45

        # Hips sides
        define_loose_bounds(x_bounds[-1], cls.YrotUpperLegs, 2, LooseValue(0.0, 0.1))

    @classmethod
    def get_q_bounds(cls, half_twists: list, prefer_left: bool) -> dict:
        nb_somersaults = len(half_twists)
        is_forward = sum(half_twists) % 2 != 0
        x_bounds = []

        def add_phase_bounds():
            x_bounds.append(
                {
                    "min": cls.q_min_bounds.copy(),
                    "max": cls.q_max_bounds.copy(),
                }
            )

        # twist start
        if half_twists[0] > 0:
            add_phase_bounds()
            cls._fill_init_phase(x_bounds, half_twists)

        last_have_twist = True
        next_have_twist = half_twists[1] > 0
        for i in range(1, nb_somersaults):
            is_last_somersault = i == nb_somersaults - 1
            # piking
            if last_have_twist:
                add_phase_bounds()
                cls._fill_position_phase(x_bounds, i, half_twists)

            if is_last_somersault or next_have_twist:
                # somersaulting in pike
                add_phase_bounds()
                cls._fill_somersault_phase(x_bounds, i, half_twists)

                # kick out
                add_phase_bounds()
                cls._fill_kickout_phase(x_bounds, i, half_twists)

            # twisting
            if next_have_twist:
                add_phase_bounds()
                cls._fill_twist_phase(x_bounds, i, half_twists, is_last_somersault)

            last_have_twist = next_have_twist
            next_have_twist = is_last_somersault or half_twists[i + 1] > 0

        # waiting phase
        if half_twists[-1] == 0:
            add_phase_bounds()
            cls._fill_waiting_phase(x_bounds, nb_somersaults)

        # landing
        add_phase_bounds()
        cls._fill_landing_phase(x_bounds, half_twists)

        if not is_forward:
            invert_min_max(x_bounds, cls.Xrot)
        if not prefer_left:
            invert_min_max(x_bounds, cls.Zrot)

        return x_bounds
