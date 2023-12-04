from bioptim_gui_api.model_converter.converter import *


def get_converter(position: str = "straight", with_visual_criteria: bool = False):
    if with_visual_criteria:
        if position == "straight":
            return StraightWithVisualConverter
        elif position == "tuck":
            return TuckWithVisualConverter
        elif position == "pike":
            return PikeWithVisualConverter
    else:
        if position == "straight":
            return StraightConverter
        elif position == "tuck":
            return TuckConverter
        elif position == "pike":
            return PikeConverter
