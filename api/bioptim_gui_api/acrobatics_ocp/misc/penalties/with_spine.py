from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import create_objective


def with_spine_objectives(model):
    """
    PROPORTIONAL_CONTROL lagrange: qddot_joints, coef=1.0, all_shooting, weight=10.0
    on all phases, on all X,Y,Z joints of the spine
    """
    objectives = []

    x_pairs = [model.XrotStomach, model.XrotRib, model.XrotNipple, model.XrotShoulder]
    y_pairs = [model.YrotStomach, model.YrotRib, model.YrotNipple, model.YrotShoulder]
    z_pairs = [model.ZrotStomach, model.ZrotRib, model.ZrotNipple, model.ZrotShoulder]

    for pairs in [x_pairs, y_pairs, z_pairs]:
        for i, j in ((0, 1), (1, 2), (2, 3)):
            objectives.append(
                create_objective(
                    objective_type="lagrange",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict["PROPORTIONAL_CONTROL"],
                    nodes="all_shooting",
                    weight=10.0,
                    arguments=[
                        {"name": "key", "value": "qddot_joints", "type": "str"},
                        {"name": "first_dof", "value": pairs[i], "type": "int"},
                        {"name": "second_dof", "value": pairs[j], "type": "int"},
                        {"name": "coef", "value": 1.0, "type": "float"},
                    ],
                )
            )

    return objectives
