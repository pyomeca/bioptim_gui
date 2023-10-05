class DefaultVariablesConfig:
    default_dummy_variables = {
        "state_variables": [
            {
                "name": "coucou",
                "dimension": 1,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": [[-1.0, -2.0, -3.0]],
                    "max_bounds": [[1.0, 2.0, 3.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[4.0]],
            },
        ],
        "control_variables": [
            {
                "name": "tata",
                "dimension": 1,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": [[-100.0, -200.0, -300.0]],
                    "max_bounds": [[100.0, 200.0, 300.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[400.0]],
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
                    "min_bounds": [[-1.0, -2.0, -3.0]],
                    "max_bounds": [[1.0, 2.0, 3.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[4.0]],
            },
            {
                "name": "qdot",
                "dimension": 1,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": [[-10.0, -20.0, -30.0]],
                    "max_bounds": [[10.0, 20.0, 30.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[40.0]],
            },
        ],
        "control_variables": [
            {
                "name": "tau",
                "dimension": 1,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": [[-100.0, -200.0, -300.0]],
                    "max_bounds": [[100.0, 200.0, 300.0]],
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": [[400.0]],
            },
        ],
    }
