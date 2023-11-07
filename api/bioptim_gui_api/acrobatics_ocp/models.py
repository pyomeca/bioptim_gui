from pydantic import BaseModel

from bioptim_gui_api.penalty.models import Objective, Constraint


class SomersaultPhase(BaseModel):
    nb_shooting_points: int
    duration: float
    objectives: list[Objective]
    constraints: list[Constraint]
