from multiprocessing import cpu_count

from bioptim_gui_api.acrobatics_ocp.code_generation.bounds_non_collision import (
    AcrobaticsGenerationBoundsNonCollision,
)
from bioptim_gui_api.acrobatics_ocp.code_generation.gen_prepare_ocp import AcrobaticsGenerationPrepareOCP
from bioptim_gui_api.penalty.misc.constraint_printer import ConstraintPrinter
from bioptim_gui_api.penalty.misc.objective_printer import ObjectivePrinter
from bioptim_gui_api.penalty.misc.penalty_utils import penalty_str_to_non_collision_penalty
from bioptim_gui_api.variables.misc.variables_config import DefaultVariablesConfig


class AcrobaticsGenerationPrepareOCPNonCollision(AcrobaticsGenerationPrepareOCP):
    """
    This class is used to generate the prepare_ocp function for non-collision acrobatics
    """

    bounds_generation = AcrobaticsGenerationBoundsNonCollision

    @classmethod
    def prepare_ocp_header(cls) -> str:
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

    @classmethod
    def penalties(cls, data: dict) -> str:
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

    @classmethod
    def multistart_noise(cls, data: dict) -> str:
        control = DefaultVariablesConfig.dynamics_control[data["dynamics"]]
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
            x_initial_guesses[i]["qdot"].add_noise(
                bounds=x_bounds[i]["qdot"],
                n_shooting=np.array(n_shooting[i])+1,
                magnitude=0.2,
                magnitude_type=MagnitudeType.RELATIVE,
                seed=seed,
            )
    
            u_initial_guesses[i]["{control}"].add_noise(
                bounds=u_bounds[i]["{control}"],
                n_shooting=np.array(n_shooting[i]),
                magnitude=0.2,
                magnitude_type=MagnitudeType.RELATIVE,
                seed=seed,
            )
"""

    @classmethod
    def return_ocp(cls, torque_driven: bool) -> str:
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
