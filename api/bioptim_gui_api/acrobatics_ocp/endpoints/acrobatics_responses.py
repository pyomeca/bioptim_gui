from typing import NamedTuple

from pydantic import BaseModel

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_requests import (
    FinalTimeMarginRequest,
    FinalTimeRequest,
    PreferredTwistSideRequest,
    SportTypeRequest,
)
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_requests import PhaseDurationRequest


class FinalTimeResponse(FinalTimeRequest):
    new_phase_duration: float


class FinalTimeMarginResponse(FinalTimeMarginRequest):
    pass


class SportTypeResponse(SportTypeRequest):
    pass


class PreferredTwistSideResponse(PreferredTwistSideRequest):
    pass


class AcrobaticPhaseDurationResponse(PhaseDurationRequest):
    new_final_time: float


class NewGeneratedBioMod(NamedTuple):
    new_model: str
    new_model_path: str


class CodeGenerationResponse(BaseModel):
    generated_code: str
    new_models: list[NewGeneratedBioMod]
