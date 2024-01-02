from bioptim_gui_api.acrobatics_ocp.variables.utils import BioptimVariable, var_bounds_list, var_initial_guess_list
from bioptim_gui_api.generic_ocp.code_generation.bounds import BoundsGeneration
from bioptim_gui_api.utils.format_utils import format_2d_array


class AcrobaticsGenerationBounds(BoundsGeneration):
    """
    This class is used to generate the bounds inside prepare_ocp of the acrobatics OCP.
    """

    @classmethod
    def add_q_bounds(cls, data: dict) -> str:
        phases = data["phases_info"]

        q_bounds = var_bounds_list(data, "q", BioptimVariable.STATE_VARIABLE)

        nb_phases = len(phases)

        ret = ""
        for i in range(nb_phases):
            ret += f"""
    x_bounds.add(
        "q",
        min_bound={format_2d_array(q_bounds[i]["min"])},
        max_bound={format_2d_array(q_bounds[i]["max"])},
        interpolation=InterpolationType.{q_bounds[i]["interpolation_type"]},
        phase={i},
    )
"""
        return ret

    @classmethod
    def add_qdot_bounds(cls, data: dict) -> str:
        phases = data["phases_info"]

        qdot_bounds = var_bounds_list(data, "qdot", BioptimVariable.STATE_VARIABLE)

        nb_phases = len(phases)

        ret = ""
        for i in range(nb_phases):
            ret += f"""
    x_bounds.add(
        "qdot",
        min_bound={format_2d_array(qdot_bounds[i]["min"])},
        max_bound={format_2d_array(qdot_bounds[i]["max"])},
        interpolation=InterpolationType.{qdot_bounds[i]["interpolation_type"]},
        phase={i},
    )
"""
        return ret

    @classmethod
    def add_q_init(cls, data: dict) -> str:
        phases = data["phases_info"]

        q_init = var_initial_guess_list(data, "q", BioptimVariable.STATE_VARIABLE)

        nb_phases = len(phases)

        ret = ""
        for i in range(nb_phases):
            ret += f"""
    x_initial_guesses.add(
        "q",
        initial_guess={format_2d_array(q_init[i]["initial_guess"])},
        interpolation=InterpolationType.{q_init[i]["interpolation_type"]},
        phase={i},
    )
"""
        return ret

    @classmethod
    def add_qdot_init(cls, data: dict) -> str:
        qdot = data["phases_info"][0]["state_variables"][1]
        qdot_init = qdot["initial_guess"]
        interpolation_type = qdot["initial_guess_interpolation_type"]

        return f"""
    x_initial_guesses.add(
        "qdot",
        initial_guess={qdot_init},
        interpolation=InterpolationType.{interpolation_type},
        phase=0,
    )
"""

    @classmethod
    def add_tau_bounds(cls, data: dict) -> str:
        control_var = data["phases_info"][0]["control_variables"][0]
        control_bounds = control_var["bounds"]
        control_name = control_var["name"]
        interpolation_type = control_var["bounds_interpolation_type"]

        return f"""
    for phase in range(nb_phases):
        u_bounds.add(
            "{control_name}",
            min_bound={control_bounds["min_bounds"]},
            max_bound={control_bounds["max_bounds"]},
            interpolation=InterpolationType.{interpolation_type},
            phase=phase,
        )
"""

    @classmethod
    def add_tau_init(cls, data: dict) -> str:
        control = data["phases_info"][0]["control_variables"][0]
        control_init = control["initial_guess"]
        interpolation_type = control["initial_guess_interpolation_type"]
        control_name = control["name"]

        return f"""
    u_initial_guesses.add(
        "{control_name}",
        initial_guess={control_init},
        interpolation=InterpolationType.{interpolation_type},
        phase=0,
    )
"""

    @classmethod
    def bounds(cls, data: dict) -> str:
        ret = cls.declare_bounds()
        ret += cls.add_q_bounds(data)
        ret += cls.add_qdot_bounds(data)
        ret += cls.add_tau_bounds(data)
        ret += cls.add_q_init(data)
        ret += cls.add_qdot_init(data)
        ret += cls.add_tau_init(data)
        return ret
