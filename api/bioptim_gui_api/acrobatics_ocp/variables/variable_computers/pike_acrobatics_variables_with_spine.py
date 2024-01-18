import numpy as np

from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.pike_acrobatics_variables import (
    PikeAcrobaticsVariables,
)
from bioptim_gui_api.variables.misc.variables_utils import LooseValue, define_loose_bounds


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

    dofs = [
        "Pelvis translation X",
        "Pelvis translation Y",
        "Pelvis translation Z",
        "Pelvis rotation X",
        "Pelvis rotation Y",
        "Pelvis rotation Z",
        "Stomach rotation X",
        "Stomach rotation Y",
        "Stomach rotation Z",
        "Rib rotation X",
        "Rib rotation Y",
        "Rib rotation Z",
        "Nipple rotation X",
        "Nipple rotation Y",
        "Nipple rotation Z",
        "Shoulder rotation X",
        "Shoulder rotation Y",
        "Shoulder rotation Z",
        "Right upper arm rotation Z",
        "Right upper arm rotation Y",
        "Right lower arm rotation Z",
        "Right lower arm rotation X",
        "Left upper arm rotation Z",
        "Left upper arm rotation Y",
        "Left lower arm rotation Z",
        "Left lower arm rotation X",
        "Upper legs rotation X",
        "Upper legs rotation Y",
    ]

    nb_q, nb_qdot, nb_tau = 28, 28, 22

    q_min_bounds = np.array(
        [
            [-1] * 3,
            [-1] * 3,
            [-0.1] * 3,
            [0] * 3,
            [-np.pi / 4] * 3,
            [0] * 3,
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
    def _fill_landing_phase(cls, x_bounds, half_twists: list) -> dict:
        super()._fill_landing_phase(x_bounds, half_twists)

        x_bounds[-1]["min"][cls.XrotStomach : cls.ZrotShoulder, 2] = -0.01
        x_bounds[-1]["max"][cls.XrotStomach : cls.ZrotShoulder, 2] = 0.01
