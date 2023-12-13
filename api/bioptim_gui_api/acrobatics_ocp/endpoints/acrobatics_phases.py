from fastapi import APIRouter, HTTPException

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_phases_constraints import (
    router as constraints_router,
)
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_phases_objectives import (
    router as objectives_router,
)
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_requests import (
    NbShootingPointsRequest,
    SomersaultDurationRequest,
)
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_responses import (
    NbShootingPointsResponse,
    SomersaultDurationResponse,
)
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_data import update_acrobatics_data, read_acrobatics_data

router = APIRouter()
router.include_router(objectives_router)
router.include_router(constraints_router)


# somersaults info endpoints


@router.get("/", response_model=list)
def get_phases_info():
    phases_info = read_acrobatics_data("phases_info")
    return phases_info


@router.get("/{phase_index}", response_model=dict)
def get_phase_info(phase_index: int):
    n_somersaults = read_acrobatics_data("nb_somersaults")
    if phase_index < 0 or phase_index >= n_somersaults:
        raise HTTPException(
            status_code=404,
            detail=f"phase_index must be between 0 and {n_somersaults - 1}",
        )
    phases_info = read_acrobatics_data("phases_info")
    return phases_info[phase_index]


@router.put("/{phase_index}/nb_shooting_points", response_model=NbShootingPointsResponse)
def put_nb_shooting_points(phase_index: int, nb_shooting_points: NbShootingPointsRequest):
    if nb_shooting_points.nb_shooting_points <= 0:
        raise HTTPException(status_code=400, detail="nb_shooting_points must be positive")
    phases_info = read_acrobatics_data("phases_info")
    phases_info[phase_index]["nb_shooting_points"] = nb_shooting_points.nb_shooting_points
    update_acrobatics_data("phases_info", phases_info)
    return NbShootingPointsResponse(nb_shooting_points=nb_shooting_points.nb_shooting_points)


@router.put("/{phase_index}/duration", response_model=SomersaultDurationResponse)
def put_duration(phase_index: int, duration: SomersaultDurationRequest):
    if duration.duration <= 0:
        raise HTTPException(status_code=400, detail="duration must be positive")
    infos = read_acrobatics_data()
    phases_info = infos["phases_info"]
    phases_info[phase_index]["duration"] = duration.duration
    infos["final_time"] = sum(somersault["duration"] for somersault in phases_info)
    update_acrobatics_data("phases_info", phases_info)
    update_acrobatics_data("final_time", infos["final_time"])
    return SomersaultDurationResponse(duration=duration.duration)
