from typing import NamedTuple

from pydantic import BaseModel

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_requests import (
    FinalTimeMarginRequest,
    FinalTimeRequest,
    PreferredTwistSideRequest,
    SportTypeRequest,
)


class FinalTimeResponse(FinalTimeRequest):
    pass


class FinalTimeMarginResponse(FinalTimeMarginRequest):
    pass


class SportTypeResponse(SportTypeRequest):
    pass


class PreferredTwistSideResponse(PreferredTwistSideRequest):
    pass


class NewGeneratedBioMod(NamedTuple):
    new_model: str
    new_model_path: str


class CodeGenerationResponse(BaseModel):
    generated_code: str
    new_models: list[NewGeneratedBioMod]
