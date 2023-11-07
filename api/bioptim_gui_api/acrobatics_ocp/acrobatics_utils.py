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


def add_somersault_info(n: int = 1) -> None:
    # rounding is necessary to avoid buffer overflow in the frontend
    if n < 1:
        raise ValueError("n must be positive")

    data = read_acrobatics_data()
    phases_info = data["phases_info"]
    before = len(phases_info)
    n_somersaults = before + n
    final_time = data["final_time"]
    for i in range(0, before):
        phases_info[i]["duration"] = round(final_time / n_somersaults, 2)

    for i in range(before, before + n):
        phases_info.append(config.DefaultAcrobaticsConfig.default_phases_info)
        data["nb_half_twists"].append(0)

        phases_info[i]["duration"] = round(final_time / n_somersaults, 2)

    data["phases_info"] = phases_info
    with open(config.DefaultAcrobaticsConfig.datafile, "w") as f:
        json.dump(data, f)


def remove_somersault_info(n: int = 0) -> None:
    if n < 0:
        raise ValueError("n must be positive")
    data = read_acrobatics_data()
    phases_info = data["phases_info"]
    before = len(phases_info)
    n_somersaults = before - n
    final_time = data["final_time"]
    for i in range(0, n_somersaults):
        phases_info[i]["duration"] = round(final_time / n_somersaults, 2)

    for _ in range(n):
        phases_info.pop()
        data["nb_half_twists"].pop()

    data["phases_info"] = phases_info
    with open(config.DefaultAcrobaticsConfig.datafile, "w") as f:
        json.dump(data, f)
