from enum import Enum


class ObjectiveType(str, Enum):
    MAYER = "mayer"
    LAGRANGE = "lagrange"
