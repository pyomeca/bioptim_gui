import json

import bioptim_gui_api.acrobatics_ocp.acrobatics_config as config


def update_acrobatics_data(key: str, value) -> None:
    """
    Update the data of the acrobatics ocp

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
    with open(config.DefaultAcrobaticsConfig.datafile, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(config.DefaultAcrobaticsConfig.datafile, "w") as f:
        json.dump(data, f)


def read_acrobatics_data(key: str = None):
    """
    Read the data of the acrobatics ocp

    Parameters
    ----------
    key: str
        The key to read

    Returns
    -------
    The data or the value of the key, the whole data if key is None
    """
    with open(config.DefaultAcrobaticsConfig.datafile, "r") as f:
        data = json.load(f)
    return data if key is None else data[key]
