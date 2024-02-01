import copy
import json

from bioptim_gui_api.variables.misc.variables_config import DefaultVariablesConfig


class GenericOCPData:
    datafile = "generic_ocp_data.json"

    default_phase_info = {
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
        "phases_info": [copy.deepcopy(default_phase_info)],
    }

    @classmethod
    def read_data(cls, key: str = None):
        """
        Read the data of the ocp store in a json file

        Parameters
        ----------
        key: str
            The key to read

        Returns
        -------
        The data or the value of the key, the whole data if key is None
        """
        with open(cls.datafile, "r") as f:
            data = json.load(f)
        return data if key is None else data[key]

    @classmethod
    def update_data(cls, key: str | None, value) -> None:
        """
        Update the data of the ocp store in a json file

        Parameters
        ----------
        key: str
            The key to update
        value: Any
            The value to put in the key

        Returns
        -------
        None
        """
        if key is not None:
            with open(cls.datafile, "r") as f:
                data = json.load(f)
            data[key] = value
        else:
            data = value

        with open(cls.datafile, "w") as f:
            json.dump(data, f)
