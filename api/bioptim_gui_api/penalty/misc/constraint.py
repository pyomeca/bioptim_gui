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
        space_indent = " " * indent

        ret = f"constraint=ConstraintFcn.{self.penalty_type},\n"

        for argument in self.arguments:
            ret += f"{arg_to_string(argument)},\n"

        ret += f"node=Node.{self.nodes.upper()},\n"
        ret += f"quadratic={self.quadratic},\n"
        if not self.expand:
            ret += f"expand=False,\n"

        if self.target is not None:
            ret += f"target={self.target},\n"

        if self.derivative:
            ret += f"derivative=True,\n"

        if self.integration_rule != "rectangle_left":
            ret += f"integration_rule=QuadratureRule.{self.integration_rule.upper()},\n"

        if self.multi_thread:
            ret += f"multi_thread=True,\n"

        if nb_phase > 1:
            ret += f"phase={self.phase},\n"

        # indent the whole string
        # strip to remove excess spaces at the end of the string
        ret = ret.replace("\n", "\n" + space_indent).strip(" ")

        return ret
