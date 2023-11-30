from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.utils.format_utils import arg_to_string


class Objective:
    def __init__(self, phase: int = 0, **kwargs):
        self.phase = phase
        self.objective_type = kwargs["objective_type"]
        self.nodes = kwargs["nodes"]
        self.quadratic = kwargs["quadratic"]
        self.expand = kwargs["expand"]
        self.target = kwargs["target"]
        self.derivative = kwargs["derivative"]
        self.integration_rule = kwargs["integration_rule"]
        self.multi_thread = kwargs["multi_thread"]
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
{' ' * indent}custom_type=ObjectiveFcn.{self.objective_type.capitalize()},
"""

        return ret

    def _regular_str(self, indent: int = 8) -> str:
        ret = f"""objective=ObjectiveFcn.{self.objective_type.capitalize()}.{self.penalty_type},
"""
        for argument in self.arguments:
            ret += f"{' ' * indent}{arg_to_string(argument)},\n"

        return ret

    def __str__(self, indent: int = 8, nb_phase: int = 1) -> str:
        if self.penalty_type == "CUSTOM":
            ret = self._custom_str(indent)
        else:
            ret = self._regular_str(indent)

        ret += f"""{' ' * indent}node=Node.{self.nodes.upper()},
{' ' * indent}quadratic={self.quadratic},
{' ' * indent}weight={self.weight},
"""
        if not self.expand:
            ret += f"{' ' * indent}expand=False,\n"

        if self.target is not None:
            ret += f"{' ' * indent}target={self.target},\n"

        if self.derivative:
            ret += f"{' ' * indent}derivative=True,\n"

        if self.objective_type == "lagrange" and self.integration_rule != "rectangle_left":
            ret += f"{' ' * indent}integration_rule=QuadratureRule.{self.integration_rule.upper()},\n"

        if self.multi_thread:
            ret += f"{' ' * indent}multi_thread=True,\n"

        if nb_phase > 1:
            ret += f"{' ' * indent}phase={self.phase},\n"

        return ret
