from fastapi import APIRouter

from bioptim_gui_api.utils.format_utils import get_spaced_capitalized
from bioptim_gui_api.variables.misc.enums import Dynamics, InterpolationType

router = APIRouter(
    prefix="/variables",
    tags=["variables"],
    responses={404: {"description": "Not found"}},
)


@router.get("/interpolation_type", response_model=list[str])
def get_interpolation_types():
    # TODO all interpolations types are not implemented yet,
    #  use get_spaced_capitalized on bioptim.Interpolation_Type when they are
    return get_spaced_capitalized(InterpolationType)


@router.get("/dynamics", response_model=list[str])
def get_dynamics_list():
    return get_spaced_capitalized(Dynamics)


@router.get("/available_values", response_model=dict)
def variables_get_available_values():
    return {
        "interpolation_types": get_interpolation_types(),
        "dynamics": get_dynamics_list(),
    }
