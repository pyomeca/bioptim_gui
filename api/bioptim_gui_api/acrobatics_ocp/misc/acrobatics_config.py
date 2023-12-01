import copy

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
from bioptim_gui_api.variables.misc.variables_utils import get_variable_computer


class DefaultAcrobaticsConfig:
    datafile = "acrobatics_data.json"

    default_phases_info = {
        "phase_name": None,
        "nb_shooting_points": 40,
        "duration": 1.0,
        "objectives": common_objectives(default=True),
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


def phase_name_to_phase(position, phase_names: str, phase_index: int, with_visual_criteria: bool = False):
    model = get_variable_computer(position, with_visual_criteria)

    # needed as there are nested list inside it
    # removing the deepcopy will cause issues on the objectives and constraints
    # some will be duplicated on all phases
    res = copy.deepcopy(DefaultAcrobaticsConfig.default_phases_info)

    objectives = common_objectives(phase_name=phase_names[phase_index], position=position, phase_index=phase_index)
    constraints = []

    phase_name = phase_names[phase_index]
    res["phase_name"] = phase_name

    if phase_name in ["Pike", "Tuck"]:
        objectives += pike_tuck_objectives(phase_name, model)
    elif phase_name == "Kick out":
        objectives += kickout_objectives(phase_name, model)
    elif phase_name == "Twist":
        objectives += twist_objectives(phase_name, model)
    elif phase_name == "Somersault":
        constraints += somersault_constraints(phase_name, model, position)
    elif phase_name == "Waiting":
        objectives += waiting_objectives(phase_name, model)
    elif phase_name == "Landing":
        objectives += landing_objectives(phase_name, model, position)

    if "Somersault" in phase_name:
        objectives += somersault_objectives(phase_name, model, position)

    if with_visual_criteria:
        objectives += with_visual_criteria_objectives(phase_names, phase_index, model)

    res["objectives"] = objectives
    res["constraints"] = constraints

    return res
