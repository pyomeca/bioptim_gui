import copy

from bioptim_gui_api.penalty.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.penalty_utils import create_objective, create_constraint
from bioptim_gui_api.variables.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)
from bioptim_gui_api.variables.tuck_acrobatics_variables import TuckAcrobaticsVariables


class DefaultAcrobaticsConfig:
    datafile = "acrobatics_data.json"

    default_phases_info = {
        "phase_name": None,
        "nb_shooting_points": 40,
        "duration": 1.0,
        "objectives": [
            create_objective(
                objective_type="lagrange",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                    "MINIMIZE_CONTROL"
                ],
                nodes="all_shooting",
                weight=1.0,
                arguments=[
                    {"name": "key", "value": "tau", "type": "string"},
                ],
            ),
            create_objective(
                objective_type="lagrange",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                    "MINIMIZE_CONTROL"
                ],
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


def phase_name_to_phase(position, phase_names: str, phase_index: int):
    # needed as there are nested list inside it
    # removing the deepcopy will cause issues on the objectives and constraints
    # some will be duplicated on all phases
    minimize_time_index = 2

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
        res["objectives"][minimize_time_index]["weight"] = 100.0
        res["objectives"][minimize_time_index]["penalty_type"] = "MINIMIZE_TIME"

        # Aim to put the hands on the lower legs to grab the pike position
        for side in "D", "G":
            res["objectives"].append(
                create_objective(
                    objective_type="mayer",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                        "SUPERIMPOSE_MARKERS"
                    ],
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
    elif phase_name == "Kick out":
        res["objectives"][minimize_time_index]["weight"] = 100.0
        res["objectives"][minimize_time_index]["penalty_type"] = "MINIMIZE_TIME"

        # Keeping the body alignment after kick out
        res["objectives"].append(
            create_objective(
                objective_type="lagrange",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                    "MINIMIZE_STATE"
                ],
                nodes="all_shooting",
                weight=50000.0,
                arguments=[
                    {"name": "key", "value": "q", "type": "str"},
                    {"name": "index", "value": model.XrotUpperLegs, "type": "list"},
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
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                        "MINIMIZE_STATE"
                    ],
                    nodes="all_shooting",
                    weight=50000.0,
                    arguments=[
                        {"name": "key", "value": "q", "type": "string"},
                        {"name": "index", "value": model.elbow_dofs, "type": "list"},
                    ],
                )
            )

        if phase_names[phase_index + 1] == "Landing":
            res["objectives"].append(
                create_objective(
                    objective_type="lagrange",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                        "MINIMIZE_STATE"
                    ],
                    nodes="all_shooting",
                    weight=50000.0,
                    arguments=[
                        {"name": "key", "value": "q", "type": "str"},
                        {"name": "index", "value": model.XrotUpperLegs, "type": "list"},
                    ],
                )
            )
    elif phase_name == "Somersault":
        res["objectives"][minimize_time_index]["weight"] = -0.01
        res["objectives"][minimize_time_index]["penalty_type"] = "MAXIMIZE_TIME"
        # quick kickout
        res["objectives"].append(
            create_objective(
                objective_type="lagrange",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                    "MINIMIZE_STATE"
                ],
                nodes="all_shooting",
                weight=50000.0,
                arguments=[
                    {"name": "key", "value": "q", "type": "str"},
                    {"name": "index", "value": model.XrotUpperLegs, "type": "int"},
                ],
            )
        )
        for side in "D", "G":
            res["constraints"].append(
                create_constraint(
                    penalty_type="SUPERIMPOSE_MARKERS",
                    nodes="all_shooting",
                    weight=1.0,
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
    elif phase_name == "Landing":
        res["objectives"][minimize_time_index]["weight"] = -0.01
        res["objectives"][minimize_time_index]["penalty_type"] = "MAXIMIZE_TIME"

        if position != "straight":
            res["objectives"].append(
                create_objective(
                    objective_type="lagrange",
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                        "MINIMIZE_STATE"
                    ],
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
                    penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                        "MINIMIZE_STATE"
                    ],
                    nodes="all_shooting",
                    weight=50000.0,
                    arguments=[
                        {"name": "key", "value": "q", "type": "str"},
                        {"name": "index", "value": model.XrotUpperLegs, "type": "int"},
                    ],
                )
            )

        # land safely
        res["objectives"].append(
            create_objective(
                objective_type="mayer",
                penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                    "MINIMIZE_STATE"
                ],
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
                penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                    "MINIMIZE_STATE"
                ],
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
                penalty_type=DefaultPenaltyConfig.original_to_min_dict[
                    "MINIMIZE_STATE"
                ],
                nodes="all",
                weight=100.0,
                arguments=[
                    {"name": "key", "value": "q", "type": "str"},
                    {"name": "index", "value": [model.Yrot], "type": "list"},
                ],
            )
        )

    return res
