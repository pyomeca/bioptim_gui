import copy

from bioptim_gui_api.acrobatics_ocp.penalties.phases.common import common_objectives
from bioptim_gui_api.generic_ocp.misc.generic_ocp_data import GenericOCPData
from bioptim_gui_api.variables.misc.variables_config import DefaultVariablesConfig


class AcrobaticsOCPData(GenericOCPData):
    datafile = "acrobatics_data.json"

    default_phases_info = {
        "phase_name": None,
        "nb_shooting_points": 40,
        "duration": 1.0,
        "objectives": common_objectives(),
        "constraints": [],
        "state_variables": DefaultVariablesConfig.default_torque_driven_variables["state_variables"].copy(),
        "control_variables": DefaultVariablesConfig.default_torque_driven_variables["control_variables"].copy(),
    }

    base_data = {
        "nb_phases": 2,
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
