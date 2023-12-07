from bioptim_gui_api.acrobatics_ocp.misc.non_collision_cylinders.cylinder_collisions import get_collision_computer
from bioptim_gui_api.penalty.misc.penalty_utils import create_constraint, create_objective


def collision_constraint_objectives(phase_names: list[str], phase_index: int, position: str) -> list:
    objectives = []

    if phase_names[phase_index] == "Somersault":
        return objectives

    collision_computer = get_collision_computer(position)
    non_collisions_markers = collision_computer.non_collision_markers_combinations()

    for m1_1, m1_2, m2_1, m2_2 in non_collisions_markers:
        objectives.append(
            create_objective(
                objective_type="lagrange",
                penalty_type="CUSTOM",
                nodes="all_shooting",
                weight=1.0,
                arguments=[
                    {"name": "function", "value": "custom_noncrossing_obj", "type": "function"},
                    {
                        "name": "closestDistanceBetweenLines_func",
                        "value": "closestDistanceBetweenLines_func",
                        "type": "function",
                    },
                    {"name": "cylinder_1_1", "value": m1_1, "type": "str"},
                    {"name": "cylinder_1_2", "value": m1_2, "type": "str"},
                    {"name": "radius_1", "value": 0.05, "type": "float"},
                    {"name": "cylinder_2_1", "value": m2_1, "type": "str"},
                    {"name": "cylinder_2_2", "value": m2_2, "type": "str"},
                    {"name": "radius_2", "value": 0.05, "type": "float"},
                ],
            )
        )

    return objectives


def collision_constraint_constraints(phase_name, position):
    constraints = []

    if phase_name == "Somersault":
        return constraints

    collision_computer = get_collision_computer(position)
    non_collisions_markers = collision_computer.non_collision_markers_combinations()

    for m1_1, m1_2, m2_1, m2_2 in non_collisions_markers:
        constraints.append(
            create_constraint(
                penalty_type="CUSTOM",
                nodes="all_shooting",
                weight=1.0,
                arguments=[
                    {"name": "function", "value": "custom_noncrossing_const", "type": "function"},
                    {
                        "name": "closestDistanceBetweenLines_func",
                        "value": "closestDistanceBetweenLines_func",
                        "type": "function",
                    },
                    {"name": "cylinder_1_1", "value": m1_1, "type": "str"},
                    {"name": "cylinder_1_2", "value": m1_2, "type": "str"},
                    {"name": "radius_1", "value": 0.05, "type": "float"},
                    {"name": "cylinder_2_1", "value": m2_1, "type": "str"},
                    {"name": "cylinder_2_2", "value": m2_2, "type": "str"},
                    {"name": "radius_2", "value": 0.05, "type": "float"},
                ],
            )
        )

    return constraints
