from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import create_objective


def waiting_objectives(phase_name: str, model):
    """
    MINIMIZE_STATE lagrange: q, shoulder_dofs, all_shooting, weight=50000.0
    MINIMIZE_STATE lagrange: q, elbow_dofs, all_shooting, weight=50000.0
    MINIMIZE_STATE lagrange: q, legs_xdofs, all_shooting, weight=50000.0
    """
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

    objectives.append(
        create_objective(
            objective_type="lagrange",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="all_shooting",
            weight=50000.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {"name": "index", "value": model.elbow_dofs, "type": "list"},
            ],
        )
    )

    objectives.append(
        create_objective(
            objective_type="lagrange",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="all_shooting",
            weight=50000.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {"name": "index", "value": model.legs_xdofs, "type": "list"},
            ],
        )
    )

    return objectives
