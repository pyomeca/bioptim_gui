from typing import Optional

from bioptim import QuadratureRule, Node
from pydantic import BaseModel

from bioptim_gui_api.penalty.enums import ObjectiveType


class Penalty(BaseModel):
    penalty_type: str
    nodes: Node
    quadratic: bool = True
    expand: bool = True
    target: Optional[list] = None
    derivative: bool = False
    integration_rule: QuadratureRule = QuadratureRule.RECTANGLE_LEFT
    multi_thread: bool = False
    arguments: dict


class Objective(Penalty):
    weight: float = 1.0
    objective_type: ObjectiveType = ObjectiveType.MAYER


class Constraint(Penalty):
    pass
