from fastapi import APIRouter

from bioptim_gui_api.utils.format_utils import get_spaced_capitalized
from bioptim_gui_api.variables.misc.enums import Dynamics

router = APIRouter(
    prefix="/variables",
    tags=["variables"],
    responses={404: {"description": "Not found"}},
)


@router.get("/interpolation_type", response_model=list[str])
def get_interpolation_types():
    return [
        "CONSTANT",
        "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
        "LINEAR",
    ]


@router.get("/dynamics", response_model=list[str])
def get_dynamics_list():
    return get_spaced_capitalized(Dynamics)
