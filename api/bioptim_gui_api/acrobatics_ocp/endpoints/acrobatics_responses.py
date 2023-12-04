from typing import Union

from bioptim import Axis

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_requests import *


class ModelPathResponse(ModelPathRequest):
    pass


class FinalTimeResponse(FinalTimeRequest):
    pass


class FinalTimeMarginResponse(FinalTimeMarginRequest):
    pass


class SportTypeResponse(SportTypeRequest):
    pass


class PreferredTwistSideResponse(PreferredTwistSideRequest):
    pass


class VisualCriteriaResponse(VisualCriteriaRequest):
    pass


class NbShootingPointsResponse(NbShootingPointsRequest):
    pass


class SomersaultDurationResponse(SomersaultDurationRequest):
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


class ArgumentResponse(BaseModel):
    key: str
    type: str
    value: Union[int, float, str, list, None, Axis]


class CodeGenerationResponse(BaseModel):
    generated_code: str
    new_model: str
    new_model_path: str
