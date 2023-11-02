from bioptim_gui_api.variables.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)


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

    @classmethod
    def get_q_bounds(
        cls, min_bounds, max_bounds, half_twists: list, prefer_left: bool
    ) -> dict:
        min_bounds_cpy = min_bounds.copy()
        max_bounds_cpy = max_bounds.copy()

        min_bounds_cpy[cls.YrotUpperLegs, :] = -0.1
        max_bounds_cpy[cls.YrotUpperLegs, :] = 0.1

        return super().get_q_bounds(
            min_bounds_cpy, max_bounds_cpy, half_twists, prefer_left
        )
