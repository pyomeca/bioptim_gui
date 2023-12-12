from enum import Enum


class PreferredTwistSide(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class SportType(str, Enum):
    TRAMPOLINE = "trampoline"
    DIVING = "diving"


class Position(str, Enum):
    STRAIGHT = "straight"
    TUCK = "tuck"
    PIKE = "pike"


class Dynamics(str, Enum):
    TORQUE_DRIVEN = "torque_driven"
    JOINTS_ACCELERATION_DRIVEN = "joints_acceleration_driven"


class Node(str, Enum):
    START = "start"
    MID = "mid"
    INTERMEDIATES = "intermediates"
    PENULTIMATE = "penultimate"
    END = "end"
    ALL = "all"
    ALL_SHOOTING = "all_shooting"
    TRANSITION = "transition"
    MULTINODES = "multinodes"
    DEFAULT = "default"
    ALL_3 = "all[3:]"
    ALL_3_ = "all[:-3]"
