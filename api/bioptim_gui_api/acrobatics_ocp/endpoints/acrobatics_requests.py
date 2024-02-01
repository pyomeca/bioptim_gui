from pydantic import BaseModel

from bioptim_gui_api.acrobatics_ocp.misc.enums import (
    Position,
    SportType,
    PreferredTwistSide,
)


class NbSomersaultsRequest(BaseModel):
    nb_somersaults: int


class NbHalfTwistsRequest(BaseModel):
    nb_half_twists: int


class FinalTimeRequest(BaseModel):
    final_time: float


class FinalTimeMarginRequest(BaseModel):
    final_time_margin: float


class PositionRequest(BaseModel):
    position: Position


class SportTypeRequest(BaseModel):
    sport_type: SportType


class PreferredTwistSideRequest(BaseModel):
    preferred_twist_side: PreferredTwistSide


class VisualCriteriaRequest(BaseModel):
    with_visual_criteria: bool


class CollisionConstraintRequest(BaseModel):
    collision_constraint: bool


class WithSpineRequest(BaseModel):
    with_spine: bool
