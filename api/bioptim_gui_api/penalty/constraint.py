from bioptim_gui_api.utils.format_utils import arg_to_string


class Constraint:
    def __init__(self, phase: int = 0, **kwargs):
        self.phase = phase
        self.penalty_type = kwargs["penalty_type"]
        self.nodes = kwargs["nodes"]
        self.quadratic = kwargs["quadratic"]
        self.expand = kwargs["expand"]
        self.target = kwargs["target"]
        self.derivative = kwargs["derivative"]
        self.integration_rule = kwargs["integration_rule"]
        self.multi_thread = kwargs["multi_thread"]
        self.arguments = kwargs["arguments"]

    def __str__(self, indent: int = 8, nb_phase: int = 1) -> str:
        ret = f"""constraint=ConstraintFcn.{self.penalty_type},
"""
        for argument in self.arguments:
            ret += f"{' ' * indent}{arg_to_string(argument)},\n"

        ret += f"""{' ' * indent}node=Node.{self.nodes.upper()},
{' ' * indent}quadratic={self.quadratic},
"""
        if not self.expand:
            ret += f"{' ' * indent}expand=False,\n"
        if self.target is not None:
            ret += f"{' ' * indent}target={self.target},\n"
        if self.derivative:
            ret += f"{' ' * indent}derivative=True,\n"
        if self.integration_rule != "rectangle_left":
            ret += f"{' ' * indent}integration_rule=QuadratureRule.{self.integration_rule.upper()},\n"
        if self.multi_thread:
            ret += f"{' ' * indent}multi_thread=True,\n"
        if nb_phase > 1:
            ret += f"{' ' * indent}phase={self.phase},\n"

        return ret
