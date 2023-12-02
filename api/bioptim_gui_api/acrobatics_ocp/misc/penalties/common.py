from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import (
    create_objective,
)


def common_objectives(
    default: bool = False, phase_name: str = None, position: str = "straight", phase_index: int = 0
) -> list:
    """
    Objectives that are common regardless of the phase and position

    MINIMIZE_CONTROL lagrange: tau, all_shooting, weight=1.0
    MINIMIZE_CONTROL lagrange: tau, derivative, all_shooting, weight=1.0
    MINIMIZE_TIME mayer:
    Straight: end, weight=1.0,
    Pike/Tuck:
    |--------|-------------|--------|-----------|------------|----------|----------|--------|
    | Phase  | Start Twist | Twist  | Pike/Tuck | Somersault | Kick-out | Waiting | Landing |
    |--------|-------------|--------|-----------|------------|----------|---------|---------|
    | weight |     1.0     |  -0.01 |    100k   |   -100     |   100k   |  -0.01  |  -0.01  |
    |--------|-------------|--------|-----------|------------|----------|---------|---------|

    """
    # only for tuck/pike acrobatics
    phase_name_to_minimize_time_weight = {
        "Twist": -0.01,
        "Pike": 100_000.0,
        "Tuck": 100_000.0,
        "Somersault": -100.0,
        "Kick out": 100_000.0,
        "Waiting": -0.01,
        "Landing": -0.01,
    }

    if default or position == "straight":
        weight = 1.0
    elif phase_index == 0 and phase_name == "Twist":
        weight = 1.0
    else:
        weight = phase_name_to_minimize_time_weight[phase_name]

    penalty_type = "MINIMIZE_TIME" if weight > 0 else "MAXIMIZE_TIME"

    objectives = []

    objectives.append(
        create_objective(
            objective_type="lagrange",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_CONTROL"],
            nodes="all_shooting",
            weight=1.0,
            arguments=[
                {"name": "key", "value": "tau", "type": "string"},
            ],
        )
    )
    objectives.append(
        create_objective(
            objective_type="lagrange",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_CONTROL"],
            nodes="all_shooting",
            weight=1.0,
            derivative=True,
            arguments=[
                {"name": "key", "value": "tau", "type": "string"},
            ],
        )
    )

    objectives.append(
        create_objective(
            objective_type="mayer",
            penalty_type=penalty_type,
            nodes="end",
            weight=weight,
            arguments=[
                {"name": "min_bound", "value": 0.1, "type": "float"},
                {"name": "max_bound", "value": 2.0, "type": "float"},
            ],
        )
    )

    return objectives
