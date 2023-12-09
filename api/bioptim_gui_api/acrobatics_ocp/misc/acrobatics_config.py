import copy
from typing import NamedTuple

from bioptim_gui_api.acrobatics_ocp.misc.penalties.collision_constraint import (
    collision_constraint_constraints,
    collision_constraint_objectives,
)
from bioptim_gui_api.acrobatics_ocp.misc.penalties.common import common_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.kickout import kickout_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.landing import landing_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.pike_tuck import pike_tuck_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.somersault import somersault_constraints, somersault_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.twist import twist_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.waiting import waiting_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.with_visual_criteria import with_visual_criteria_objectives
from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import (
    create_objective,
)
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)
from bioptim_gui_api.variables.misc.variables_config import get_variable_computer


class DefaultAcrobaticsConfig:
    datafile = "acrobatics_data.json"

    default_phases_info = {
        "phase_name": None,
        "nb_shooting_points": 40,
        "duration": 1.0,
        "objectives": common_objectives(),
        "constraints": [],
    }

    base_data = {
        "nb_somersaults": 1,
        "nb_half_twists": [0],
        "model_path": "",
        "final_time": 1.0,
        "final_time_margin": 0.1,
        "position": "straight",
        "sport_type": "trampoline",
        "preferred_twist_side": "left",
        "with_visual_criteria": False,
        "collision_constraint": False,
        "phases_info": [
            copy.deepcopy(default_phases_info),
            copy.deepcopy(default_phases_info),
        ],
    }
    base_data["phases_info"][0]["phase_name"] = "Somersault 1"
    base_data["phases_info"][1]["phase_name"] = "Landing"

    base_data["phases_info"][0]["objectives"].append(
        create_objective(
            objective_type="lagrange",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="all_shooting",
            weight=50000.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {
                    "name": "index",
                    "value": StraightAcrobaticsVariables.shoulder_dofs,
                    "type": "list",
                },
            ],
        )
    )
    base_data["phases_info"][0]["objectives"].append(
        create_objective(
            objective_type="mayer",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="all",
            weight=100.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {
                    "name": "index",
                    "value": [StraightAcrobaticsVariables.Yrot],
                    "type": "list",
                },
            ],
        )
    )

    # land safely
    base_data["phases_info"][1]["objectives"].append(
        create_objective(
            objective_type="mayer",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="end",
            weight=1000.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {
                    "name": "index",
                    "value": [StraightAcrobaticsVariables.Yrot],
                    "type": "list",
                },
            ],
        )
    )


class AdditionalCriteria(NamedTuple):
    with_visual_criteria: bool = False
    collision_constraint: bool = False
    without_cone: bool = False


def get_phase_objectives(
    phase_names: list[str], phase_index: int, position: str, additional_criteria: AdditionalCriteria
):
    with_visual_criteria = additional_criteria.with_visual_criteria
    collision_constraint = additional_criteria.collision_constraint

    phase_name = phase_names[phase_index]
    model = get_variable_computer(position, with_visual_criteria)

    objectives = common_objectives(
        phase_name=phase_names[phase_index], position=position, phase_index=phase_index, model=model
    )

    objectives += pike_tuck_objectives(phase_name, model)
    objectives += kickout_objectives(phase_name, model)
    objectives += twist_objectives(phase_name, model)
    objectives += waiting_objectives(phase_name, model)
    objectives += landing_objectives(phase_name, model, position)
    objectives += somersault_objectives(phase_name, model, position)

    if with_visual_criteria:
        objectives += with_visual_criteria_objectives(phase_names, phase_index, model)

    if collision_constraint:
        objectives += collision_constraint_objectives(phase_names, phase_index, position)

    return objectives


def get_phase_constraints(phase_name: str, position: str, additional_criteria: AdditionalCriteria):
    with_visual_criteria = additional_criteria.with_visual_criteria
    collision_constraint = additional_criteria.collision_constraint

    model = get_variable_computer(position, with_visual_criteria)
    constraints = []
    constraints += somersault_constraints(phase_name, model, position)

    if collision_constraint:
        constraints += collision_constraint_constraints(phase_name, position)

    return constraints


def phase_name_to_info(position, phase_names: str, phase_index: int, additional_criteria: AdditionalCriteria):
    phase_name = phase_names[phase_index]

    # need to deepcopy or else there will be unwanted modification due to addresses
    res = copy.deepcopy(DefaultAcrobaticsConfig.default_phases_info)
    res["phase_name"] = phase_name

    res["objectives"] = get_phase_objectives(phase_names, phase_index, position, additional_criteria)
    res["constraints"] = get_phase_constraints(phase_name, position, additional_criteria)

    return res
