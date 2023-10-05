import json

import bioptim_gui_api.generic_ocp.generic_ocp_config as config


def update_generic_ocp_data(key: str, value) -> None:
    """
    Update the data of the generic ocp

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
    with open(config.DefaultGenericOCPConfig.datafile, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(config.DefaultGenericOCPConfig.datafile, "w") as f:
        json.dump(data, f)


def read_generic_ocp_data(key: str = None):
    """
    Read the data of the generic ocp

    Parameters
    ----------
    key: str
        The key to read

    Returns
    -------
    The data or the value of the key, the whole data if key is None
    """
    with open(config.DefaultGenericOCPConfig.datafile, "r") as f:
        data = json.load(f)
    return data if key is None else data[key]
