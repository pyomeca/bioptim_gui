from enum import Enum


class Dynamics(str, Enum):
    """
    Not using bioptim.Dynamics because all dynamics are not implemented yet
    """

    TORQUE_DRIVEN = "TORQUE_DRIVEN"
    JOINTS_ACCELERATION_DRIVEN = "JOINTS_ACCELERATION_DRIVEN"


class InterpolationType(str, Enum):
    """
    Not using bioptim.InterpolationType because all interpolations types are not implemented yet
    """

    CONSTANT = "CONSTANT"
    CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT = "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT"
    LINEAR = "LINEAR"
