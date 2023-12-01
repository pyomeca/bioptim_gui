from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import create_objective


def landing_objectives(phase_name: str, model, position: str):
    """
    ONLY IN TUCK/PIKE:
        MINIMIZE_STATE lagrange: q, elbow_dofs, all_shooting, weight=50000.0
        MINIMIZE_STATE lagrange: q, legs_xdofs, all_shooting, weight=50000.0

    ALL:
        MINIMIZE_STATE mayer: q, Yrot, end, weight=1000.0
    """
    objectives = []
    if position != "straight":
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

        # Keeping the body alignement after kick out
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

    # land safely
    objectives.append(
        create_objective(
            objective_type="mayer",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="end",
            weight=1000.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {"name": "index", "value": [model.Yrot], "type": "list"},
            ],
        )
    )
    return objectives
