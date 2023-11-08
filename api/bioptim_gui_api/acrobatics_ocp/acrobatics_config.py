import copy


class DefaultAcrobaticsConfig:
    datafile = "acrobatics_data.json"

    default_phases_info = {
        "phase_name": None,
        "nb_shooting_points": 40,
        "duration": 1.0,
        "objectives": [
            {
                "objective_type": "lagrange",
                "penalty_type": "MINIMIZE_CONTROL",
                "nodes": "all_shooting",
                "quadratic": True,
                "expand": True,
                "target": None,
                "derivative": False,
                "integration_rule": "rectangle_left",
                "multi_thread": False,
                "weight": 100.0,
                "arguments": [
                    {"name": "key", "value": "tau", "type": "string"},
                ],
            },
            {
                "objective_type": "mayer",
                "penalty_type": "MINIMIZE_TIME",
                "nodes": "end",
                "quadratic": True,
                "expand": True,
                "target": None,
                "derivative": False,
                "integration_rule": "rectangle_left",
                "multi_thread": False,
                "weight": 1.0,
                "arguments": [
                    {"name": "min_bound", "value": 0.9, "type": "float"},
                    {"name": "max_bound", "value": 1.1, "type": "float"},
                ],
            },
        ],
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
        "phases_info": [
            copy.deepcopy(default_phases_info),
            copy.deepcopy(default_phases_info),
        ],
    }
    base_data["phases_info"][0]["phase_name"] = "Somersault 1"
    base_data["phases_info"][1]["phase_name"] = "Landing"


def phase_name_to_phase(phase_name: str):
    # needed as there are nested list inside it
    # removing the deepcopy will cause issues on the objectives and constraints
    # some will be duplicated on all phases
    res = copy.deepcopy(DefaultAcrobaticsConfig.default_phases_info)
    res["phase_name"] = phase_name
    if phase_name == "Pike":
        for side in "D", "G":
            res["objectives"].append(
                {
                    "objective_type": "mayer",
                    "penalty_type": "SUPERIMPOSE_MARKERS",
                    "nodes": "end",
                    "quadratic": True,
                    "expand": True,
                    "target": None,
                    "derivative": False,
                    "integration_rule": "rectangle_left",
                    "multi_thread": False,
                    "weight": 1.0,
                    "arguments": [
                        {
                            "name": "first_marker",
                            "value": f"MidMain{side}",
                            "type": "str",
                        },
                        {
                            "name": "second_marker",
                            "value": f"CibleMain{side}",
                            "type": "str",
                        },
                    ],
                },
            )
    elif phase_name == "Somersault":
        for side in "D", "G":
            res["constraints"].append(
                {
                    "penalty_type": "SUPERIMPOSE_MARKERS",
                    "nodes": "all_shooting",
                    "quadratic": True,
                    "expand": True,
                    "target": None,
                    "derivative": False,
                    "integration_rule": "rectangle_left",
                    "multi_thread": False,
                    "weight": 1.0,
                    "arguments": [
                        {
                            "name": "min_bound",
                            "value": -0.05,
                            "type": "float",
                        },
                        {
                            "name": "max_bound",
                            "value": 0.05,
                            "type": "float",
                        },
                        {
                            "name": "first_marker",
                            "value": f"MidMain{side}",
                            "type": "str",
                        },
                        {
                            "name": "second_marker",
                            "value": f"CibleMain{side}",
                            "type": "str",
                        },
                    ],
                },
            )

    return res
