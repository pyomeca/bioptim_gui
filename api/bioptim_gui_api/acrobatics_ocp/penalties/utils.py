from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.acrobatics_ocp.penalties.phases.collision_constraint import collision_constraint_constraints
from bioptim_gui_api.acrobatics_ocp.penalties.phases.common import common_objectives
from bioptim_gui_api.acrobatics_ocp.penalties.phases.kickout import kickout_objectives
from bioptim_gui_api.acrobatics_ocp.penalties.phases.landing import landing_objectives
from bioptim_gui_api.acrobatics_ocp.penalties.phases.pike_tuck import pike_tuck_objectives
from bioptim_gui_api.acrobatics_ocp.penalties.phases.somersault import somersault_objectives, somersault_constraints
from bioptim_gui_api.acrobatics_ocp.penalties.phases.twist import twist_objectives
from bioptim_gui_api.acrobatics_ocp.penalties.phases.waiting import waiting_objectives
from bioptim_gui_api.acrobatics_ocp.penalties.phases.with_spine import with_spine_objectives
from bioptim_gui_api.acrobatics_ocp.penalties.phases.with_visual_criteria import with_visual_criteria_objectives
from bioptim_gui_api.acrobatics_ocp.variables.variable_compute import get_variable_computer


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
        objectives += with_spine_objectives(phase_name, model)

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
