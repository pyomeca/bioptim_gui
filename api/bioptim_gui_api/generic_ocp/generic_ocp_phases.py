from fastapi import APIRouter, HTTPException

import bioptim_gui_api.variables.variables_config as variables_config
from bioptim_gui_api.generic_ocp.generic_ocp_phases_constraints import (
    router as constraints_router,
)
from bioptim_gui_api.generic_ocp.generic_ocp_phases_control_variables import (
    router as control_variables_router,
)
from bioptim_gui_api.generic_ocp.generic_ocp_phases_objectives import (
    router as objectives_router,
)
from bioptim_gui_api.generic_ocp.generic_ocp_phases_state_variables import (
    router as state_variables_router,
)
from bioptim_gui_api.generic_ocp.generic_ocp_responses import *
from bioptim_gui_api.generic_ocp.generic_ocp_utils import (
    read_generic_ocp_data,
    update_generic_ocp_data,
)

router = APIRouter()
router.include_router(state_variables_router)
router.include_router(control_variables_router)
router.include_router(objectives_router)
router.include_router(constraints_router)


# phases info endpoints


@router.get("/", response_model=list)
def get_phases_info():
    phases_info = read_generic_ocp_data("phases_info")
    return phases_info


@router.get("/{phase_index}", response_model=dict)
def get_phases_info(phase_index: int):
    n_phases = read_generic_ocp_data("nb_phases")
    if phase_index < 0 or phase_index >= n_phases:
        raise HTTPException(
            status_code=404,
            detail=f"phase_index must be between 0 and {n_phases - 1}",
        )
    phases_info = read_generic_ocp_data("phases_info")
    return phases_info[phase_index]


@router.put(
    "/{phase_index}/nb_shooting_points",
    response_model=NbShootingPointsResponse,
)
def put_nb_shooting_points(
    phase_index: int, nb_shooting_points: NbShootingPointsRequest
):
    if nb_shooting_points.nb_shooting_points <= 0:
        raise HTTPException(
            status_code=400, detail="nb_shooting_points must be positive"
        )
    phases_info = read_generic_ocp_data("phases_info")
    phases_info[phase_index][
        "nb_shooting_points"
    ] = nb_shooting_points.nb_shooting_points
    update_generic_ocp_data("phases_info", phases_info)
    return NbShootingPointsResponse(
        nb_shooting_points=nb_shooting_points.nb_shooting_points
    )


@router.put(
    "/{phase_index}/duration",
    response_model=PhaseDurationResponse,
)
def put_duration(phase_index: int, duration: PhaseDurationRequest):
    if duration.duration <= 0:
        raise HTTPException(status_code=400, detail="duration must be positive")
    infos = read_generic_ocp_data()
    phases_info = infos["phases_info"]
    phases_info[phase_index]["duration"] = duration.duration
    update_generic_ocp_data("phases_info", phases_info)
    return PhaseDurationResponse(duration=duration.duration)


@router.get("/{phase_index}/dynamics", response_model=list)
def get_dynamics_list():
    return ["TORQUE_DRIVEN", "DUMMY"]


@router.put("/{phase_index}/dynamics", response_model=list)
def put_dynamics_list(phase_index: int, dynamic_req: DynamicsRequest):
    phases_info = read_generic_ocp_data("phases_info")

    new_dynamic = dynamic_req.dynamics

    phases_info[phase_index]["dynamics"] = new_dynamic

    if new_dynamic == "TORQUE_DRIVEN":
        phases_info[phase_index][
            "state_variables"
        ] = variables_config.DefaultVariablesConfig.default_torque_driven_variables[
            "state_variables"
        ]
        phases_info[phase_index][
            "control_variables"
        ] = variables_config.DefaultVariablesConfig.default_torque_driven_variables[
            "control_variables"
        ]
    else:
        phases_info[phase_index][
            "state_variables"
        ] = variables_config.DefaultVariablesConfig.default_dummy_variables[
            "state_variables"
        ]
        phases_info[phase_index][
            "control_variables"
        ] = variables_config.DefaultVariablesConfig.default_dummy_variables[
            "control_variables"
        ]
    update_generic_ocp_data("phases_info", phases_info)

    return phases_info
