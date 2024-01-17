class ImportGeneration:
    """
    This class contains the imports for the acrobatics generation
    """

    @classmethod
    def generate_imports(cls) -> str:
        return """\"""This file was automatically generated using BioptimGUI version 0.0.1\"""

import argparse
import biorbd
import casadi as cas
import os
from pathlib import Path
import pickle as pkl
import time
import sys

import numpy as np
from bioptim import (
    Axis,
    BiMappingList,
    BiorbdModel,
    BoundsList,
    ConstraintFcn,
    ConstraintList,
    DynamicsFcn,
    DynamicsList,
    InitialGuessList,
    InterpolationType,
    MagnitudeType,
    MultinodeConstraintFcn,
    MultinodeConstraintList,
    MultiStart,
    Node,
    ObjectiveFcn,
    ObjectiveList,
    OptimalControlProgram,
    PenaltyController,
    QuadratureRule,
    Solution,
    Solver,
)
"""
