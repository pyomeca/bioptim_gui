from bioptim_gui_api.model_converter.converter import *


def get_converter(position: str = "straight", with_visual_criteria: bool = False):
    visual_converter = {
        "straight": StraightWithVisualConverter,
        "tuck": TuckWithVisualConverter,
        "pike": PikeWithVisualConverter,
    }

    non_visual_converter = {
        "straight": StraightConverter,
        "tuck": TuckConverter,
        "pike": PikeConverter,
    }

    if with_visual_criteria:
        return visual_converter[position]
    else:
        return non_visual_converter[position]
