from typing import Union

from bioptim import Axis

from bioptim_gui_api.acrobatics_ocp.acrobatics_requests import *


class NbSomersaultsResponse(NbSomersaultsRequest):
    pass


class ModelPathResponse(ModelPathRequest):
    pass


class FinalTimeResponse(FinalTimeRequest):
    pass


class FinalTimeMarginResponse(FinalTimeMarginRequest):
    pass


class PositionResponse(PositionRequest):
    pass


class SportTypeResponse(SportTypeRequest):
    pass


class PreferredTwistSideResponse(PreferredTwistSideRequest):
    pass


class NbShootingPointsResponse(NbShootingPointsRequest):
    pass


class SomersaultDurationResponse(SomersaultDurationRequest):
    pass


class NbHalfTwistsResponse(NbHalfTwistsRequest):
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
