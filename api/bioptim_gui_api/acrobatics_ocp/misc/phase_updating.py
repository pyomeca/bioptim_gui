import numpy as np

from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_data import AcrobaticsOCPData
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_utils import (
    acrobatics_phase_names,
    phase_name_to_info,
)
from bioptim_gui_api.acrobatics_ocp.misc.dynamics_updating import adapt_dynamics
from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.acrobatics_ocp.variables.variable_compute import get_variable_computer


def update_state_control_variables(phases: list[dict], data: dict) -> None:
    """
    Updates the state and control variables of the phases according to given data.
    Updates the dimension of the state and control variables.
    Updates the bounds and initial guess of the state and control variables.
    Updates the bounds interpolation type and initial guess interpolation type of the state and control variables.

    Parameters
    ----------
    phases: list[dict]
        The list of phases to update
    data: dict
        The data of the acrobatics
    """
    dynamics_control = {
        "torque_driven": "tau",
        "joints_acceleration_driven": "qddot_joints",
    }

    nb_somersaults = data["nb_somersaults"]
    half_twists = data["nb_half_twists"]
    prefer_left = data["preferred_twist_side"] == "left"
    position = data["position"]
    additional_criteria = AdditionalCriteria(
        with_visual_criteria=data["with_visual_criteria"],
        collision_constraint=data["collision_constraint"],
        with_spine=data["with_spine"],
    )
    phase_durations = [s["duration"] for s in phases]
    final_time = sum(phase_durations)
    is_forward = sum(half_twists) % 2 != 0

    model = get_variable_computer(position, additional_criteria)

    AcrobaticsOCPData.update_data("dof_names", model.dofs)

    nb_q = model.nb_q
    nb_qdot = model.nb_qdot
    nb_tau = model.nb_tau

    q_bounds = model.get_q_bounds(half_twists, prefer_left)
    nb_phases = len(q_bounds)
    qdot_bounds = model.get_qdot_bounds(nb_phases, final_time, is_forward)
    tau_bounds = model.get_tau_bounds(nb_phases)

    q_init = model.get_q_init(q_bounds=q_bounds)
    qdot_init = model.get_qdot_init(nb_somersaults, phase_durations, is_forward, nb_phases)
    tau_init = model.get_tau_init(nb_phases)

    for i, phase in enumerate(phases):
        phases[i]["state_variables"] = [
            {
                "name": "q",
                "dimension": nb_q,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": np.round(q_bounds[i]["min"], 2).tolist(),
                    "max_bounds": np.round(q_bounds[i]["max"], 2).tolist(),
                },
                "initial_guess_interpolation_type": "LINEAR",
                "initial_guess": np.round(q_init[i].T, 2).tolist(),
            },
            {
                "name": "qdot",
                "dimension": nb_qdot,
                "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
                "bounds": {
                    "min_bounds": np.round(qdot_bounds[i]["min"], 2).tolist(),
                    "max_bounds": np.round(qdot_bounds[i]["max"], 2).tolist(),
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": np.round(qdot_init[i], 2).tolist(),
            },
        ]
        phases[i]["control_variables"] = [
            {
                "name": dynamics_control[data["dynamics"]],
                "dimension": nb_tau,
                "bounds_interpolation_type": "CONSTANT",
                "bounds": {
                    "min_bounds": np.round(tau_bounds[i]["min"], 2).tolist(),
                    "max_bounds": np.round(tau_bounds[i]["max"], 2).tolist(),
                },
                "initial_guess_interpolation_type": "CONSTANT",
                "initial_guess": np.round(tau_init[i], 2).tolist(),
            },
        ]


def update_phase_info() -> list[dict]:
    """
    Update the phases_info of the acrobatics
    It will update the phase_name, duration and objectives and constraints according to the new phase names, the
    existing position, with_visual_criteria and collision_constraint.

    - Compute the phase names
    - The phase names are updated in the order they are given.
    - The new durations for each phase is calculated by dividing the final_time by the number of phases.
    - The phase's objectives and constraints are updated according to the new phase name, existing position, and
    additional criteria (with_visual_criteria and collision_constraint)


    Returns
    -------
    list[dict]
        The updated phases_info
    """
    data = AcrobaticsOCPData.read_data()

    nb_somersaults = data["nb_somersaults"]
    position = data["position"]
    half_twists = data["nb_half_twists"]
    final_time = data["final_time"]
    additional_criteria = AdditionalCriteria(
        with_visual_criteria=data["with_visual_criteria"],
        collision_constraint=data["collision_constraint"],
        with_spine=data["with_spine"],
    )
    dynamics = data["dynamics"]

    phase_names = acrobatics_phase_names(nb_somersaults, position, half_twists)
    n_phases = len(phase_names)
    new_phases = [phase_name_to_info(position, phase_names, i, additional_criteria) for i, _ in enumerate(phase_names)]

    for i in range(n_phases):
        new_phases[i]["phase_name"] = phase_names[i]
        # rounding is necessary to avoid buffer overflow in the frontend
        new_phases[i]["duration"] = round(final_time / n_phases, 2)

    update_state_control_variables(new_phases, data)

    for phase in new_phases:
        adapt_dynamics(phase, dynamics)

    AcrobaticsOCPData.update_data("nb_phases", n_phases)
    AcrobaticsOCPData.update_data("phases_info", new_phases)

    return new_phases
