from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_printer import PenaltyPrinter
from bioptim_gui_api.utils.format_utils import arg_to_string


class ObjectivePrinter(PenaltyPrinter):
    """
    This class is used to generate the objective inside prepare_ocp of the acrobatics OCP. (generated code)

    Attributes
    ----------
    phase: int
        The phase of the objective.
    objective_type: str
        The type of the objective. (e.g. "LAGRANGE", "MAYER", ...)
    weight: float
        The weight of the objective.
    PenaltyPrinter attributes
    """

    def __init__(self, phase: int = 0, **kwargs):
        super().__init__(phase, **kwargs)
        self.objective_type = kwargs["objective_type"]
        self.weight = kwargs["weight"]

        self.penalty_type = (
            DefaultPenaltyConfig.min_to_original_dict[kwargs["penalty_type"]]
            if self.weight > 0
            else DefaultPenaltyConfig.max_to_original_dict[kwargs["penalty_type"]]
        )

    def _specific_custom_first_line(self) -> str:
        ret = super()._specific_custom_first_line()
        ret += f"custom_type=ObjectiveFcn.{self.objective_type.capitalize()},\n"
        ret += f"weight={self.weight},\n"
        return ret

    def _regular_str(self) -> str:
        """
        This function is used to get the string of the regular objective (non-CUSTOM).
        """
        ret = f"objective=ObjectiveFcn.{self.objective_type.capitalize()}.{self.penalty_type},\n"
        ret += f"weight={self.weight},\n"
        for argument in self.arguments:
            ret += f"{arg_to_string(argument)},\n"

        return ret

    def _integration_rule_str(self) -> str:
        """
        Objective specific integration rule, mayer objectives don't have integration rule argument.
        """
        ret = ""
        if self.objective_type == "lagrange" and self.integration_rule != "rectangle_left":
            ret += f"integration_rule=QuadratureRule.{self.integration_rule.upper()},\n"
        return ret
