from bioptim_gui_api.variables.misc.variables_config import DefaultVariablesConfig


class DefaultGenericOCPConfig:
    """
    Default config for generic ocp

    Attributes
    ----------
    datafile: str
        The file name that will be used to store the data and in the endpoints(e.g. "generic_ocp_data.json")

    base_data: dict
        The base data at startup (e.g. {nb_phases, model_path, final_time, ...})
    """

    datafile = "generic_ocp_data.json"

    default_phases_info = {
        "nb_shooting_points": 24,
        "duration": 1.0,
        "dynamics": "TORQUE_DRIVEN",
        "state_variables": DefaultVariablesConfig.default_torque_driven_variables["state_variables"].copy(),
        "control_variables": DefaultVariablesConfig.default_torque_driven_variables["control_variables"].copy(),
        "objectives": [],
        "constraints": [],
    }

    base_data = {
        "nb_phases": 1,
        "model_path": "",
        "phases_info": [default_phases_info.copy()],
    }
