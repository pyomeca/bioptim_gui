from bioptim_gui_api.variables.misc.variables_config import DefaultVariablesConfig


def adapt_dynamics(phase: dict, dynamics: str) -> None:
    control_names = DefaultVariablesConfig.dynamics_control.values()
    control = DefaultVariablesConfig.dynamics_control[dynamics]

    for argument in objective_key_arguments_iterator(phase):
        if argument["value"] in control_names:
            argument["value"] = control

    for control_variable in phase["control_variables"]:
        if control_variable["name"] in control_names:
            control_variable["name"] = control


def objective_key_arguments_iterator(phase: dict) -> dict:
    """
    Iterates over the arguments of the objectives of the given phase

    Parameters
    ----------
    phase: dict
        The phase

    Yields
    -------
    dict
        The arguments of the objectives of the phase

    """
    for objective in phase["objectives"]:
        for argument in objective["arguments"]:
            if argument["name"] == "key":
                yield argument
