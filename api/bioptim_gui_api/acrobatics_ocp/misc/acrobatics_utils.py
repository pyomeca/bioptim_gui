import copy
import json

import numpy as np

from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_data import AcrobaticsOCPData
from bioptim_gui_api.acrobatics_ocp.misc.dynamics_updating import adapt_dynamics
from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.acrobatics_ocp.penalties.utils import get_phase_objectives, get_phase_constraints


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


def phase_name_to_info(
    position, phase_names: list[str], phase_index: int, additional_criteria: AdditionalCriteria
) -> dict:
    """
    Returns the phase info for the given phase name, position and additional criteria

    Parameters
    ----------
    position: str
        The position of the acrobatics (e.g. "straight", "pike", "tuck")
    phase_names: list[str]
        The list of phase names (e.g. ["Somersault", "Landing", "Twist", ...])
    phase_index: int
        The index of the phase in the list of phase names, is used to get the phase name
        Some objectives depends on the index of the phase (First, last, ...)
    additional_criteria: AdditionalCriteria
        The additional criteria (e.g. with_visual_criteria, collision_constraint, without_cone)

    Returns
    -------
    dict
        The phase info (e.g. {phase_name, nb_shooting_points, objectives, constraints, ...})

    """
    phase_name = phase_names[phase_index]

    # need to deepcopy or else there will be unwanted modification due to addresses
    res = copy.deepcopy(AcrobaticsOCPData.default_phases_info)
    res["phase_name"] = phase_name

    res["objectives"] = get_phase_objectives(phase_names, phase_index, position, additional_criteria)
    res["constraints"] = get_phase_constraints(phase_name, position, additional_criteria)

    with open(AcrobaticsOCPData.datafile, "r") as f:
        dynamics = json.load(f)["dynamics"]

    adapt_dynamics(res, dynamics)

    return res
