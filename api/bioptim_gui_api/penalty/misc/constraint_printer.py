from bioptim_gui_api.penalty.misc.penalty_printer import PenaltyPrinter
from bioptim_gui_api.utils.format_utils import arg_to_string


class ConstraintPrinter(PenaltyPrinter):
    def __init__(self, phase: int = 0, **kwargs):
        super().__init__(phase=phase, **kwargs)

    def _regular_str(self) -> str:
        ret = f"constraint=ConstraintFcn.{self.penalty_type},\n"

        for argument in self.arguments:
            ret += f"{arg_to_string(argument)},\n"

        return ret
