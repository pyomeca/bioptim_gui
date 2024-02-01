from multiprocessing import cpu_count

from bioptim_gui_api.acrobatics_ocp.code_generation.bounds import AcrobaticsGenerationBounds
from bioptim_gui_api.penalty.misc.constraint_printer import ConstraintPrinter
from bioptim_gui_api.penalty.misc.objective_printer import ObjectivePrinter
from bioptim_gui_api.variables.misc.variables_config import DefaultVariablesConfig


class AcrobaticsGenerationPrepareOCP:
    """
    This class is used to generate the prepare_ocp function
    """

    bounds_generation = AcrobaticsGenerationBounds

    @classmethod
    def prepare_ocp_header(cls) -> str:
        return """
def prepare_ocp(
    seed: int = 0,
    is_multistart: bool = False,
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
    def generic_elements(cls, data: dict, new_model_path: str) -> str:
        phases = data["phases_info"]
        nb_phases = len(phases)

        return f"""
    # Declaration of generic elements
    n_shooting = [{", ".join([str(s["nb_shooting_points"]) for s in phases])}]
    phase_time = [{", ".join([str(s["duration"]) for s in phases])}]
    nb_phases = {nb_phases}

    bio_model = [BiorbdModel(r"{new_model_path}") for _ in range(nb_phases)]
    # can't use * to have multiple, needs duplication

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
                ret += f"""
    objective_functions.add(
        {ObjectivePrinter(i, **objective).stringify()}    )
"""

            for constraint in phases[i]["constraints"]:
                ret += f"""
    constraints.add(
        {ConstraintPrinter(i, **constraint).stringify()}    )
"""
        return ret

    @classmethod
    def dynamics_str(cls, data) -> str:
        dynamics = data["dynamics"].upper()
        return f"""
    # Declaration of the dynamics function used during integration
    dynamics = DynamicsList()

    for i in range(nb_phases):
        dynamics.add(
            DynamicsFcn.{dynamics},
            phase=i,
        )
"""

    @classmethod
    def multinode_constraints(cls, data) -> str:
        phases = data["phases_info"]
        nb_phases = len(phases)
        total_time = sum(s["duration"] for s in phases)
        final_time_margin = data["final_time_margin"]

        return f"""
    multinode_constraints = MultinodeConstraintList()
    multinode_constraints.add(
        MultinodeConstraintFcn.TRACK_TOTAL_TIME,
        nodes_phase=({", ".join([str(i) for i in range(nb_phases)])}),
        nodes=({", ".join(["Node.END" for _ in range(nb_phases)])}),
        min_bound={total_time} - {final_time_margin},
        max_bound={total_time} + {final_time_margin},
    )
"""

    @classmethod
    def multistart_noise(cls, data: dict) -> str:
        control = DefaultVariablesConfig.dynamics_control[data["dynamics"]]
        return f"""
    if is_multistart:
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
    def bimapping(cls, data: dict) -> str:
        nb_q = data["phases_info"][0]["state_variables"][0]["dimension"]
        nb_tau = data["phases_info"][0]["control_variables"][0]["dimension"]

        return f"""
    mapping = BiMappingList()
    mapping.add(
        "tau",
        to_second=[None, None, None, None, None, None, {", ".join([str(i) for i in range(nb_tau)])}],
        to_first=[{", ".join([str(i + (nb_q - nb_tau)) for i in range(nb_tau)])}],
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
        n_threads=({int(n_threads / 2)} if is_multistart else {n_threads}),
    )
"""
        return ret

    @classmethod
    def prepare_ocp(cls, data: dict, new_model_path: str) -> str:
        torque_driven = data["dynamics"] == "TORQUE_DRIVEN"

        ret = cls.prepare_ocp_header()
        ret += cls.generic_elements(data, new_model_path)
        ret += cls.penalties(data)
        ret += cls.dynamics_str(data)
        ret += cls.multinode_constraints(data)
        ret += cls.bounds_generation.bounds(data)
        ret += cls.multistart_noise(data)
        if torque_driven:
            ret += cls.bimapping(data)
        ret += cls.return_ocp(torque_driven)
        return ret
