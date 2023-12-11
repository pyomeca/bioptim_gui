from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_config import AdditionalCriteria
from bioptim_gui_api.model_converter.converter import *


def get_converter(position: str = "straight", additional_criteria: AdditionalCriteria = None) -> BioModConverter:
    """
    Get the converter class for the given position and additional criteria

    Converting a model means having:
    - the correct markers, segment rotations and translations according to the position

    + additional criteria combination:
    - the correct markers, segment rotations and translations according to with_visual_criteria (Eyes, cones, trampo)
    - the correct markers according to non-collision (cylinders)
    - the correct markers with_visual_criteria without the cones, to be able to make a front facing video without having
    the cone facing us

    Parameters
    ----------
    position: str
        The position of the acrobatics.

    additional_criteria: AdditionalCriteria
        The additional criteria of the acrobatics (visual criteria, collision constraint, without cone).

    Returns
    -------
    BioModConverter
        The converter class for the given position and additional criteria.
    """
    base_converters = {
        "straight": StraightConverter,
        "tuck": TuckConverter,
        "pike": PikeConverter,
    }

    with_visual_segment_rotations = {"Head": "zx", "Eyes": "zx"}
    with_visual_markers = ["eyes_vect_start", "eyes_vect_end", "fixation_front", "fixation_center"] + [
        f"Trampo_corner_{n}" for n in range(1, 5)
    ]
    cones = [f"cone_approx_{i}_{j}" for i in range(11) for j in range(10)]

    straight_collision_markers = ["HeadTop", "Ankle", "RightShoulder", "RightKnuckle", "LeftShoulder", "LeftKnuckle"]
    pike_collision_markers = straight_collision_markers + ["RightElbow", "LeftElbow", "PelvisBase"]
    tuck_collision_markers = pike_collision_markers + ["Knee"]

    collision_markers = {
        "straight": straight_collision_markers,
        "pike": pike_collision_markers,
        "tuck": tuck_collision_markers,
    }

    base = base_converters[position]

    # copy necessary, or else it modifies the base class
    new_segment_rotation = base.segment_rotation.copy()
    new_segment_translation = base.segment_translation.copy()
    new_markers = base.markers.copy()

    if additional_criteria.with_visual_criteria:
        new_segment_rotation.update(with_visual_segment_rotations)
        new_markers += with_visual_markers

        if not additional_criteria.without_cone:
            new_markers += cones

    if additional_criteria.collision_constraint:
        new_markers += collision_markers[position]

    class SubConverter(BioModConverter):
        segment_rotation = new_segment_rotation
        segment_translation = new_segment_translation
        markers = new_markers

    return SubConverter
