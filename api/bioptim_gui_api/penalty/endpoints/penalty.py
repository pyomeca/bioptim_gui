from bioptim import QuadratureRule
from fastapi import APIRouter

from bioptim_gui_api.acrobatics_ocp.misc.enums import Node

router = APIRouter(
    prefix="/penalties",
    tags=["penalties"],
    responses={404: {"description": "Not found"}},
)


def get_spaced_capitalized(enum) -> list:
    return [e.value.replace("_", " ").capitalize() for e in enum]


@router.get("/nodes", response_model=list[str])
def get_nodes():
    return get_spaced_capitalized(Node)


@router.get("/integration_rules", response_model=list[str])
def get_integration_rules():
    return get_spaced_capitalized(QuadratureRule)
