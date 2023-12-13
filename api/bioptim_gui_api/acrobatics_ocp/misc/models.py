from typing import NamedTuple

from pydantic import BaseModel

from bioptim_gui_api.penalty.misc.models import Objective, Constraint


class SomersaultPhase(BaseModel):
    nb_shooting_points: int
    duration: float
    objectives: list[Objective]
    constraints: list[Constraint]


class AdditionalCriteria(NamedTuple):
    """
    The additional criteria (e.g. with_visual_criteria, collision_constraint, without_cone)
    Can be used to add/remove additional criteria to the acrobatics that would otherwise result in more/less arguments
    in functions that depends on it (objectives, constraints, code generation, model conversion, ...)
    """

    with_visual_criteria: bool = False
    collision_constraint: bool = False
    without_cone: bool = False
    with_spine: bool = False
