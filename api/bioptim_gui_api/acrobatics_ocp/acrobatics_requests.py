from typing import Optional

from bioptim import QuadratureRule, Node
from pydantic import BaseModel

from bioptim_gui_api.penalty.enums import ObjectiveType

from bioptim_gui_api.acrobatics_ocp.enums import (
    Position,
    SportType,
    PreferredTwistSide,
)


class NbSomersaultsRequest(BaseModel):
    nb_somersaults: int


class ModelPathRequest(BaseModel):
    model_path: str


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


class NbShootingPointsRequest(BaseModel):
    nb_shooting_points: int


class SomersaultDurationRequest(BaseModel):
    duration: float


class NbHalfTwistsRequest(BaseModel):
    nb_half_twists: int


class NodesRequest(BaseModel):
    nodes: Node


class QuadraticRequest(BaseModel):
    quadratic: bool


class ExpandRequest(BaseModel):
    expand: bool


class TargetRequest(BaseModel):
    target: Optional[list] = None


class DerivativeRequest(BaseModel):
    derivative: bool


class IntegrationRuleRequest(BaseModel):
    integration_rule: QuadratureRule


class MultiThreadRequest(BaseModel):
    multi_thread: bool


class WeightRequest(BaseModel):
    weight: float


class ObjectiveTypeRequest(BaseModel):
    objective_type: ObjectiveType


class PenaltyTypeRequest(BaseModel):
    penalty_type: str


class ConstraintFcnRequest(BaseModel):
    penalty_type: str


class ObjectiveFcnRequest(BaseModel):
    penalty_type: str


class ArgumentRequest(BaseModel):
    type: str
    value: int | float | str | list | None
