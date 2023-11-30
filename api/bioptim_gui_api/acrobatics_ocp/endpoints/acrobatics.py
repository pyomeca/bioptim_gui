from fastapi import APIRouter, HTTPException

import bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_code_generation as acrobatics_code_generation
import bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_phases as acrobatics_somersaults
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_responses import *
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_utils import *

router = APIRouter(
    prefix="/acrobatics",
    tags=["acrobatics"],
    responses={404: {"description": "Not found"}},
)
router.include_router(
    acrobatics_somersaults.router,
    prefix="/phases_info",
    responses={404: {"description": "Not found"}},
)
router.include_router(acrobatics_code_generation.router)


@router.get("/", response_model=dict)
def get_acrobatics_data():
    data = read_acrobatics_data()
    return data


@router.put("/nb_somersaults", response_model=dict)
def update_nb_somersaults(nb_somersaults: NbSomersaultsRequest):
    """
    Append or pop the half_twists list
    Update the number of somersaults of the acrobatics ocp
    Update the phase info of the acrobatics ocp accordingly
    """
    nb_max_somersaults = 5
    old_value = read_acrobatics_data("nb_somersaults")
    new_nb_somersaults = nb_somersaults.nb_somersaults

    if new_nb_somersaults <= 0 or new_nb_somersaults > nb_max_somersaults:
        raise HTTPException(status_code=400, detail="nb_somersaults must be positive")

    data = read_acrobatics_data()
    position = data["position"]
    updated_half_twists = data["nb_half_twists"][:new_nb_somersaults] + [0] * (new_nb_somersaults - old_value)

    # 1 somersault tuck/pike are not allowed, set the position to straight
    if new_nb_somersaults == 1 and position != "straight":
        update_acrobatics_data("position", "straight")
        new_phase_names = acrobatics_phase_names(new_nb_somersaults, "straight", updated_half_twists)
    else:
        new_phase_names = acrobatics_phase_names(new_nb_somersaults, position, updated_half_twists)

    update_acrobatics_data("nb_somersaults", new_nb_somersaults)
    update_acrobatics_data("nb_half_twists", updated_half_twists)
    update_phase_info(new_phase_names)

    return read_acrobatics_data()


@router.put(
    "/nb_half_twists/{somersault_index}",
    response_model=list,
)
def put_nb_half_twist(somersault_index: int, half_twists_request: NbHalfTwistsRequest):
    if half_twists_request.nb_half_twists < 0:
        raise HTTPException(status_code=400, detail="nb_half_twists must be positive or zero")
    half_twists = read_acrobatics_data("nb_half_twists")
    half_twists[somersault_index] = half_twists_request.nb_half_twists
    update_acrobatics_data("nb_half_twists", half_twists)

    data = read_acrobatics_data()
    nb_somersaults = data["nb_somersaults"]
    position = data["position"]
    half_twists = data["nb_half_twists"]
    with_visual_criteria = data["with_visual_criteria"]

    new_phase_names = acrobatics_phase_names(nb_somersaults, position, half_twists)

    new_phases = [
        config.phase_name_to_phase(position, new_phase_names, i, with_visual_criteria)
        for i, _ in enumerate(new_phase_names)
    ]

    data["phases_info"] = new_phases
    update_acrobatics_data("phases_info", new_phases)

    phases_info = read_acrobatics_data("phases_info")
    return phases_info


@router.put("/model_path", response_model=ModelPathResponse)
def put_model_path(model_path: ModelPathRequest):
    update_acrobatics_data("model_path", model_path.model_path)
    return ModelPathResponse(model_path=model_path.model_path)


@router.put("/final_time", response_model=FinalTimeResponse)
def put_final_time(final_time: FinalTimeRequest):
    new_value = final_time.final_time
    if new_value < 0:
        raise HTTPException(status_code=400, detail="final_time must be positive")
    update_acrobatics_data("final_time", new_value)
    return FinalTimeResponse(final_time=new_value)


@router.put("/final_time_margin", response_model=FinalTimeMarginResponse)
def put_final_time_margin(final_time_margin: FinalTimeMarginRequest):
    new_value = final_time_margin.final_time_margin
    if new_value < 0:
        raise HTTPException(status_code=400, detail="final_time_margin must be positive")
    update_acrobatics_data("final_time_margin", new_value)
    return FinalTimeMarginResponse(final_time_margin=new_value)


@router.get("/position", response_model=list)
def get_position():
    # TODO implement with frontend
    # nb_somersaults = read_acrobatics_data("nb_somersaults")
    # if nb_somersaults == 1:
    #     return [Position.STRAIGHT.capitalize()]
    return [side.capitalize() for side in Position]


@router.put("/position", response_model=dict)
def put_position(position: PositionRequest):
    new_value = position.position.value
    old_value = read_acrobatics_data("position")

    if old_value == new_value:
        raise HTTPException(
            status_code=304,
            detail=f"position is already {position}",
        )

    update_acrobatics_data("position", new_value)

    # TODO update phases
    data = read_acrobatics_data()
    nb_somersaults = data["nb_somersaults"]
    half_twists = data["nb_half_twists"]

    # 1 somersault tuck/pike are not allowed, set the nb_somersault to 2
    if old_value == "straight" and nb_somersaults == 1:
        update_acrobatics_data("position", new_value)
        update_acrobatics_data("nb_somersaults", 2)

        half_twists = data["nb_half_twists"] + [0]
        update_acrobatics_data("nb_half_twists", half_twists)

        new_phase_names = acrobatics_phase_names(2, new_value, half_twists)
        update_phase_info(new_phase_names)
    else:
        new_phase_names = acrobatics_phase_names(nb_somersaults, new_value, half_twists)
        update_phase_info(new_phase_names)

    return read_acrobatics_data()


@router.get("/sport_type", response_model=list)
def put_sport_type():
    return [side.capitalize() for side in SportType]


@router.put("/sport_type", response_model=SportTypeResponse)
def put_sport_type(sport_type: SportTypeRequest):
    new_value = sport_type.sport_type.value
    old_value = read_acrobatics_data("sport_type")

    if old_value == new_value:
        raise HTTPException(
            status_code=304,
            detail=f"sport_type is already {sport_type}",
        )

    update_acrobatics_data("sport_type", new_value)
    return SportTypeResponse(sport_type=new_value)


@router.get("/preferred_twist_side", response_model=list)
def get_preferred_twist_side():
    return [side.capitalize() for side in PreferredTwistSide]


@router.put("/preferred_twist_side", response_model=PreferredTwistSideResponse)
def put_preferred_twist_side(preferred_twist_side: PreferredTwistSideRequest):
    new_value = preferred_twist_side.preferred_twist_side.value
    old_value = read_acrobatics_data("preferred_twist_side")
    if old_value == new_value:
        raise HTTPException(
            status_code=304,
            detail=f"preferred_twist_side is already {preferred_twist_side}",
        )

    update_acrobatics_data("preferred_twist_side", new_value)
    return PreferredTwistSideResponse(preferred_twist_side=new_value)


@router.put("/with_visual_criteria", response_model=list)
def put_preferred_twist_side(visual_criteria: VisualCriteriaRequest):
    new_value = visual_criteria.with_visual_criteria
    old_value = read_acrobatics_data("with_visual_criteria")
    if old_value == new_value:
        raise HTTPException(
            status_code=304,
            detail=f"with_visual_criteria is already {old_value}",
        )

    update_acrobatics_data("with_visual_criteria", new_value)

    data = read_acrobatics_data()
    nb_somersaults = data["nb_somersaults"]
    position = data["position"]
    half_twists = data["nb_half_twists"]

    new_phase_names = acrobatics_phase_names(nb_somersaults, position, half_twists)
    update_phase_info(new_phase_names)

    phases_info = read_acrobatics_data("phases_info")
    return phases_info
