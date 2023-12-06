from bioptim_gui_api.penalty.misc.penalty_utils import create_constraint, create_objective


def collision_constraint_objectives(phase_names, phase_index, model):
    objectives = []

    objectives.append(
        create_objective(
            objective_type="lagrange",
            penalty_type="CUSTOM",
            nodes="all_shooting",
            weight=1.0,
            arguments=[
                {"name": "function", "value": "custom_noncrossing_obj", "type": "function"},
                {"name": "test_arg", "value": -0.05, "type": "float"},
                {"name": "test_arg2", "value": 0.05, "type": "float"},
            ],
        )
    )

    return objectives


def collision_constraint_constraints(phase_name, model):
    constraints = []

    constraints.append(
        create_constraint(
            penalty_type="CUSTOM",
            nodes="all_shooting",
            weight=1.0,
            arguments=[
                {"name": "function", "value": "custom_noncrossing_const", "type": "function"},
                {"name": "test_arg", "value": -0.05, "type": "float"},
                {"name": "test_arg2", "value": 0.05, "type": "float"},
            ],
        )
    )

    return constraints
