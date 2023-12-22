from multiprocessing import cpu_count

from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.penalty.misc.constraint_printer import ConstraintPrinter
from bioptim_gui_api.penalty.misc.objective_printer import ObjectivePrinter
from bioptim_gui_api.penalty.misc.penalty_utils import penalty_str_to_non_collision_penalty
from bioptim_gui_api.variables.misc.variables_config import get_variable_computer
from tests.acrobatics_ocp.misc.code_generation.bounds_non_collision import (
    AcrobaticsGenerationBoundsNonCollision,
)
from tests.acrobatics_ocp.misc.code_generation.gen_prepare_ocp import AcrobaticsGenerationPrepareOCP


class AcrobaticsGenerationPrepareOCPNonCollision(AcrobaticsGenerationPrepareOCP):
    """
    This class is used to generate the prepare_ocp function for non-collision acrobatics
    """

    @staticmethod
    def prepare_ocp_header() -> str:
        return """
def prepare_ocp(
    seed: int = 0,
    warming_up: bool = False,
    pkl_path: str = None,
)-> OptimalControlProgram:
    \"""
    This function build an optimal control program and instantiate it.
    It can be seen as a factory for the OptimalControlProgram class.

    Parameters
    ----------
    # TODO fill this section

    Returns
    -------
    The OptimalControlProgram ready to be solved
    \"""
"""

    @staticmethod
    def penalties(data: dict) -> str:
        phases = data["phases_info"]
        nb_phases = len(phases)
        ret = """
    # Declaration of the constraints and objectives of the ocp
    constraints = ConstraintList()
    objective_functions = ObjectiveList()
"""
        for i in range(nb_phases):
            for objective in phases[i]["objectives"]:
                objective_printer = ObjectivePrinter(i, **objective)
                stringified = objective_printer.stringify()
                if (
                    objective_printer.penalty_type != "CUSTOM"
                    or not objective_printer._custom_function_name().startswith("custom_noncrossing_")
                ):
                    ret += f"""
    objective_functions.add(
        {stringified}    )
"""
                else:
                    ret += f"""
    {penalty_str_to_non_collision_penalty(stringified)}
"""

            for constraint in phases[i]["constraints"]:
                constraint_printer = ConstraintPrinter(i, **constraint)
                stringified = constraint_printer.stringify()
                if (
                    constraint_printer.penalty_type != "CUSTOM"
                    or not constraint_printer._custom_function_name().startswith("custom_noncrossing_")
                ):
                    ret += f"""
    constraints.add(
        {ConstraintPrinter(i, **constraint).stringify()}    )
"""
                else:
                    ret += f"""
    {penalty_str_to_non_collision_penalty(stringified)}
"""
        return ret

    @staticmethod
    def multistart_noise(data: dict) -> str:
        dynamics = data["dynamics"]
        control = "tau" if dynamics == "torque_driven" else "qddot_joints"
        return f"""
    if warming_up:
        for i in range(nb_phases):
            x_initial_guesses[i]["q"].add_noise(
                bounds=x_bounds[i]["q"],
                n_shooting=np.array(n_shooting[i])+1,
                magnitude=0.2,
                magnitude_type=MagnitudeType.RELATIVE,
                seed=seed,
            )
        x_initial_guesses[0]["qdot"].add_noise(
            bounds=x_bounds[0]["qdot"],
            n_shooting=np.array(n_shooting[0])+1,
            magnitude=0.2,
            magnitude_type=MagnitudeType.RELATIVE,
            seed=seed,
        )

        u_initial_guesses[0]["{control}"].add_noise(
            bounds=u_bounds[0]["{control}"],
            magnitude=0.2,
            magnitude_type=MagnitudeType.RELATIVE,
            n_shooting=n_shooting[0],
            seed=seed,
        )
"""

    @staticmethod
    def bimapping(model) -> str:
        nb_q = model.nb_q
        nb_tau = model.nb_tau
        return f"""
    mapping = BiMappingList()
    mapping.add(
        "tau",
        to_second=[None, None, None, None, None, None, {", ".join([str(i) for i in range(nb_tau)])}],
        to_first=[{", ".join([str(i + (nb_q - nb_tau)) for i in range(nb_tau)])}],
    )
"""

    @staticmethod
    def return_ocp(torque_driven: bool) -> str:
        n_threads = cpu_count() - 2
        ret = f"""
    # Construct and return the optimal control program (OCP)
    return OptimalControlProgram(
        bio_model=bio_model,
        n_shooting=n_shooting,
        phase_time=phase_time,
        dynamics=dynamics,
        x_bounds=x_bounds,
        u_bounds=u_bounds,
        x_init=x_initial_guesses,
        u_init=u_initial_guesses,
        objective_functions=objective_functions,
"""
        if torque_driven:
            ret += "        variable_mappings=mapping,\n"

        ret += f"""        use_sx=False,
        constraints=constraints,
        multinode_constraints=multinode_constraints,
        n_threads={int(n_threads / 2)},
    )
"""
        return ret

    @staticmethod
    def prepare_ocp(data: dict, new_model_path: str) -> str:
        position = data["position"]
        torque_driven = data["dynamics"] == "torque_driven"
        additional_criteria = AdditionalCriteria(
            with_visual_criteria=data["with_visual_criteria"],
            collision_constraint=data["collision_constraint"],
            with_spine=data["with_spine"],
        )

        model = get_variable_computer(position, additional_criteria)

        ret = AcrobaticsGenerationPrepareOCPNonCollision.prepare_ocp_header()
        ret += AcrobaticsGenerationPrepareOCPNonCollision.generic_elements(data, new_model_path)
        ret += AcrobaticsGenerationPrepareOCPNonCollision.penalties(data)
        ret += AcrobaticsGenerationPrepareOCPNonCollision.dynamics_str(data)
        ret += AcrobaticsGenerationPrepareOCPNonCollision.multinode_constraints(data)
        ret += AcrobaticsGenerationBoundsNonCollision.bounds(data, model)
        ret += AcrobaticsGenerationPrepareOCPNonCollision.multistart_noise(data)
        if torque_driven:
            ret += AcrobaticsGenerationPrepareOCPNonCollision.bimapping(model)
        ret += AcrobaticsGenerationPrepareOCPNonCollision.return_ocp(torque_driven)
        return ret
