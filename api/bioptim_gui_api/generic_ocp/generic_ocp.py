import json

from fastapi import APIRouter, HTTPException

import bioptim_gui_api.generic_ocp.generic_ocp_config as config
from bioptim_gui_api.generic_ocp.generic_ocp_code_generation import (
    router as code_generation_router,
)
from bioptim_gui_api.generic_ocp.generic_ocp_phases import router as phases_router
from bioptim_gui_api.generic_ocp.generic_ocp_responses import *
from bioptim_gui_api.generic_ocp.generic_ocp_utils import (
    read_generic_ocp_data,
    update_generic_ocp_data,
)

router = APIRouter(
    prefix="/generic_ocp",
    tags=["generic_ocp"],
    responses={404: {"description": "Not found"}},
)
router.include_router(
    phases_router,
    prefix="/phases_info",
    tags=["phases"],
    responses={404: {"description": "Not found"}},
)
router.include_router(code_generation_router)


def add_phase_info(n: int = 1) -> None:
    if n < 1:
        raise ValueError("n must be positive")

    data = read_generic_ocp_data()
    phases_info = data["phases_info"]
    before = len(phases_info)

    for i in range(before, before + n):
        phases_info.append(config.DefaultGenericOCPConfig.default_phases_info)

    data["phases_info"] = phases_info
    with open(config.DefaultGenericOCPConfig.datafile, "w") as f:
        json.dump(data, f)


def remove_phase_info(n: int = 0) -> None:
    if n < 0:
        raise ValueError("n must be positive")
    data = read_generic_ocp_data()
    phases_info = data["phases_info"]
    before = len(phases_info)
    n_phases = before - n

    for _ in range(n):
        phases_info.pop()
    data["phases_info"] = phases_info
    with open(config.DefaultGenericOCPConfig.datafile, "w") as f:
        json.dump(data, f)


@router.get("/", response_model=dict)
def get_generic_ocp_data():
    data = read_generic_ocp_data()
    return data


@router.put("/nb_phases", response_model=dict)
def update_nb_phases(nb_phases: NbPhasesRequest):
    old_value = read_generic_ocp_data("nb_phases")
    new_value = nb_phases.nb_phases
    if new_value < 0:
        raise HTTPException(status_code=400, detail="nb_phases must be positive")

    if new_value > old_value:
        add_phase_info(new_value - old_value)
    elif new_value < old_value:
        remove_phase_info(old_value - new_value)

    update_generic_ocp_data("nb_phases", new_value)

    data = read_generic_ocp_data()
    return data


@router.put("/model_path", response_model=ModelPathResponse)
def put_model_path(model_path: ModelPathRequest):
    update_generic_ocp_data("model_path", model_path.model_path)
    return ModelPathResponse(model_path=model_path.model_path)
