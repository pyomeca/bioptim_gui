from bioptim_gui_api.acrobatics_ocp.code_generation.bounds import AcrobaticsGenerationBounds
from bioptim_gui_api.utils.format_utils import indent_lines
from bioptim_gui_api.variables.misc.variables_config import DefaultVariablesConfig


class AcrobaticsGenerationBoundsNonCollision(AcrobaticsGenerationBounds):
    """
    This class is used to generate the bounds inside prepare_ocp of the acrobatics OCP.
    """

    @classmethod
    def add_q_init(cls, data: dict) -> str:
        ret = """
    if warming_up:
"""
        ret += indent_lines(super().add_q_init(data))
        return ret

    @classmethod
    def add_qdot_init(cls, data: dict) -> str:
        return indent_lines(super().add_qdot_init(data))

    @classmethod
    def add_tau_init(cls, data: dict) -> str:
        return indent_lines(super().add_tau_init(data))

    @classmethod
    def use_solution_as_initial_guess(cls, data: dict) -> str:
        control = DefaultVariablesConfig.dynamics_control[data["dynamics"]]
        return f"""
    if not warming_up:
        # use the solution of the warm up as initial guess
        with open(pkl_path, "rb") as file:
            sol = pkl.load(file)["solution"]
            for phase in range(nb_phases):
                q_init = sol.states[phase]["q"]
                qdot_init = sol.states[phase]["qdot"]
                tau_init = sol.controls[phase]["{control}"][:, :-1]

                x_initial_guesses.add(
                    "q",
                    initial_guess= q_init,
                    interpolation=InterpolationType.EACH_FRAME,
                    phase=phase,
                )

                x_initial_guesses.add(
                    "qdot",
                    initial_guess= qdot_init,
                    interpolation=InterpolationType.EACH_FRAME,
                    phase=phase,
                )

                u_initial_guesses.add(
                    "{control}",
                    initial_guess= tau_init,
                    interpolation=InterpolationType.EACH_FRAME,
                    phase=phase,
                )
"""

    @classmethod
    def bounds(cls, data: dict) -> str:
        ret = super().bounds(data)
        ret += cls.use_solution_as_initial_guess(data)
        return ret
