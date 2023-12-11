from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import create_objective


def spotting_objectives():
    # Spotting
    """
    MINIMIZE_SEGMENT_VELOCITY lagrange: Head, default, weight=10.0
    """
    return [
        create_objective(
            penalty_type=DefaultPenaltyConfig.original_to_min_dict["MINIMIZE_SEGMENT_VELOCITY"],
            weight=10.0,
            arguments=[
                {"name": "segment", "value": "Head", "type": "string"},
            ],
        )
    ]


def quiet_eye_objective():
    """
    TRACK_VECTOR_ORIENTATIONS_FROM_MARKERS lagrange: eyes_vect_start, eyes_vect_end, default, weight=1.0
    """
    # quiet eye
    return [
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
    ]


def with_visual_criteria_common_objectives(phase_name, model):
    """
    MINIMIZE_STATE lagrange: qdot, [ZrotEyes, XrotEyes], default, weight=1.0
    MINIMIZE_STATE lagrange: q, [ZrotEyes, XrotEyes], default, weight=10.0
    MINIMIZE_STATE lagrange: q, [ZrotHead, XrotHead], default, weight=100.0

    ALL_BUT_SOMERSAULT:
    CUSTOM lagrange: custom_trampoline_bed_in_peripheral_vision, all_shooting, weight=100.0
    """
    objectives = []
    # Self-motion detection
    objectives.append(
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
        objectives.append(
            create_objective(
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
        objectives.append(
            create_objective(
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
    return objectives


def with_visual_criteria_objectives(phase_names, phase_index, model):
    """
    FIRST_AND_LAST:
    MINIMIZE_SEGMENT_VELOCITY lagrange: Head, default, weight=10.0

    ALL:
    MINIMIZE_STATE lagrange: qdot, [ZrotEyes, XrotEyes], default, weight=1.0
    MINIMIZE_STATE lagrange: q, [ZrotEyes, XrotEyes], default, weight=10.0
    MINIMIZE_STATE lagrange: q, [ZrotHead, XrotHead], default, weight=100.0

    ALL_BUT_SOMERSAULT:
    CUSTOM lagrange: custom_trampoline_bed_in_peripheral_vision, all_shooting, weight=100.0

    LAST:
    TRACK_VECTOR_ORIENTATIONS_FROM_MARKERS lagrange: eyes_vect_start, eyes_vect_end, default, weight=1.0
    """
    objectives = []
    # FIRST AND LAST
    if phase_index in [0, len(phase_names) - 1]:
        objectives += spotting_objectives()

    # ALL
    objectives += with_visual_criteria_common_objectives(phase_names[phase_index], model)

    # LAST ONLY
    if phase_index == len(phase_names) - 1:
        objectives += quiet_eye_objective()

    return objectives
