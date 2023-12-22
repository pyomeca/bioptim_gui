from bioptim_gui_api.utils.format_utils import format_2d_array


class AcrobaticsGenerationBounds:
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
        is_forward = data["position"] == "straight"

        nb_phases = len(phases)
        total_time = sum(s["duration"] for s in phases)
        qdot_bounds = model.get_qdot_bounds(nb_phases, total_time, is_forward)

        ret = ""
        for i in range(nb_phases):
            ret += f"""
    x_bounds.add(
        "qdot",
        min_bound={format_2d_array(qdot_bounds[i]["min"])},
        max_bound={format_2d_array(qdot_bounds[i]["max"])},
        interpolation=InterpolationType.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT,
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

        ret = ""
        for i in range(nb_phases):
            ret += f"""
    x_initial_guesses.add(
        "q",
        initial_guess={format_2d_array(q_init[i].T)},
        interpolation=InterpolationType.LINEAR,
        phase={i},
    )
"""
        return ret

    @staticmethod
    def add_qdot_init(data: dict, model) -> str:
        phases = data["phases_info"]
        final_time = sum(s["duration"] for s in phases)
        nb_somersaults = data["nb_somersaults"]
        qdot_init = model.get_qdot_init(nb_somersaults, final_time)

        return f"""
    x_initial_guesses.add(
        "qdot",
        initial_guess={qdot_init},
        interpolation=InterpolationType.CONSTANT,
        phase=0,
    )
"""

    @staticmethod
    def add_tau_bounds(data: dict, model) -> str:
        tau_bounds = model.get_tau_bounds()
        control = "tau" if data["dynamics"] == "TORQUE_DRIVEN" else "qddot_joints"

        return f"""
    for phase in range(nb_phases):
        u_bounds.add(
            "{control}",
            min_bound={tau_bounds["min"]},
            max_bound={tau_bounds["max"]},
            interpolation=InterpolationType.CONSTANT,
            phase=phase,
        )
"""

    @staticmethod
    def add_tau_init(data: dict, model) -> str:
        tau_init = model.get_tau_init()
        control = "tau" if data["dynamics"] == "TORQUE_DRIVEN" else "qddot_joints"

        return f"""
    u_initial_guesses.add(
        "{control}",
        initial_guess={tau_init},
        interpolation=InterpolationType.CONSTANT,
        phase=0,
    )
"""

    @staticmethod
    def bounds(data: dict, model) -> str:
        ret = AcrobaticsGenerationBounds.declare_bounds()
        ret += AcrobaticsGenerationBounds.add_q_bounds(data, model)
        ret += AcrobaticsGenerationBounds.add_qdot_bounds(data, model)
        ret += AcrobaticsGenerationBounds.add_q_init(data, model)
        ret += AcrobaticsGenerationBounds.add_qdot_init(data, model)
        ret += AcrobaticsGenerationBounds.add_tau_bounds(data, model)
        ret += AcrobaticsGenerationBounds.add_tau_init(data, model)
        return ret
