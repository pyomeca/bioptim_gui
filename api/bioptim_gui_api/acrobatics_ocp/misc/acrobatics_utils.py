import copy
import json

import numpy as np

import bioptim_gui_api.acrobatics_ocp.misc.models
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_data import AcrobaticsOCPData
from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.acrobatics_ocp.misc.penalties.collision_constraint import collision_constraint_constraints
from bioptim_gui_api.acrobatics_ocp.misc.penalties.common import common_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.kickout import kickout_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.landing import landing_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.pike_tuck import pike_tuck_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.somersault import somersault_objectives, somersault_constraints
from bioptim_gui_api.acrobatics_ocp.misc.penalties.twist import twist_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.waiting import waiting_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.with_spine import with_spine_objectives
from bioptim_gui_api.acrobatics_ocp.misc.penalties.with_visual_criteria import with_visual_criteria_objectives
from bioptim_gui_api.variables.misc.variables_config import get_variable_computer


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

    with open(AcrobaticsOCPData.datafile, "r") as f:
        data = json.load(f)

    n_phases = len(phase_names)

    final_time = data["final_time"]
    position = data["position"]
    additional_criteria = bioptim_gui_api.acrobatics_ocp.misc.models.AdditionalCriteria(
        with_visual_criteria=data["with_visual_criteria"],
        collision_constraint=data["collision_constraint"],
        with_spine=data["with_spine"],
    )

    new_phases = [phase_name_to_info(position, phase_names, i, additional_criteria) for i, _ in enumerate(phase_names)]

    for i in range(n_phases):
        new_phases[i]["phase_name"] = phase_names[i]

    for i in range(0, n_phases):
        # rounding is necessary to avoid buffer overflow in the frontend
        new_phases[i]["duration"] = round(final_time / n_phases, 2)

    control = "tau" if data["dynamics"] == "torque_driven" else "qddot_joints"
    for phase in new_phases:
        for objective in phase["objectives"]:
            for arguments in objective["arguments"]:
                if arguments["name"] == "key" and arguments["value"] in ["tau", "qddot_joints"]:
                    arguments["value"] = control

    AcrobaticsOCPData.update_data("nb_phases", n_phases)

    data["phases_info"] = new_phases
    with open(AcrobaticsOCPData.datafile, "w") as f:
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


def get_phase_objectives(
    phase_names: list[str], phase_index: int, position: str, additional_criteria: AdditionalCriteria
) -> list[dict]:
    """
    Returns the list of objectives for the given phase name, position and additional criteria

    Parameters
    ----------
    phase_names: list[str]
        The list of phase names (e.g. ["Somersault", "Landing", "Twist", ...])
    phase_index: int
        The index of the phase in the list of phase names, is used to get the phase name
        Some objectives depends on the index of the phase (First, last, ...)
    position: str
        The position of the acrobatics (e.g. "straight", "pike", "tuck")
    additional_criteria: AdditionalCriteria
        The additional criteria (e.g. with_visual_criteria, collision_constraint, without_cone)

    Returns
    -------
    list[dict]
        The list of objectives (e.g. [{penalty_type, nodes, target, arguments, weight, ...} ...])
    """
    with_visual_criteria = additional_criteria.with_visual_criteria
    with_spine = additional_criteria.with_spine

    phase_name = phase_names[phase_index]
    model = get_variable_computer(position, additional_criteria)

    objectives = common_objectives(
        phase_name=phase_names[phase_index], position=position, phase_index=phase_index, model=model
    )

    objectives += pike_tuck_objectives(phase_name, model, position)
    objectives += kickout_objectives(phase_name, model)
    objectives += twist_objectives(phase_name, model)
    objectives += waiting_objectives(phase_name, model)
    objectives += landing_objectives(phase_name, model, position)
    objectives += somersault_objectives(phase_name, model)

    if with_visual_criteria:
        objectives += with_visual_criteria_objectives(phase_names, phase_index, model)

    if with_spine:
        objectives += with_spine_objectives(model)

    return objectives


def get_phase_constraints(phase_name: str, position: str, additional_criteria: AdditionalCriteria) -> list[dict]:
    """
    Returns the list of constraints for the given phase name, position and additional criteria

    Parameters
    ----------
    phase_name: str
        The name of the phase (e.g. "Somersault", "Landing", "Twist", ...)
    position: str
        The position of the acrobatics (e.g. "straight", "pike", "tuck")
    additional_criteria: AdditionalCriteria
        The additional criteria (e.g. with_visual_criteria, collision_constraint, without_cone)

    Returns
    -------
    list[dict]
        The list of constraints (e.g. [{penalty_type, nodes, target, arguments, ...} ...])
    """
    collision_constraint = additional_criteria.collision_constraint

    constraints = []
    constraints += somersault_constraints(phase_name, position)

    if collision_constraint:
        constraints += collision_constraint_constraints(phase_name, position)

    return constraints


def adapt_dynamics(phases: dict, dynamics: str) -> None:
    old_control = "tau" if dynamics != "torque_driven" else "qddot_joints"
    new_control = "tau" if dynamics == "torque_driven" else "qddot_joints"

    for objective in phases["objectives"]:
        for arguments in objective["arguments"]:
            if arguments["name"] == "key" and arguments["value"] == old_control:
                arguments["value"] = new_control


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
