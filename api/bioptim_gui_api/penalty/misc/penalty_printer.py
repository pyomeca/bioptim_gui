from bioptim_gui_api.utils.format_utils import arg_to_string


class PenaltyPrinter:
    """
    This class is used to generate the penalty inside prepare_ocp of the acrobatics OCP. (generated code)
    SHOULD NOT BE USED DIRECTLY.

    Attributes
    ----------
    phase: int
        The phase of the penalty.
    penalty_type: str
        The type of the penalty. (e.g. "CUSTOM", "MINIMIZE_STATE", ...)
    nodes: str
        The nodes of the penalty. (e.g. "END", "ALL", ...)
    quadratic: bool
        If the penalty is quadratic or not.
    expand: bool
        If the penalty is expand or not.
    target: list|None
        The target of the penalty.
    derivative: bool
        If the penalty is derivative or not.
    integration_rule: str
        The integration rule of the penalty.
    multi_thread: bool
        If the penalty is multi_thread or not.
    arguments: list
        The arguments of the penalty.
    """

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
        """
        This function is used to get the name of the function used in a CUSTOM penalty.

        Returns
        -------
        str|None
            The name of the function used in a CUSTOM penalty if it exists, None otherwise.
        """
        for argument in self.arguments:
            if argument["name"] == "function":
                return argument["value"]

        return None

    def _specific_custom_first_line(self) -> str:
        """
        This function is used to get the first lines of a CUSTOM penalty (e.g. "custom_function_name,")

        Returns
        -------
        str
            The first lines of a CUSTOM penalty.

        Raises
        ------
        AssertionError
            If the function argument is missing.
        """
        function_name = self._custom_function_name()
        assert function_name is not None, "The function argument is missing"

        return f"{function_name},\n"

    def _custom_str(self) -> str:
        """
        This function is used to get the string of a CUSTOM penalty without the common arguments.

        Returns
        -------
        str
            The string of a CUSTOM penalty.

        Raises
        ------
        AssertionError
            If the penalty type is not "CUSTOM".
        """
        assert self.penalty_type == "CUSTOM", "This function should only be called for custom penalty"

        ret = self._specific_custom_first_line()

        for argument in self.arguments:
            if argument["name"] != "function":
                ret += f"{arg_to_string(argument)},\n"

        return ret

    def _expand_str(self) -> str:
        """
        Expand argument is added to the string only if it not the default value (True).
        """
        ret = ""
        if not self.expand:
            ret += "expand=False,\n"
        return ret

    def _target_str(self) -> str:
        """
        Target argument is added to the string only if it not the default value (None).
        """
        ret = ""
        if self.target is not None:
            ret += f"target={self.target},\n"
        return ret

    def _derivative_str(self) -> str:
        """
        Derivative argument is added to the string only if it not the default value (False).
        """
        ret = ""
        if self.derivative:
            ret += "derivative=True,\n"
        return ret

    def _integration_rule_str(self) -> str:
        """
        Integration rule argument is added to the string only if it not the default value ("rectangle_left").
        """
        ret = ""
        if self.integration_rule != "rectangle_left":
            ret += f"integration_rule=QuadratureRule.{self.integration_rule.upper()},\n"
        return ret

    def _multi_thread_str(self) -> str:
        """
        Multi thread argument is added to the string only if it not the default value (False).
        """
        ret = ""
        if self.multi_thread:
            ret += "multi_thread=True,\n"
        return ret

    def _phase_str(self) -> str:
        """
        Phase argument is added to the string only if it not the default value (0).
        """
        ret = ""
        if self.phase > 0:
            ret += f"phase={self.phase},\n"
        return ret

    def __common__args__(self) -> str:
        """
        This function is used to get the common arguments of a penalty.
        """
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

    def _regular_str(self) -> str:
        return ""

    def stringify(self, indent: int = 8) -> str:
        """
        This function is used to get the string of a penalty.
        """
        space_indent = " " * indent
        if self.penalty_type == "CUSTOM":
            ret = self._custom_str()
        else:
            ret = self._regular_str()

        ret += self.__common__args__()

        # indent the whole string
        # strip to remove excess spaces at the end of the string
        ret = ret.replace("\n", "\n" + space_indent).strip(" ")

        return ret
