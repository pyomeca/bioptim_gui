from typing import Union

from bioptim import Axis
from pydantic import BaseModel

from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_requests import (
    ConstraintFcnRequest,
    ExpandRequest,
    DerivativeRequest,
    IntegrationRuleRequest,
    ModelPathRequest,
    MultiThreadRequest,
    NbShootingPointsRequest,
    NbPhasesRequest,
    NodesRequest,
    ObjectiveFcnRequest,
    ObjectiveTypeRequest,
    PenaltyTypeRequest,
    PhaseDurationRequest,
    QuadraticRequest,
    TargetRequest,
    WeightRequest,
)


class NbPhasesResponse(NbPhasesRequest):
    pass


class ModelPathResponse(ModelPathRequest):
    pass


class NbShootingPointsResponse(NbShootingPointsRequest):
    pass


class PhaseDurationResponse(PhaseDurationRequest):
    pass


class NodesResponse(NodesRequest):
    pass


class QuadraticResponse(QuadraticRequest):
    pass


class ExpandResponse(ExpandRequest):
    pass


class TargetResponse(TargetRequest):
    pass


class DerivativeResponse(DerivativeRequest):
    pass


class IntegrationRuleResponse(IntegrationRuleRequest):
    pass


class MultiThreadResponse(MultiThreadRequest):
    pass


class WeightResponse(WeightRequest):
    pass


class ObjectiveTypeResponse(ObjectiveTypeRequest):
    pass


class PenaltyTypeResponse(PenaltyTypeRequest):
    pass


class ConstraintFcnResponse(ConstraintFcnRequest):
    pass


class ObjectiveFcnResponse(ObjectiveFcnRequest):
    pass


class ArgumentResponse(BaseModel):
    key: str
    type: str
    value: Union[float, int, str, list, None, Axis]
