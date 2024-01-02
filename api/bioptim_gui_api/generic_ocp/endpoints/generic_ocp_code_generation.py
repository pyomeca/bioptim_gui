from fastapi import APIRouter

from bioptim_gui_api.generic_ocp.code_generation.generic_generation_utils import generic_generated_code
from bioptim_gui_api.generic_ocp.misc.generic_ocp_data import GenericOCPData

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/generate_code", response_model=str)
def get_generic_ocp_generated_code():
    data = GenericOCPData.read_data()

    generated_code = generic_generated_code(data)

    return generated_code
