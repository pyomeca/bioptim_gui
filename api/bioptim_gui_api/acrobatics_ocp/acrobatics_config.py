class DefaultAcrobaticsConfig:
    datafile = "acrobatics_data.json"

    default_somersaults_info = {
        "nb_shooting_points": 24,
        "nb_half_twists": 0,
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
        "model_path": "",
        "final_time": 1.0,
        "final_time_margin": 0.1,
        "position": "straight",
        "sport_type": "trampoline",
        "preferred_twist_side": "left",
        "somersaults_info": [default_somersaults_info.copy()],
    }
