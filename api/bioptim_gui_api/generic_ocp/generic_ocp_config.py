from bioptim_gui_api.variables.variables_config import DefaultVariablesConfig


class DefaultGenericOCPConfig:
    datafile = "generic_ocp_data.json"

    default_phases_info = {
        "nb_shooting_points": 24,
        "duration": 1.0,
        "dynamics": "TORQUE_DRIVEN",
        "state_variables": DefaultVariablesConfig.default_torque_driven_variables[
            "state_variables"
        ].copy(),
        "control_variables": DefaultVariablesConfig.default_torque_driven_variables[
            "control_variables"
        ].copy(),
        "objectives": [],
        "constraints": [],
    }

    base_data = {
        "nb_phases": 1,
        "model_path": "",
        "phases_info": [default_phases_info.copy()],
    }
