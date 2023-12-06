from bioptim_gui_api.utils.format_utils import arg_to_string


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
        self.arguments = kwargs["arguments"]

    def _custom_function_name(self) -> str:
        for argument in self.arguments:
            if argument["name"] == "function":
                return argument["value"]

        return None

    def _specific_custom_first_line(self) -> str:
        function_name = self._custom_function_name()
        assert function_name is not None, "The function argument is missing"

        return f"{function_name},\n"

    def _custom_str(self) -> str:
        assert self.penalty_type == "CUSTOM", "This function should only be called for custom penalty"

        ret = self._specific_custom_first_line()

        for argument in self.arguments:
            if argument["name"] != "function":
                ret += f"{arg_to_string(argument)},\n"

        return ret

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
