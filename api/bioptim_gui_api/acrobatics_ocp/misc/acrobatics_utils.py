import json

import numpy as np

import bioptim_gui_api.acrobatics_ocp.misc.acrobatics_config as config


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


def update_phase_info(phase_names: list[str]) -> None:
    """
    Update the phases_info of the acrobatics, given a list of phase names
    It will update the phase_name, duration and objectives and constraints according to the new phase names, the
    existing position, with_visual_criteria and collision_constraint.

    - The phase names are updated in the order they are given.
    - The new durations for each phase is calculated by dividing the final_time by the number of phases.
    - The phase's objectives and constraints are updated according to the new phase name, existing position, and
    additional criteria (with_visual_criteria and collision_constraint)


    Parameters
    ----------
    phase_names: list[str]
        The new phase names

    Returns
    -------
    None
    """
    if len(phase_names) == 0:
        raise ValueError("n must be positive")

    data = read_acrobatics_data()

    n_phases = len(phase_names)
    final_time = data["final_time"]
    position = data["position"]
    additional_criteria = config.AdditionalCriteria(
        with_visual_criteria=data["with_visual_criteria"],
        collision_constraint=data["collision_constraint"],
    )

    new_phases = [
        config.phase_name_to_info(position, phase_names, i, additional_criteria) for i, _ in enumerate(phase_names)
    ]

    for i in range(n_phases):
        new_phases[i]["phase_name"] = phase_names[i]

    for i in range(0, n_phases):
        # rounding is necessary to avoid buffer overflow in the frontend
        new_phases[i]["duration"] = round(final_time / n_phases, 2)

    data["phases_info"] = new_phases
    with open(config.DefaultAcrobaticsConfig.datafile, "w") as f:
        json.dump(data, f)


def calculate_n_tuck(half_twists: list[int]) -> int:
    """
    Calculate the number of tuck/pike phases given the number of half twists in each somersault of the acrobatics

    The number of tuck/pike is at least 1 (acrobatics with no half twists whatsoever).
    A beginning or an ending half twist does impact the number of tuck/pike phases.
    But every somersault with a half twist in the middle will add a tuck/pike phase.

    Parameters
    ----------
    half_twists: list[int]
        The number of half twists for each phase

    Returns
    -------
    The number of tuck/pike phases in the acrobatics
    """
    return sum(np.array(half_twists[1:-1]) > 0) + 1


def acrobatics_phase_names(nb_somersaults: int, position: str, half_twists: list[int]) -> list[str]:
    """
    Calculate the phase names of the acrobatics

    Straight acrobatics: Somersault 1, Somersault 2, ..., Landing (The twists are done within the somersaults)
    Tuck/Pike acrobatics: Twist, Tuck/Pike, Somersault, Kick out, Twists, ..., Landing,
    (The phases names are computed with the same logic as in calculate_n_tuck)


    Parameters
    ----------
    nb_somersaults: int
        The number of somersaults in the acrobatics
    position: str
        The position of the acrobatics
    half_twists: list[int]
        The number of half twists for each phase

    Returns
    -------
    list[str]:
        The phase names of the acrobatics
    """
    if position == "straight":
        return [f"Somersault {i + 1}" for i in range(nb_somersaults)] + ["Landing"]

    n_tucks = calculate_n_tuck(half_twists)

    names = ["Twist"] if half_twists[0] > 0 else []
    names += [position.capitalize(), "Somersault", "Kick out", "Twist"] * n_tucks

    if half_twists[-1] == 0:
        names[-1] = "Waiting"

    names.append("Landing")
    return names
