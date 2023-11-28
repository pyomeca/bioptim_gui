import copy

from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import (
    create_objective,
    create_constraint,
)
from bioptim_gui_api.variables.misc.pike_acrobatics_variables import (
    PikeAcrobaticsVariables,
)
from bioptim_gui_api.variables.misc.pike_with_visual_acrobatics_variables import (
    PikeAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.variables.misc.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)
from bioptim_gui_api.variables.misc.straight_with_visual_acrobatics_variables import (
    StraightAcrobaticsWithVisualVariables,
)
from bioptim_gui_api.variables.misc.tuck_acrobatics_variables import (
    TuckAcrobaticsVariables,
)
from bioptim_gui_api.variables.misc.tuck_with_visual_acrobatics_variables import (
    TuckAcrobaticsWithVisualVariables,
)


class DefaultAcrobaticsConfig:
    datafile = "acrobatics_data.json"

    default_phases_info = {
        "phase_name": None,
        "nb_shooting_points": 40,
        "duration": 1.0,
        "objectives": [
            create_objective(
                objective_type="lagrange",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_CONTROL"],
                nodes="all_shooting",
                weight=1.0,
                arguments=[
                    {"name": "key", "value": "tau", "type": "string"},
                ],
            ),
            create_objective(
                objective_type="lagrange",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_CONTROL"],
                nodes="all_shooting",
                weight=1.0,
                derivative=True,
                arguments=[
                    {"name": "key", "value": "tau", "type": "string"},
                ],
            ),
            create_objective(
                objective_type="mayer",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_TIME"],
                nodes="end",
                weight=1.0,
                arguments=[
                    {"name": "min_bound", "value": 0.0, "type": "float"},
                    {"name": "max_bound", "value": 100.0, "type": "float"},
                ],
            ),
        ],
        "constraints": [],
    }

    base_data = {
        "nb_somersaults": 1,
        "nb_half_twists": [0],
        "model_path": "",
        "final_time": 1.0,
        "final_time_margin": 0.1,
        "position": "straight",
        "sport_type": "trampoline",
        "preferred_twist_side": "left",
        "with_visual_criteria": False,
        "phases_info": [
            copy.deepcopy(default_phases_info),
            copy.deepcopy(default_phases_info),
        ],
    }
    base_data["phases_info"][0]["phase_name"] = "Somersault 1"
    base_data["phases_info"][1]["phase_name"] = "Landing"

    base_data["phases_info"][0]["objectives"].append(
        create_objective(
            objective_type="lagrange",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="all_shooting",
            weight=50000.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {
                    "name": "index",
                    "value": StraightAcrobaticsVariables.shoulder_dofs,
                    "type": "list",
                },
            ],
        )
    )
    base_data["phases_info"][0]["objectives"].append(
        create_objective(
            objective_type="mayer",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="all",
            weight=100.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {
                    "name": "index",
                    "value": [StraightAcrobaticsVariables.Yrot],
                    "type": "list",
                },
            ],
        )
    )

    # land safely
    base_data["phases_info"][1]["objectives"].append(
        create_objective(
            objective_type="mayer",
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
            nodes="end",
            weight=1000.0,
            arguments=[
                {"name": "key", "value": "q", "type": "str"},
                {
                    "name": "index",
                    "value": [StraightAcrobaticsVariables.Yrot],
                    "type": "list",
                },
            ],
        )
    )


def phase_name_to_phase(position, phase_names: str, phase_index: int, with_visual_criteria: bool = False):
    # needed as there are nested list inside it
    # removing the deepcopy will cause issues on the objectives and constraints
    # some will be duplicated on all phases
    minimize_time_index = 2

    model = PikeAcrobaticsVariables

    if with_visual_criteria:
        model = (
            StraightAcrobaticsWithVisualVariables
            if position == "straight"
            else TuckAcrobaticsWithVisualVariables
            if position == "tuck"
            else PikeAcrobaticsWithVisualVariables
        )
    else:
        model = (
            StraightAcrobaticsVariables
            if position == "straight"
            else TuckAcrobaticsVariables
            if position == "tuck"
            else PikeAcrobaticsVariables
        )

    res = copy.deepcopy(DefaultAcrobaticsConfig.default_phases_info)

    if position in ["pike", "tuck"]:
        res["objectives"][minimize_time_index]["weight"] = -0.01
        res["objectives"][minimize_time_index]["penalty_type"] = "MAXIMIZE_TIME"

    phase_name = phase_names[phase_index]
    res["phase_name"] = phase_name

    if phase_name in ["Pike", "Tuck"]:
        # minimize time weight is set to 100 for pike/tuck and kick out phase
        res["objectives"][minimize_time_index]["weight"] = 1000.0
        res["objectives"][minimize_time_index]["penalty_type"] = "MINIMIZE_TIME"

        # Aim to put the hands on the lower legs to grab the pike position
        for side in "D", "G":
            res["objectives"].append(
                create_objective(
                    objective_type="mayer",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict["SUPERIMPOSE_MARKERS"],
                    nodes="end",
                    weight=1.0,
                    arguments=[
                        {
                            "name": "first_marker",
                            "value": f"MidMain{side}",
                            "type": "string",
                        },
                        {
                            "name": "second_marker",
                            "value": f"CibleMain{side}",
                            "type": "string",
                        },
                    ],
                )
            )

        res["objectives"].append(
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
    elif phase_name == "Kick out":
        res["objectives"][minimize_time_index]["weight"] = 1000.0
        res["objectives"][minimize_time_index]["penalty_type"] = "MINIMIZE_TIME"
        # quick kickout
        res["objectives"].append(
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
        res["objectives"].append(
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
    elif phase_name == "Twist":
        res["objectives"][minimize_time_index]["weight"] = -0.01
        res["objectives"][minimize_time_index]["penalty_type"] = "MAXIMIZE_TIME"
        # if there is a twist before piking/tucking the minimize_time weight is set to 1
        if phase_index == 0:
            res["objectives"][minimize_time_index]["weight"] = 1.0
            res["objectives"][minimize_time_index]["penalty_type"] = "MINIMIZE_TIME"

        if position != "straight":
            res["objectives"].append(
                create_objective(
                    objective_type="lagrange",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
                    nodes="all_shooting",
                    weight=50000.0,
                    arguments=[
                        {"name": "key", "value": "q", "type": "string"},
                        {"name": "index", "value": model.elbow_dofs, "type": "list"},
                    ],
                )
            )
    elif phase_name == "Somersault":
        res["objectives"][minimize_time_index]["weight"] = -100.0
        res["objectives"][minimize_time_index]["penalty_type"] = "MAXIMIZE_TIME"
        for side in "D", "G":
            res["constraints"].append(
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
                            "value": f"MidMain{side}",
                            "type": "str",
                        },
                        {
                            "name": "second_marker",
                            "value": f"CibleMain{side}",
                            "type": "str",
                        },
                    ],
                )
            )
    elif phase_name == "Waiting":
        res["objectives"][minimize_time_index]["weight"] = -0.01
        res["objectives"][minimize_time_index]["penalty_type"] = "MAXIMIZE_TIME"

        res["objectives"].append(
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

        res["objectives"].append(
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

        res["objectives"].append(
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

    elif phase_name == "Landing":
        res["objectives"][minimize_time_index]["weight"] = -0.01
        res["objectives"][minimize_time_index]["penalty_type"] = "MAXIMIZE_TIME"

        if position != "straight":
            res["objectives"].append(
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
            res["objectives"].append(
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
        res["objectives"].append(
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

    if "Somersault" in phase_name:
        res["objectives"].append(
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
        res["objectives"].append(
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

    if with_visual_criteria:
        # FIRST AND LAST
        if phase_index == 0 or phase_index == len(phase_names) - 1:
            # Spotting
            res["objectives"].append(
                create_objective(
                    objective_type="lagrange",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_SEGMENT_VELOCITY"],
                    nodes="default",
                    weight=10.0,
                    arguments=[
                        {"name": "segment", "value": "Head", "type": "string"},
                    ],
                )
            )

        # ALL
        # Self-motion detection
        res["objectives"].append(
            create_objective(
                objective_type="lagrange",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
                nodes="default",
                weight=1.0,
                arguments=[
                    {"name": "key", "value": "qdot", "type": "string"},
                    {
                        "name": "index",
                        "value": [model.ZrotEyes, model.XrotEyes],
                        "type": "list",
                    },
                ],
            )
        )

        # Avoid extreme eye and neck angles
        for index, weight in [
            ([model.ZrotEyes, model.XrotEyes], 10.0),
            ([model.ZrotHead, model.XrotHead], 100.0),
        ]:
            res["objectives"].append(
                create_objective(
                    objective_type="lagrange",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_STATE"],
                    nodes="default",
                    weight=weight,
                    arguments=[
                        {"name": "key", "value": "q", "type": "string"},
                        {"name": "index", "value": index, "type": "list"},
                    ],
                )
            )

        # ALL BUT SOMERSAULT
        if "Somersault" not in phase_name:
            # Keeping the trampoline bed in the peripheral vision
            res["objectives"].append(
                create_objective(
                    objective_type="lagrange",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict["CUSTOM"],
                    nodes="all_shooting",
                    weight=100.0,
                    arguments=[
                        {
                            "name": "function",
                            "value": "custom_trampoline_bed_in_peripheral_vision",
                            "type": "function",
                        },
                    ],
                )
            )

        # LAST ONLY
        if phase_index == len(phase_names) - 1:
            # quiet eye
            res["objectives"].append(
                create_objective(
                    objective_type="lagrange",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict["TRACK_VECTOR_ORIENTATIONS_FROM_MARKERS"],
                    nodes="default",
                    weight=1.0,
                    arguments=[
                        {
                            "name": "vector_0_marker_0",
                            "value": "eyes_vect_start",
                            "type": "string",
                        },
                        {
                            "name": "vector_0_marker_1",
                            "value": "eyes_vect_end",
                            "type": "string",
                        },
                        {
                            "name": "vector_1_marker_0",
                            "value": "eyes_vect_start",
                            "type": "string",
                        },
                        {
                            "name": "vector_1_marker_1",
                            "value": "fixation_front",
                            "type": "string",
                        },
                    ],
                )
            )

        # SOMERSAULT ONLY

    return res
