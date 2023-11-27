import numpy as np

from bioptim_gui_api.variables.misc.straight_acrobatics_variables import (
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

    @classmethod
    def get_q_bounds(cls, half_twists: list, prefer_left: bool) -> dict:
        nb_somersaults = len(half_twists)
        is_forward = sum(half_twists) % 2 != 0
        intermediate_min_bounds = cls.q_min_bounds.copy()[:, 0]
        intermediate_max_bounds = cls.q_max_bounds.copy()[:, 0]
        x_bounds = []
        current_phase = -1

        # twist start
        if half_twists[0] > 0:
            x_bounds.append(
                {
                    "min": cls.q_min_bounds.copy(),
                    "max": cls.q_max_bounds.copy(),
                }
            )
            current_phase += 1

            x_bounds[0]["min"][:, 0] = [0] * cls.nb_q
            x_bounds[0]["min"][: cls.Xrot, 0] = -0.001
            # arm position up
            x_bounds[0]["min"][cls.YrotRightUpperArm, 0] = 2.9
            x_bounds[0]["min"][cls.YrotLeftUpperArm, 0] = -2.9

            x_bounds[0]["max"][:, 0] = -x_bounds[0]["min"][:, 0]
            x_bounds[0]["max"][cls.YrotRightUpperArm, 0] = 2.9
            x_bounds[0]["max"][cls.YrotLeftUpperArm, 0] = -2.9

            x_bounds[0]["min"][:, 1] = intermediate_min_bounds
            x_bounds[0]["max"][:, 1] = intermediate_max_bounds

            # somersaulting
            x_bounds[0]["min"][cls.Xrot, 1] = -0.1 if is_forward else -2 * np.pi + 0.1
            x_bounds[0]["max"][cls.Xrot, 1] = 2 * np.pi + 0.1 if is_forward else 0.1

            x_bounds[0]["min"][cls.Xrot, 2] = (
                np.pi / 2 - 0.1 if is_forward else -2 * np.pi + 0.1
            )
            x_bounds[0]["max"][cls.Xrot, 2] = (
                2 * np.pi + 0.1 if is_forward else -np.pi / 2 + 0.1
            )

            # twisting
            x_bounds[0]["min"][cls.Zrot, 1] = (
                -0.2 if prefer_left else -np.pi * half_twists[0] - 0.2
            )

            x_bounds[0]["max"][cls.Zrot, 1] = (
                np.pi * half_twists[0] + 0.2 if prefer_left else 0.2
            )

            x_bounds[0]["min"][cls.Zrot, 2] = (
                np.pi * half_twists[0] - 0.2 - np.pi / 4
                if prefer_left
                else -np.pi * half_twists[0] - 0.2
            )

            x_bounds[0]["max"][cls.Zrot, 2] = (
                np.pi * half_twists[0] + 0.2
                if prefer_left
                else -np.pi * half_twists[0] + 0.2 + np.pi / 4
            )

        last_have_twist = True
        next_have_twist = half_twists[1] > 0
        somersault_tuck_start = None
        for i in range(1, nb_somersaults):
            is_last_somersault = i == nb_somersaults - 1
            # tucking
            if last_have_twist:
                x_bounds.append(
                    {
                        "min": cls.q_min_bounds.copy(),
                        "max": cls.q_max_bounds.copy(),
                    }
                )
                somersault_tuck_start = i
                current_phase += 1

                # acrobatics starts with tuck
                if len(x_bounds) == 1:
                    x_bounds[0]["min"][:, 0] = [0] * cls.nb_q
                    x_bounds[0]["min"][: cls.Xrot, 0] = -0.001

                    # arm position up
                    x_bounds[0]["min"][cls.YrotRightUpperArm, 0] = 2.9
                    x_bounds[0]["min"][cls.YrotLeftUpperArm, 0] = -2.9

                    x_bounds[0]["max"][:, 0] = -x_bounds[0]["min"][:, 0]
                    x_bounds[0]["max"][cls.YrotRightUpperArm, 0] = 2.9
                    x_bounds[0]["max"][cls.YrotLeftUpperArm, 0] = -2.9

                    x_bounds[0]["min"][:, 1] = intermediate_min_bounds
                    x_bounds[0]["max"][:, 1] = intermediate_max_bounds

                    # somersaulting
                    x_bounds[0]["min"][cls.Xrot, 1] = (
                        0 if is_forward else -2 * np.pi + 0.1
                    )
                    x_bounds[0]["max"][cls.Xrot, 1] = (
                        2 * np.pi + 0.1 if is_forward else 0
                    )

                    x_bounds[0]["min"][cls.Xrot, 2] = (
                        np.pi / 2 - 0.1 if is_forward else -2 * np.pi + 0.1
                    )
                    x_bounds[0]["max"][cls.Xrot, 2] = (
                        2 * np.pi + 0.1 if is_forward else -np.pi / 2 + 0.1
                    )

                    # twisting
                    x_bounds[0]["min"][cls.Zrot, 1:] = -0.2
                    x_bounds[0]["max"][cls.Zrot, 1:] = 0.2

                else:
                    # initial bounds, same as final bounds of previous phase
                    for b in 0, 1, 2:
                        x_bounds[current_phase]["min"][:, b] = x_bounds[
                            current_phase - 1
                        ]["min"][:, 2]
                        x_bounds[current_phase]["max"][:, b] = x_bounds[
                            current_phase - 1
                        ]["max"][:, 2]

                    half_twists_till_now = sum(half_twists[:i])
                    if half_twists_till_now != 0:
                        x_bounds[current_phase]["min"][cls.Zrot, 2] = (
                            np.pi * half_twists_till_now - 0.2
                            if prefer_left
                            else -np.pi * half_twists_till_now - 0.2
                        )

                        x_bounds[current_phase]["max"][cls.Zrot, 2] = (
                            np.pi * half_twists_till_now + 0.2
                            if prefer_left
                            else -np.pi * half_twists_till_now + 0.2
                        )

                    if sum(half_twists[: i + 1]) == sum(half_twists):
                        x_bounds[current_phase]["min"][cls.Zrot, 1] = (
                            np.pi * half_twists_till_now - 0.2 - np.pi / 4
                            if prefer_left
                            else -np.pi * half_twists_till_now - 0.2
                        )

                        x_bounds[current_phase]["max"][cls.Zrot, 1] = (
                            np.pi * half_twists_till_now + 0.2
                            if prefer_left
                            else -np.pi * half_twists_till_now + 0.2 + np.pi / 4
                        )

                # legs
                x_bounds[current_phase]["min"][cls.XrotUpperLegs, 0] = -0.2
                x_bounds[current_phase]["max"][cls.XrotUpperLegs, 0] = 0.2
                x_bounds[current_phase]["min"][cls.XrotUpperLegs, 1] = -2.4 - 0.2
                x_bounds[current_phase]["max"][cls.XrotUpperLegs, 1] = 0.2
                x_bounds[current_phase]["min"][cls.XrotUpperLegs, 2] = -2.4 - 0.2
                x_bounds[current_phase]["max"][cls.XrotUpperLegs, 2] = -2.4 + 0.2

                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 0] = -0.2
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 0] = 0.2
                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 1] = -0.2
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 1] = 2.4 + 0.2
                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 2] = 2.4 - 0.2
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 2] = 2.4 + 0.2

                # Hips sides
                x_bounds[current_phase]["min"][cls.YrotUpperLegs, 2] = -0.1
                x_bounds[current_phase]["max"][cls.YrotUpperLegs, 2] = 0.1

            # somersaulting in tuck
            if i == nb_somersaults - 1 or next_have_twist:
                x_bounds.append(
                    {
                        "min": cls.q_min_bounds.copy(),
                        "max": cls.q_max_bounds.copy(),
                    }
                )
                current_phase += 1

                for b in 0, 1, 2:
                    x_bounds[current_phase]["min"][:, b] = x_bounds[current_phase - 1][
                        "min"
                    ][:, 2]
                    x_bounds[current_phase]["max"][:, b] = x_bounds[current_phase - 1][
                        "max"
                    ][:, 2]

                # somersaulting in tuck, for all no-twist somersaults, starting from last tuck
                x_bounds[current_phase]["min"][cls.Xrot, 1:] = (
                    min(
                        2 * np.pi * somersault_tuck_start - 0.2 - np.pi,
                        2 * np.pi * nb_somersaults - np.pi / 2 - 0.2,
                    )
                    if is_forward
                    else max(
                        -2 * np.pi * (i + 1) - 0.2,
                        -2 * np.pi * nb_somersaults + np.pi / 2 - 0.2,
                    )
                )
                x_bounds[current_phase]["max"][cls.Xrot, 1:] = (
                    min(
                        2 * np.pi * (i + 1) + 0.2,
                        2 * np.pi * nb_somersaults - np.pi / 2 + 0.2,
                    )
                    if is_forward
                    else max(
                        -2 * np.pi * somersault_tuck_start + 0.2 + np.pi,
                        -2 * np.pi * nb_somersaults + np.pi / 2 + 0.2,
                    )
                )

                # tilt pi / 8
                x_bounds[current_phase]["min"][cls.Yrot, :] = -np.pi / 8
                x_bounds[current_phase]["max"][cls.Yrot, :] = np.pi / 8

                # twisting
                # should be good with the end of twist from previous phase

                # rot legs, hips
                x_bounds[current_phase]["min"][cls.XrotUpperLegs, :] = -2.4 - 0.2
                x_bounds[current_phase]["max"][cls.XrotUpperLegs, :] = -2.4 + 0.2

                x_bounds[current_phase]["min"][cls.XrotLowerLegs, :] = 2.4 - 0.2
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, :] = 2.4 + 0.2

                # Hips sides
                x_bounds[current_phase]["min"][cls.YrotUpperLegs, :] = -0.1
                x_bounds[current_phase]["max"][cls.YrotUpperLegs, :] = 0.1

            # kick out
            if next_have_twist or is_last_somersault:
                x_bounds.append(
                    {
                        "min": cls.q_min_bounds.copy(),
                        "max": cls.q_max_bounds.copy(),
                    }
                )
                current_phase += 1

                for b in 0, 1, 2:
                    x_bounds[current_phase]["min"][:, b] = x_bounds[current_phase - 1][
                        "min"
                    ][:, 2]
                    x_bounds[current_phase]["max"][:, b] = x_bounds[current_phase - 1][
                        "max"
                    ][:, 2]

                # somersaulting
                x_bounds[current_phase]["min"][cls.Xrot, 1:] = (
                    min(
                        2 * np.pi * somersault_tuck_start - 0.2,
                        2 * np.pi * nb_somersaults - np.pi / 2 - 0.2,
                    )
                    if is_forward
                    else max(
                        -2 * np.pi * (i + 1) - 0.2,
                        -2 * np.pi * nb_somersaults + np.pi / 2 - 0.2,
                    )
                )
                x_bounds[current_phase]["max"][cls.Xrot, 1:] = (
                    min(
                        2 * np.pi * (i + 1) + 0.2,
                        2 * np.pi * nb_somersaults - np.pi / 2 + 0.2,
                    )
                    if is_forward
                    else max(
                        -2 * np.pi * somersault_tuck_start + 0.2,
                        -2 * np.pi * nb_somersaults + np.pi / 2 + 0.2,
                    )
                )

                # tilt pi / 4
                x_bounds[current_phase]["min"][cls.Yrot, :] = -np.pi / 4
                x_bounds[current_phase]["max"][cls.Yrot, :] = np.pi / 4

                # twisting
                x_bounds[current_phase]["min"][cls.Zrot, 1:] = (
                    np.pi * sum(half_twists[:i]) - 0.2
                    if prefer_left
                    else -np.pi * sum(half_twists[: i + 1])
                    - 0.2
                    + (np.pi * half_twists[i] / 2 if half_twists[i] != 0 else 0)
                )
                x_bounds[current_phase]["max"][cls.Zrot, 1:] = (
                    np.pi * sum(half_twists[: i + 1])
                    + 0.2
                    - (np.pi * half_twists[i] / 2 if half_twists[i] != 0 else 0)
                    if prefer_left
                    else -np.pi * sum(half_twists[:i]) + 0.2
                )

                # Hips flexion
                x_bounds[current_phase]["min"][cls.XrotUpperLegs, 0] = -2.4 + 0.2 - 0.01
                x_bounds[current_phase]["max"][cls.XrotUpperLegs, 0] = -2.4 + 0.2 + 0.01
                x_bounds[current_phase]["min"][cls.XrotUpperLegs, 1] = -2.4 + 0.2 - 0.01
                x_bounds[current_phase]["max"][cls.XrotUpperLegs, 1] = 0.35
                x_bounds[current_phase]["min"][cls.XrotUpperLegs, 2] = -0.35
                x_bounds[current_phase]["max"][cls.XrotUpperLegs, 2] = 0.35

                # lower legs
                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 0] = 2.4 - 0.2 - 0.01
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 0] = 2.4 + 0.2 + 0.01
                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 1] = -0.2 - 0.01
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 1] = 2.4 + 0.2 + 0.01
                x_bounds[current_phase]["min"][cls.XrotLowerLegs, 2] = -0.15
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, 2] = 0.15

            # twisting
            if next_have_twist:
                x_bounds.append(
                    {
                        "min": cls.q_min_bounds.copy(),
                        "max": cls.q_max_bounds.copy(),
                    }
                )
                current_phase += 1

                for b in 0, 1, 2:
                    x_bounds[current_phase]["min"][:, b] = x_bounds[current_phase - 1][
                        "min"
                    ][:, 2]
                    x_bounds[current_phase]["max"][:, b] = x_bounds[current_phase - 1][
                        "max"
                    ][:, 2]

                if is_last_somersault:
                    # tilt pi /8
                    x_bounds[current_phase]["min"][cls.Yrot, :] = -np.pi / 8
                    x_bounds[current_phase]["max"][cls.Yrot, :] = np.pi / 8

                    # somersault 1/4 left at then end
                    x_bounds[current_phase]["min"][cls.Xrot, 1] = (
                        2 * np.pi * i - 0.2
                        if is_forward
                        else -2 * np.pi * nb_somersaults + np.pi / 2 - 0.2
                    )
                    x_bounds[current_phase]["max"][cls.Xrot, 1] = (
                        2 * np.pi * nb_somersaults - np.pi / 2 + 0.2
                        if is_forward
                        else -2 * np.pi * i + 0.2
                    )
                    x_bounds[current_phase]["min"][cls.Xrot, 2] = (
                        2 * np.pi * nb_somersaults - np.pi / 2 - 0.2
                        if is_forward
                        else -2 * np.pi * nb_somersaults + np.pi / 2 - 0.2
                    )
                    x_bounds[current_phase]["max"][cls.Xrot, 2] = (
                        2 * np.pi * nb_somersaults - np.pi / 2 + 0.2
                        if is_forward
                        else -2 * np.pi * nb_somersaults + np.pi / 2 + 0.2
                    )

                    # finish twist
                    x_bounds[current_phase]["min"][cls.Zrot, 1] = (
                        sum(half_twists[:-1]) * np.pi - 0.2
                        if prefer_left
                        else -sum(half_twists) * np.pi - 0.2
                    )
                    x_bounds[current_phase]["max"][cls.Zrot, 1] = (
                        sum(half_twists) * np.pi + 0.2
                        if prefer_left
                        else -sum(half_twists[:-1]) * np.pi + 0.2
                    )
                    x_bounds[current_phase]["min"][cls.Zrot, 2] = (
                        sum(half_twists) * np.pi - 0.2
                        if prefer_left
                        else -sum(half_twists) * np.pi - 0.2
                    )
                    x_bounds[current_phase]["max"][cls.Zrot, 2] = (
                        sum(half_twists) * np.pi + 0.2
                        if prefer_left
                        else -sum(half_twists) * np.pi + 0.2
                    )

                    # Right arm
                    x_bounds[current_phase]["min"][cls.YrotRightUpperArm, 2] = 0
                    x_bounds[current_phase]["max"][cls.YrotRightUpperArm, 2] = np.pi / 8
                    # Left arm
                    x_bounds[current_phase]["min"][cls.YrotLeftUpperArm, 2] = -np.pi / 8
                    x_bounds[current_phase]["max"][cls.YrotLeftUpperArm, 2] = 0

                    # Right elbow
                    x_bounds[current_phase]["min"][
                        cls.ZrotRightLowerArm : cls.XrotRightLowerArm + 1, 2
                    ] = -0.1
                    x_bounds[current_phase]["max"][
                        cls.ZrotRightLowerArm : cls.XrotRightLowerArm + 1, 2
                    ] = 0.1
                    # Left elbow
                    x_bounds[current_phase]["min"][
                        cls.ZrotLeftLowerArm : cls.XrotLeftLowerArm + 1, 2
                    ] = -0.1
                    x_bounds[current_phase]["max"][
                        cls.ZrotLeftLowerArm : cls.XrotLeftLowerArm + 1, 2
                    ] = 0.1

                else:
                    # somersaulting
                    x_bounds[current_phase]["min"][cls.Xrot, 1:] = (
                        2 * np.pi * i - 0.2
                        if is_forward
                        else -2 * np.pi * (i + 1) - 0.2
                    )
                    x_bounds[current_phase]["max"][cls.Xrot, 1:] = (
                        2 * np.pi * (i + 1) + 0.2
                        if is_forward
                        else -2 * np.pi * i + 0.2
                    )

                    # tilt pi / 4
                    x_bounds[current_phase]["min"][cls.Yrot, :] = -np.pi / 4
                    x_bounds[current_phase]["max"][cls.Yrot, :] = np.pi / 4

                    # twisting
                    half_twist_till_now = sum(half_twists[:i])
                    if half_twist_till_now != 0:
                        x_bounds[current_phase]["min"][cls.Zrot, 1] = (
                            np.pi * sum(half_twists[:i]) - 0.2
                            if prefer_left
                            else -np.pi * sum(half_twists[: i + 1]) - 0.2
                        )
                        x_bounds[current_phase]["max"][cls.Zrot, 1] = (
                            np.pi * sum(half_twists[: i + 1]) + 0.2
                            if prefer_left
                            else -np.pi * sum(half_twists[:i]) + 0.2
                        )
                        x_bounds[current_phase]["min"][cls.Zrot, 2] = (
                            np.pi * sum(half_twists[: i + 1]) - 0.2 - np.pi / 4
                            if prefer_left
                            else -np.pi * sum(half_twists[: i + 1]) - 0.2
                        )
                        x_bounds[current_phase]["max"][cls.Zrot, 2] = (
                            np.pi * sum(half_twists[: i + 1]) + 0.2
                            if prefer_left
                            else -np.pi * sum(half_twists[: i + 1]) + 0.2 + np.pi / 4
                        )
                    else:
                        x_bounds[current_phase]["min"][cls.Zrot, 1] = (
                            np.pi * sum(half_twists[:i]) - 0.2
                            if prefer_left
                            else -np.pi * sum(half_twists[: i + 1]) - 0.2
                        )
                        x_bounds[current_phase]["max"][cls.Zrot, 1] = (
                            np.pi * sum(half_twists[: i + 1]) + 0.2
                            if prefer_left
                            else -np.pi * sum(half_twists[:i]) + 0.2
                        )
                        x_bounds[current_phase]["min"][cls.Zrot, 2] = (
                            np.pi * sum(half_twists[: i + 1]) - 0.2 - np.pi / 4
                            if prefer_left
                            else -np.pi * sum(half_twists[: i + 1]) - 0.2
                        )
                        x_bounds[current_phase]["max"][cls.Zrot, 2] = (
                            np.pi * sum(half_twists[: i + 1]) + 0.2
                            if prefer_left
                            else -np.pi * sum(half_twists[: i + 1]) + 0.2 + np.pi / 4
                        )

                # Hips flexion
                x_bounds[current_phase]["min"][cls.XrotUpperLegs, :] = -0.35
                x_bounds[current_phase]["max"][cls.XrotUpperLegs, :] = 0.35

                x_bounds[current_phase]["min"][cls.XrotLowerLegs, :] = -0.15
                x_bounds[current_phase]["max"][cls.XrotLowerLegs, :] = 0.15

            last_have_twist = next_have_twist
            next_have_twist = is_last_somersault or half_twists[i + 1] > 0

        # landing
        x_bounds.append(
            {
                "min": cls.q_min_bounds.copy(),
                "max": cls.q_max_bounds.copy(),
            }
        )
        current_phase += 1

        x_bounds[current_phase]["min"][:, 0] = x_bounds[current_phase - 1]["min"][:, 2]
        x_bounds[current_phase]["max"][:, 0] = x_bounds[current_phase - 1]["max"][:, 2]

        x_bounds[current_phase]["min"][[cls.X, cls.Y, cls.Z], 2] = [-0.01, -0.01, 0]
        x_bounds[current_phase]["max"][[cls.X, cls.Y, cls.Z], 2] = [0.01, 0.01, 0.01]

        # finish 1/4 somersault
        x_bounds[current_phase]["min"][cls.Xrot, 1] = (
            nb_somersaults * np.pi * 2 - np.pi / 2 - 0.2
            if is_forward
            else -nb_somersaults * np.pi * 2 - 0.2
        )
        x_bounds[current_phase]["max"][cls.Xrot, 1] = (
            nb_somersaults * np.pi * 2 + 0.2
            if is_forward
            else -nb_somersaults * np.pi * 2 + np.pi / 2 + 0.2
        )

        x_bounds[current_phase]["min"][cls.Xrot, 2] = (
            nb_somersaults * np.pi * 2 - 0.2
            if is_forward
            else -nb_somersaults * np.pi * 2 - 0.2
        )
        x_bounds[current_phase]["max"][cls.Xrot, 2] = (
            nb_somersaults * np.pi * 2 + 0.2
            if is_forward
            else -nb_somersaults * np.pi * 2 + 0.2
        )

        # twist finished
        x_bounds[current_phase]["min"][cls.Zrot, 1:] = (
            sum(half_twists) * np.pi - 0.2
            if prefer_left
            else -sum(half_twists) * np.pi - 0.2
        )
        x_bounds[current_phase]["max"][cls.Zrot, 1:] = (
            sum(half_twists) * np.pi + 0.2
            if prefer_left
            else -sum(half_twists) * np.pi + 0.2
        )

        # tilt pi / 16
        x_bounds[current_phase]["min"][cls.Yrot, :] = -np.pi / 16
        x_bounds[current_phase]["max"][cls.Yrot, :] = np.pi / 16

        # arms
        x_bounds[current_phase]["min"][cls.YrotRightUpperArm, 0] = 0
        x_bounds[current_phase]["max"][cls.YrotRightUpperArm, 0] = np.pi / 8
        x_bounds[current_phase]["min"][cls.YrotRightUpperArm, 2] = 2.9 - 0.1
        x_bounds[current_phase]["max"][cls.YrotRightUpperArm, 2] = 2.9 + 0.1
        x_bounds[current_phase]["min"][cls.ZrotRightUpperArm, 2] = -0.1
        x_bounds[current_phase]["max"][cls.ZrotRightUpperArm, 2] = 0.1
        # Left arm
        x_bounds[current_phase]["min"][cls.YrotLeftUpperArm, 0] = -np.pi / 8
        x_bounds[current_phase]["max"][cls.YrotLeftUpperArm, 0] = 0
        x_bounds[current_phase]["min"][cls.YrotLeftUpperArm, 2] = -2.9 - 0.1
        x_bounds[current_phase]["max"][cls.YrotLeftUpperArm, 2] = -2.9 + 0.1
        x_bounds[current_phase]["min"][cls.ZrotLeftUpperArm, 2] = -0.1
        x_bounds[current_phase]["max"][cls.ZrotLeftUpperArm, 2] = 0.1

        # Right elbow
        x_bounds[current_phase]["min"][
            cls.ZrotRightLowerArm : cls.XrotRightLowerArm + 1, 2
        ] = -0.1
        x_bounds[current_phase]["max"][
            cls.ZrotRightLowerArm : cls.XrotRightLowerArm + 1, 2
        ] = 0.1
        # Left elbow
        x_bounds[current_phase]["min"][
            cls.ZrotLeftLowerArm : cls.XrotLeftLowerArm + 1, 2
        ] = -0.1
        x_bounds[current_phase]["max"][
            cls.ZrotLeftLowerArm : cls.XrotLeftLowerArm + 1, 2
        ] = 0.1

        # Hips flexion
        x_bounds[current_phase]["min"][cls.XrotUpperLegs, :] = -0.60
        x_bounds[current_phase]["max"][cls.XrotUpperLegs, :] = 0.35
        x_bounds[current_phase]["min"][cls.XrotUpperLegs, 0] = 0
        x_bounds[current_phase]["max"][cls.XrotUpperLegs, 0] = 0.35
        x_bounds[current_phase]["min"][cls.XrotUpperLegs, 2] = -0.60
        x_bounds[current_phase]["max"][cls.XrotUpperLegs, 2] = -0.40

        x_bounds[current_phase]["min"][cls.XrotLowerLegs, :] = -0.15
        x_bounds[current_phase]["max"][cls.XrotLowerLegs, :] = 0.15

        # Hips sides
        x_bounds[current_phase]["min"][cls.YrotUpperLegs, 2] = -0.1
        x_bounds[current_phase]["max"][cls.YrotUpperLegs, 2] = 0.1

        return x_bounds

    @classmethod
    def get_q_init(
        cls, nb_phases: int, half_twists: list, prefer_left: bool = True
    ) -> list:
        x_inits = np.zeros((nb_phases, 2, cls.nb_q))
        x_bounds = cls.get_q_bounds(half_twists, prefer_left)

        for phase in range(5):
            x_inits[phase, 0] = (
                x_bounds[phase]["min"][:, 0] + x_bounds[phase]["max"][:, 0]
            ) / 2
            x_inits[phase, 1] = (
                x_bounds[phase]["min"][:, 2] + x_bounds[phase]["max"][:, 2]
            ) / 2

        return x_inits
