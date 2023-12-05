from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import create_constraint, create_objective


def somersault_objectives(phase_name: str, model, position: str) -> list:
    """
    MINIMIZE_STATE lagrange: q, shoulder_dofs, all_shooting, weight=50000.0
    MINIMIZE_STATE mayer: q, Yrot, all, weight=100.0
    """
    if "Somersault" not in phase_name:
        return []

    objectives = []

    objectives.append(
        create_objective(
            objective_type="lagrange",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="all_shooting",
            weight=50000.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {"name": "index", "value": model.shoulder_dofs, "type": "list"},
            ],
        )
    )
    # minimize wobbling
    objectives.append(
        create_objective(
            objective_type="mayer",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="all",
            weight=100.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {"name": "index", "value": [model.Yrot], "type": "list"},
            ],
        )
    )
    return objectives


def somersault_constraints(phase_name: str, model, position: str) -> list:
    """
    SUPERIMPOSE_MARKERS: all_shooting, weight=1.0, quadratic=False, MiddleRightHand, TargetRightHand
    SUPERIMPOSE_MARKERS: all_shooting, weight=1.0, quadratic=False, MiddleLeftHand, TargetLeftHand
    """
    if phase_name != "Somersault":
        return []

    constraints = []
    if position in ["pike", "tuck"]:
        for side in "Right", "Left":
            constraints.append(
                create_constraint(
                    penalty_type="SUPERIMPOSE_MARKERS",
                    nodes="all_shooting",
                    weight=1.0,
                    quadratic=False,
                    arguments=[
                        {"name": "min_bound", "value": -0.05, "type": "float"},
                        {"name": "max_bound", "value": 0.05, "type": "float"},
                        {
                            "name": "first_marker",
                            "value": f"Middle{side}Hand",
                            "type": "str",
                        },
                        {
                            "name": "second_marker",
                            "value": f"Target{side}Hand",
                            "type": "str",
                        },
                    ],
                )
            )
    return constraints
