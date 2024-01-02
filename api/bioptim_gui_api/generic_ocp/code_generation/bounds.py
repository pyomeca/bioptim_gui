from bioptim_gui_api.acrobatics_ocp.variables.utils import BioptimVariable, var_bounds_list, var_initial_guess_list
from bioptim_gui_api.utils.format_utils import format_2d_array


class BoundsGeneration:
    """
    This class is used to generate the bounds inside prepare_ocp of the generic OCP.
    """

    @classmethod
    def declare_bounds(cls) -> str:
        return """
    # Declaration of optimization variables bounds and initial guesses
    # Path constraint
    x_bounds = BoundsList()
    x_initial_guesses = InitialGuessList()

    u_bounds = BoundsList()
    u_initial_guesses = InitialGuessList()
"""

    @classmethod
    def state_bounds(cls, data: dict) -> str:
        phases = data["phases_info"]
        state_variables_names = [state_variable["name"] for state_variable in phases[0]["state_variables"]]

        ret = ""

        for state_variable in state_variables_names:
            bounds = var_bounds_list(data, state_variable, BioptimVariable.STATE_VARIABLE)
            nb_phases = len(phases)
            for i in range(nb_phases):
                ret += f"""
    x_bounds.add(
        "{state_variable}",
        min_bound={format_2d_array(bounds[i]["min"])},
        max_bound={format_2d_array(bounds[i]["max"])},
        interpolation=InterpolationType.{bounds[i]["interpolation_type"]},
        phase={i},
    )
"""
        return ret

    @classmethod
    def control_bounds(cls, data: dict) -> str:
        phases = data["phases_info"]
        control_variables_names = [control_variable["name"] for control_variable in phases[0]["control_variables"]]

        ret = ""

        for control_variable in control_variables_names:
            bounds = var_bounds_list(data, control_variable, BioptimVariable.CONTROL_VARIABLE)
            nb_phases = len(phases)
            for i in range(nb_phases):
                ret += f"""
    u_bounds.add(
        "{control_variable}",
        min_bound={format_2d_array(bounds[i]["min"])},
        max_bound={format_2d_array(bounds[i]["max"])},
        interpolation=InterpolationType.{bounds[i]["interpolation_type"]},
        phase={i},
    )
"""
        return ret

    @classmethod
    def state_init_guess(cls, data: dict) -> str:
        phases = data["phases_info"]
        state_variables_names = [state_variable["name"] for state_variable in phases[0]["state_variables"]]

        ret = ""

        for state_variable in state_variables_names:
            init_guess = var_initial_guess_list(data, state_variable, BioptimVariable.STATE_VARIABLE)
            nb_phases = len(phases)
            for i in range(nb_phases):
                ret += f"""
    x_initial_guesses.add(
        "{state_variable}",
        initial_guess={format_2d_array(init_guess[i]["initial_guess"])},
        interpolation=InterpolationType.{init_guess[i]["interpolation_type"]},
        phase={i},
    )
"""
        return ret

    @classmethod
    def control_init_guess(cls, data: dict) -> str:
        phases = data["phases_info"]
        control_variable_names = [control_variable["name"] for control_variable in phases[0]["control_variables"]]

        ret = ""

        for control_variable in control_variable_names:
            init_guess = var_initial_guess_list(data, control_variable, BioptimVariable.CONTROL_VARIABLE)
            nb_phases = len(phases)
            for i in range(nb_phases):
                ret += f"""
    u_initial_guesses.add(
        "{control_variable}",
        initial_guess={format_2d_array(init_guess[i]["initial_guess"])},
        interpolation=InterpolationType.{init_guess[i]["interpolation_type"]},
        phase={i},
    )
"""
        return ret

    @classmethod
    def bounds(cls, data: dict) -> str:
        ret = cls.declare_bounds()
        ret += cls.state_bounds(data)
        ret += cls.control_bounds(data)
        ret += cls.state_init_guess(data)
        ret += cls.control_init_guess(data)
        return ret
