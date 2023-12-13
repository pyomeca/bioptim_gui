import copy

from bioptim_gui_api.acrobatics_ocp.misc.penalties.common import common_objectives
from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import (
    create_objective,
)
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)


class DefaultAcrobaticsConfig:
    """
    The default acrobatics config

    Attributes
    ----------
    datafile: str
        The file name that will be used to store the data and in the endpoints(e.g. "acrobatics_data.json")

    base_data: dict
        The base data at startup (e.g. {nb_somersaults, nb_half_twists, model_path, final_time, ...})
    """

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
        "dynamics": "torque_driven",
        "with_spine": False,
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
