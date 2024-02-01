import numpy as np

from bioptim_gui_api.utils.format_utils import format_2d_array
from bioptim_gui_api.variables.misc.variables_config import DefaultVariablesConfig
from tests.acrobatics_ocp.code_generation.bounds import AcrobaticsGenerationBounds


class AcrobaticsGenerationBoundsNonCollision(AcrobaticsGenerationBounds):
    """
    This class is used to generate the bounds inside prepare_ocp of the acrobatics OCP.
    """

    @staticmethod
    def declare_bounds() -> str:
        return """
    # Declaration of optimization variables bounds and initial guesses
    # Path constraint
    x_bounds = BoundsList()
    x_initial_guesses = InitialGuessList()

    u_bounds = BoundsList()
    u_initial_guesses = InitialGuessList()
"""

    @staticmethod
    def add_q_bounds(data: dict, model) -> str:
        phases = data["phases_info"]
        half_twists = data["nb_half_twists"]
        prefer_left = data["preferred_twist_side"] == "left"

        nb_phases = len(phases)
        q_bounds = model.get_q_bounds(half_twists, prefer_left)

        ret = ""
        for i in range(nb_phases):
            ret += f"""
    x_bounds.add(
        "q",
        min_bound={format_2d_array(q_bounds[i]["min"])},
        max_bound={format_2d_array(q_bounds[i]["max"])},
        interpolation=InterpolationType.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT,
        phase={i},
    )
"""
        return ret

    @staticmethod
    def add_qdot_bounds(data: dict, model) -> str:
        phases = data["phases_info"]
        is_forward = sum(data["nb_half_twists"]) % 2 != 0

        nb_phases = len(phases)
        total_time = sum(s["duration"] for s in phases)
        qdot_bounds = model.get_qdot_bounds(nb_phases, total_time, is_forward)

        ret = ""
        for i in range(nb_phases):
            ret += f"""
    x_bounds.add(
        "qdot",
        min_bound={format_2d_array(qdot_bounds[i]["min"],)},
        max_bound={format_2d_array(qdot_bounds[i]["max"] )},
        interpolation=InterpolationType.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT,
        phase={i},
    )
"""
        return ret

    @staticmethod
    def add_tau_bounds(data: dict, model) -> str:
        nb_phases = data["nb_phases"]
        tau_bounds = model.get_tau_bounds(nb_phases)
        control = DefaultVariablesConfig.dynamics_control[data["dynamics"]]

        ret = ""
        for i in range(nb_phases):
            ret += f"""
    u_bounds.add(
        "{control}",
        min_bound={format_2d_array(tau_bounds[i]["min"] )},
        max_bound={format_2d_array(tau_bounds[i]["max"])},
        interpolation=InterpolationType.CONSTANT,
        phase={i},
    )
"""
        return ret

    @staticmethod
    def add_q_init(data: dict, model) -> str:
        phases = data["phases_info"]
        half_twists = data["nb_half_twists"]
        prefer_left = data["preferred_twist_side"] == "left"

        nb_phases = len(phases)
        q_init = model.get_q_init(half_twists, prefer_left)

        ret = """
    if warming_up:
"""
        for i in range(nb_phases):
            ret += f"""
        x_initial_guesses.add(
            "q",
            initial_guess={format_2d_array(q_init[i].T, 12)},
            interpolation=InterpolationType.LINEAR,
            phase={i},
        )
"""
        return ret

    @staticmethod
    def add_qdot_init(data: dict, model) -> str:
        phases = data["phases_info"]
        phase_durations = [s["duration"] for s in phases]
        nb_somersaults = data["nb_somersaults"]
        is_forward = sum(data["nb_half_twists"]) % 2 != 0
        nb_phases = data["nb_phases"]
        qdot_init = np.round(
            model.get_qdot_init(nb_somersaults, phase_durations, is_forward, nb_phases),
            2,
        )

        ret = ""
        for i in range(nb_phases):
            ret += f"""
        x_initial_guesses.add(
            "qdot",
            initial_guess={format_2d_array(qdot_init[i], 12)},
            interpolation=InterpolationType.CONSTANT,
            phase={i},
        )
"""
        return ret

    @staticmethod
    def add_tau_init(data: dict, model) -> str:
        nb_phases = data["nb_phases"]
        tau_init = model.get_tau_init(nb_phases)
        control = DefaultVariablesConfig.dynamics_control[data["dynamics"]]

        ret = ""
        for i in range(nb_phases):
            ret += f"""
        u_initial_guesses.add(
            "{control}",
            initial_guess={format_2d_array(tau_init[i], 12)},
            interpolation=InterpolationType.CONSTANT,
            phase={i},
        )
"""
        return ret

    @staticmethod
    def use_solution_as_initial_guess(data: dict) -> str:
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

    @staticmethod
    def bounds(data: dict, model) -> str:
        ret = AcrobaticsGenerationBoundsNonCollision.declare_bounds()
        ret += AcrobaticsGenerationBoundsNonCollision.add_q_bounds(data, model)
        ret += AcrobaticsGenerationBoundsNonCollision.add_qdot_bounds(data, model)
        ret += AcrobaticsGenerationBoundsNonCollision.add_tau_bounds(data, model)
        ret += AcrobaticsGenerationBoundsNonCollision.add_q_init(data, model)
        ret += AcrobaticsGenerationBoundsNonCollision.add_qdot_init(data, model)
        ret += AcrobaticsGenerationBoundsNonCollision.add_tau_init(data, model)
        ret += AcrobaticsGenerationBoundsNonCollision.use_solution_as_initial_guess(data)
        return ret
