import copy

from bioptim_gui_api.acrobatics_ocp.misc.penalties.common import common_objectives


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
