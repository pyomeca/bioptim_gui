from fastapi import APIRouter, HTTPException

from bioptim_gui_api.acrobatics_ocp.acrobatics_responses import *
from bioptim_gui_api.acrobatics_ocp.acrobatics_somersaults_constraints import (
    router as constraints_router,
)
from bioptim_gui_api.acrobatics_ocp.acrobatics_somersaults_objectives import (
    router as objectives_router,
)
from bioptim_gui_api.acrobatics_ocp.acrobatics_utils import (
    read_acrobatics_data,
    update_acrobatics_data,
)

router = APIRouter()
router.include_router(objectives_router)
router.include_router(constraints_router)


# somersaults info endpoints


@router.get("/", response_model=list)
def get_somersaults_info():
    somersaults_info = read_acrobatics_data("somersaults_info")
    return somersaults_info


@router.get("/{somersault_index}", response_model=dict)
def get_somersaults_info(somersault_index: int):
    n_somersaults = read_acrobatics_data("nb_somersaults")
    if somersault_index < 0 or somersault_index >= n_somersaults:
        raise HTTPException(
            status_code=404,
            detail=f"somersault_index must be between 0 and {n_somersaults - 1}",
        )
    somersaults_info = read_acrobatics_data("somersaults_info")
    return somersaults_info[somersault_index]


@router.put(
    "/{somersault_index}/nb_shooting_points",
    response_model=NbShootingPointsResponse,
)
def put_nb_shooting_points(
    somersault_index: int, nb_shooting_points: NbShootingPointsRequest
):
    if nb_shooting_points.nb_shooting_points <= 0:
        raise HTTPException(
            status_code=400, detail="nb_shooting_points must be positive"
        )
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index][
        "nb_shooting_points"
    ] = nb_shooting_points.nb_shooting_points
    update_acrobatics_data("somersaults_info", somersaults_info)
    return NbShootingPointsResponse(
        nb_shooting_points=nb_shooting_points.nb_shooting_points
    )


@router.put(
    "/{somersault_index}/duration",
    response_model=SomersaultDurationResponse,
)
def put_duration(somersault_index: int, duration: SomersaultDurationRequest):
    if duration.duration <= 0:
        raise HTTPException(status_code=400, detail="duration must be positive")
    infos = read_acrobatics_data()
    somersaults_info = infos["somersaults_info"]
    somersaults_info[somersault_index]["duration"] = duration.duration
    infos["final_time"] = sum(somersault["duration"] for somersault in somersaults_info)
    update_acrobatics_data("somersaults_info", somersaults_info)
    update_acrobatics_data("final_time", infos["final_time"])
    return SomersaultDurationResponse(duration=duration.duration)


@router.put(
    "/{somersault_index}/nb_half_twists",
    response_model=NbHalfTwistsResponse,
)
def put_nb_half_twist(somersault_index: int, nb_half_twists: NbHalfTwistsRequest):
    if nb_half_twists.nb_half_twists < 0:
        raise HTTPException(
            status_code=400, detail="nb_half_twists must be positive or zero"
        )
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index]["nb_half_twists"] = nb_half_twists.nb_half_twists
    update_acrobatics_data("somersaults_info", somersaults_info)
    return NbHalfTwistsResponse(nb_half_twists=nb_half_twists.nb_half_twists)
