from bioptim_gui_api.acrobatics_ocp.penalties.non_collision_cylinders.cylinder_collisions import get_collision_computer
from bioptim_gui_api.penalty.misc.penalty_utils import create_constraint


def collision_constraint_constraints(phase_name, position):
    """
    CUSTOM custom_noncrossing_const all_shooting, weight=1.0
    """
    constraints = []

    if phase_name == "Somersault":
        return constraints

    collision_computer = get_collision_computer(position)
    non_collisions_markers = collision_computer.non_collision_markers_combinations()

    position_node = {
        "Pike": "all[3:]",
        "Tuck": "all[3:]",
        "Kick out": "all[:-3]",
    }

    for m1_1, m1_2, m2_1, m2_2 in non_collisions_markers:
        constraints.append(
            create_constraint(
                penalty_type="CUSTOM",
                nodes=position_node.get(phase_name, "all_shooting"),
                weight=1.0,
                arguments=[
                    {"name": "function", "value": "custom_noncrossing_const", "type": "function"},
                    {"name": "marker_1", "value": m1_1, "type": "str"},
                    {"name": "marker_2", "value": m1_2, "type": "str"},
                    {"name": "radius_1", "value": 0.05, "type": "float"},
                    {"name": "marker_3", "value": m2_1, "type": "str"},
                    {"name": "marker_4", "value": m2_2, "type": "str"},
                    {"name": "radius_2", "value": 0.05, "type": "float"},
                ],
            )
        )

    return constraints
