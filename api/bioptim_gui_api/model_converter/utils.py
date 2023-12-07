from bioptim_gui_api.model_converter.converter import *


with_visual_segment_rotations = {"Head": "zx", "Eyes": "zx"}
with_visual_markers = (
    ["eyes_vect_start", "eyes_vect_end", "fixation_front", "fixation_center"]
    + [f"Trampo_corner_{n}" for n in range(1, 5)]
    + [f"cone_approx_{i}_{j}" for i in range(11) for j in range(10)]
)

non_collision_markers = [
    "HeadTop",
    "RightShoulder",
    "RightElbow",
    "RightKnuckle",
    "LeftShoulder",
    "LeftElbow",
    "LeftKnuckle",
    "PelvisBase",
    "Knee",
    "Ankle",
]


def get_converter(position: str = "straight", with_visual_criteria: bool = False, collision_constraint: bool = False):
    base_converters = {
        "straight": StraightConverter,
        "tuck": TuckConverter,
        "pike": PikeConverter,
    }

    base = base_converters[position]

    # copy necessary, or else it modifies the base class
    new_segment_rotation = base.segment_rotation.copy()
    new_segment_translation = base.segment_translation.copy()
    new_markers = base.markers.copy()

    if with_visual_criteria:
        new_segment_rotation.update(with_visual_segment_rotations)
        new_markers += with_visual_markers

    if collision_constraint:
        new_markers += non_collision_markers

    class SubConverter(BioModConverter):
        segment_rotation = new_segment_rotation
        segment_translation = new_segment_translation
        markers = new_markers

    return SubConverter
