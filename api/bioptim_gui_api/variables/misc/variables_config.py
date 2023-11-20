class DefaultVariablesConfig:
    default_dummy_variables = {
        "state_variables": [
            {
                "name": "coucou",
                "dimension": 1,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": [[0.0, 0.0, 0.0]],
                    "max_bounds": [[0.0, 0.0, 0.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[0.0]],
            },
        ],
        "control_variables": [
            {
                "name": "tata",
                "dimension": 1,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": [[0.0, 0.0, 0.0]],
                    "max_bounds": [[0.0, 0.0, 0.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[0.0]],
            },
        ],
    }

    default_torque_driven_variables = {
        "state_variables": [
            {
                "name": "q",
                "dimension": 1,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": [[0.0, 0.0, 0.0]],
                    "max_bounds": [[0.0, 0.0, 0.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[0.0]],
            },
            {
                "name": "qdot",
                "dimension": 1,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": [[0.0, 0.0, 0.0]],
                    "max_bounds": [[0.0, 0.0, 0.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[0.0]],
            },
        ],
        "control_variables": [
            {
                "name": "tau",
                "dimension": 1,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": [[0.0, 0.0, 0.0]],
                    "max_bounds": [[0.0, 0.0, 0.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[0.0]],
            },
        ],
    }
