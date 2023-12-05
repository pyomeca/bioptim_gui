class PenaltyPrinter:
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

    def _expand_str(self) -> str:
        ret = ""
        if not self.expand:
            ret += f"expand=False,\n"
        return ret

    def _target_str(self) -> str:
        ret = ""
        if self.target is not None:
            ret += f"target={self.target},\n"
        return ret

    def _derivative_str(self) -> str:
        ret = ""
        if self.derivative:
            ret += f"derivative=True,\n"
        return ret

    def _integration_rule_str(self) -> str:
        ret = ""
        if self.integration_rule != "rectangle_left":
            ret += f"integration_rule=QuadratureRule.{self.integration_rule.upper()},\n"
        return ret

    def _multi_thread_str(self) -> str:
        ret = ""
        if self.multi_thread:
            ret += f"multi_thread=True,\n"
        return ret

    def _phase_str(self) -> str:
        ret = ""
        if self.phase > 0:
            ret += f"phase={self.phase},\n"
        return ret

    def __common__args__(self, nb_phase: int = 1) -> str:
        ret = ""
        ret += f"node=Node.{self.nodes.upper()},\n"
        ret += f"quadratic={self.quadratic},\n"
        ret += self._expand_str()
        ret += self._target_str()
        ret += self._derivative_str()
        ret += self._integration_rule_str()
        ret += self._multi_thread_str()
        ret += self._phase_str()

        return ret
