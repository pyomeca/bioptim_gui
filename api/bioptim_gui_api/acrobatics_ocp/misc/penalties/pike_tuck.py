from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import create_objective


def pike_tuck_objectives(phase_name: str, model) -> list:
    """
    SUPERIMPOSE_MARKERS mayer: MiddleRightHand, TargetRightHand, end, weight=1.0
    SUPERIMPOSE_MARKERS mayer: MiddleLeftHand, TargetLeftHand, end, weight=1.0
    MINIMIZE_STATE lagrange: q, elbow_dofs, all_shooting, weight=50000.0
    """
    # Aim to put the hands on the lower legs to grab the pike position
    if phase_name not in ["Pike", "Tuck"]:
        return []

    objectives = []
    for side in "Right", "Left":
        objectives.append(
            create_objective(
                objective_type="mayer",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict["SUPERIMPOSE_MARKERS"],
                nodes="end",
                weight=1.0,
                arguments=[
                    {
                        "name": "first_marker",
                        "value": f"Middle{side}Hand",
                        "type": "string",
                    },
                    {
                        "name": "second_marker",
                        "value": f"Target{side}Hand",
                        "type": "string",
                    },
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

    return objectives
