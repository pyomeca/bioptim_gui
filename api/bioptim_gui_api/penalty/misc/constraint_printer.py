from bioptim_gui_api.penalty.misc.penalty_printer import PenaltyPrinter
from bioptim_gui_api.utils.format_utils import arg_to_string


class ConstraintPrinter(PenaltyPrinter):
    def __init__(self, phase: int = 0, **kwargs):
        super().__init__(phase=phase, **kwargs)
        self.arguments = kwargs["arguments"]

    def _custom_str(self) -> str:
        assert self.penalty_type == "CUSTOM", "This function should only be called for custom penalty"

        ret = None
        for argument in self.arguments:
            if argument["name"] == "function":
                ret = f"{argument['value']},\n"

        assert ret is not None, "The function argument is missing"

        for argument in self.arguments:
            if argument["name"] != "function":
                ret += f"{arg_to_string(argument)},\n"

        return ret

    def _regular_str(self) -> str:
        ret = f"constraint=ConstraintFcn.{self.penalty_type},\n"

        for argument in self.arguments:
            ret += f"{arg_to_string(argument)},\n"

        return ret

    def __str__(self, indent: int = 8, nb_phase: int = 1) -> str:
        space_indent = " " * indent

        if self.penalty_type == "CUSTOM":
            ret = self._custom_str()
        else:
            ret = self._regular_str()

        ret += self.__common__args__(nb_phase)

        # indent the whole string
        # strip to remove excess spaces at the end of the string
        ret = ret.replace("\n", "\n" + space_indent).strip(" ")

        return ret
