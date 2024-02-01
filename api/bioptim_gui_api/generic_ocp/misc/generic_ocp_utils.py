import json

from bioptim_gui_api.generic_ocp.misc.generic_ocp_data import GenericOCPData


def add_phase_info(n: int = 1) -> None:
    if n < 1:
        raise ValueError("n must be positive")

    data = GenericOCPData.read_data()
    phases_info = data["phases_info"]
    before = len(phases_info)

    for _ in range(before, before + n):
        phases_info.append(GenericOCPData.default_phase_info)

    data["phases_info"] = phases_info
    with open(GenericOCPData.datafile, "w") as f:
        json.dump(data, f)


def remove_phase_info(n: int = 0) -> None:
    if n < 0:
        raise ValueError("n must be positive")
    data = GenericOCPData.read_data()
    phases_info = data["phases_info"]

    for _ in range(n):
        phases_info.pop()
    data["phases_info"] = phases_info
    with open(GenericOCPData.datafile, "w") as f:
        json.dump(data, f)
