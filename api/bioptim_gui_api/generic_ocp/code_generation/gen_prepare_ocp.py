from bioptim_gui_api.generic_ocp.code_generation.bounds import BoundsGeneration
from bioptim_gui_api.penalty.misc.constraint_printer import ConstraintPrinter
from bioptim_gui_api.penalty.misc.objective_printer import ObjectivePrinter


class PrepareOCPGeneration:
    """
    This class is used to generate the prepare_ocp function
    """

    bounds_generation = BoundsGeneration

    @classmethod
    def prepare_ocp_header(cls) -> str:
        return """
def prepare_ocp()-> OptimalControlProgram:
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
    def generic_elements(cls, data: dict) -> str:
        nb_phases = data["nb_phases"]
        model_path = data["model_path"]
        phases = data["phases_info"]

        return f"""
    # Declaration of generic elements
    nb_phases = {nb_phases}
    bio_model = [BiorbdModel(r"{model_path}") for _ in range(nb_phases)]
    n_shooting = [{", ".join([str(s["nb_shooting_points"]) for s in phases])}]
    phase_time = [{", ".join([str(s["duration"]) for s in phases])}]
"""

    @classmethod
    def dynamics_str(cls, data) -> str:
        ret = f"""
    # Declaration of the dynamics function used during integration
    dynamics = DynamicsList()
"""

        for i, phase in enumerate(data["phases_info"]):
            ret += f"""
    dynamics.add(
        DynamicsFcn.{phase["dynamics"]},
        expand=True,
        phase={i},
    )
"""

        return ret

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
    def return_ocp(cls) -> str:
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
        constraints=constraints,
        objective_functions=objective_functions,
        use_sx=True,
    )
"""
        return ret

    @classmethod
    def prepare_ocp(cls, data: dict) -> str:
        ret = cls.prepare_ocp_header()
        ret += cls.generic_elements(data)
        ret += cls.penalties(data)
        ret += cls.dynamics_str(data)
        ret += cls.bounds_generation.bounds(data)
        ret += cls.return_ocp()
        return ret
