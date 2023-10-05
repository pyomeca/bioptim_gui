from bioptim import Node, QuadratureRule
from fastapi import APIRouter

router = APIRouter(
    prefix="/penalties",
    tags=["penalties"],
    responses={404: {"description": "Not found"}},
)


@router.get("/nodes", response_model=list[str])
def get_nodes():
    return [node.value.replace("_", " ").capitalize() for node in Node]


@router.get("/integration_rules", response_model=list[str])
def get_integration_rules():
    return [
        integration_rule.value.replace("_", " ").capitalize()
        for integration_rule in QuadratureRule
    ]
