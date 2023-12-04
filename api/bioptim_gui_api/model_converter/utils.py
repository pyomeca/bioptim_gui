from bioptim_gui_api.model_converter.converter import *


def get_converter(position: str = "straight", with_visual_criteria: bool = False):
    if with_visual_criteria:
        model = (
            StraightWithVisualConverter
            if position == "straight"
            else TuckWithVisualConverter
            if position == "tuck"
            else PikeWithVisualConverter
        )
    else:
        model = StraightConverter if position == "straight" else TuckConverter if position == "tuck" else PikeConverter
    return model
