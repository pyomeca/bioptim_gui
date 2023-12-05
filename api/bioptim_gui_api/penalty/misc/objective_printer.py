from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_printer import PenaltyPrinter
from bioptim_gui_api.utils.format_utils import arg_to_string


class ObjectivePrinter(PenaltyPrinter):
    def __init__(self, phase: int = 0, **kwargs):
        super().__init__(phase, **kwargs)
        self.objective_type = kwargs["objective_type"]
        self.weight = kwargs["weight"]
        self.arguments = kwargs["arguments"]

        self.penalty_type = (
            DefaultPenaltyConfig.min_to_original_dict[kwargs["penalty_type"]]
            if self.weight > 0
            else DefaultPenaltyConfig.max_to_original_dict[kwargs["penalty_type"]]
        )

    def _custom_str(self, indent: int = 8) -> str:
        assert self.penalty_type == "CUSTOM", "This function is only for custom penalty"
        assert len(self.arguments) == 1, "Custom penalty must have only one argument 'funtion'"
        assert self.arguments[0]["name"] == "function", "Custom penalty must have only one argument 'funtion'"

        ret = f"""{self.arguments[0]["value"]},
custom_type=ObjectiveFcn.{self.objective_type.capitalize()},\n"""
        ret += f"weight={self.weight},\n"

        return ret

    def _regular_str(self, indent: int = 8) -> str:
        ret = f"objective=ObjectiveFcn.{self.objective_type.capitalize()}.{self.penalty_type},\n"
        ret += f"weight={self.weight},\n"
        for argument in self.arguments:
            ret += f"{arg_to_string(argument)},\n"

        return ret

    def __common__args__(self, nb_phase: int = 1) -> str:
        ret = ""
        ret += f"node=Node.{self.nodes.upper()},\n"
        ret += f"quadratic={self.quadratic},\n"

        if not self.expand:
            ret += f"expand=False,\n"

        if self.target is not None:
            ret += f"target={self.target},\n"

        if self.derivative:
            ret += f"derivative=True,\n"

        if self.objective_type == "lagrange" and self.integration_rule != "rectangle_left":
            ret += f"integration_rule=QuadratureRule.{self.integration_rule.upper()},\n"

        if self.multi_thread:
            ret += f"multi_thread=True,\n"

        if nb_phase > 1:
            ret += f"phase={self.phase},\n"

        return ret

    def __str__(self, indent: int = 8, nb_phase: int = 1) -> str:
        space_indent = " " * indent
        if self.penalty_type == "CUSTOM":
            ret = self._custom_str(indent)
        else:
            ret = self._regular_str(indent)

        ret += self.__common__args__(nb_phase)

        # indent the whole string
        # strip to remove excess spaces at the end of the string
        ret = ret.replace("\n", "\n" + space_indent).strip(" ")

        return ret
