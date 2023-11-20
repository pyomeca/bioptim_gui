from fastapi import APIRouter

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
    return [
        "TORQUE_DRIVEN",
        "DUMMY",
    ]
