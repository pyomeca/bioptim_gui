from typing import Union

from bioptim import Axis

from bioptim_gui_api.generic_ocp.generic_ocp_requests import *


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
    value: Union[int, float, str, list, None, Axis]
