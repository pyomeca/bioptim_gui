from fastapi import APIRouter

from bioptim_gui_api.acrobatics_ocp.acrobatics_utils import read_acrobatics_data

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


def arg_to_string(argument: dict) -> str:
    name, arg_type, value = argument["name"], argument["type"], argument["value"]
    if arg_type == "int" or arg_type == "float":
        return f"{name}={value}"
    else:
        return f'{name}="{value}"'


@router.get("/generate_code", response_model=str)
def get_acrobatics_generated_code():
    data = read_acrobatics_data()

    nb_somersaults = data["nb_somersaults"]
    model_path = data["model_path"]

    somersaults = data["somersaults_info"]
    total_half_twists = sum([s["nb_half_twists"] for s in somersaults])
    is_forward = (total_half_twists % 2) != 0
    prefer_left = data["preferred_twist_side"] == "left"
    total_time = sum([s["duration"] for s in somersaults])

    generated = """\"""This file was automatically generated using BioptimGUI version 0.0.1\"""

import pickle as pkl

import numpy as np
from bioptim import (
    Axis,
    BiorbdModel,
    ConstraintFcn,
    OptimalControlProgram,
    DynamicsList,
    DynamicsFcn,
    BoundsList,
    InitialGuessList,
    ObjectiveList,
    ObjectiveFcn,
    InterpolationType,
    BiMappingList,
    Solver,
    Node,
    QuadratureRule,
    ConstraintList,
)

"""

    generated += """
def prepare_ocp():
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

    generated += f"""
    
    # Declaration of generic elements
    n_shooting = [{", ".join([str(s["nb_shooting_points"]) for s in somersaults])}]
    phase_time = [{", ".join([str(s["duration"]) for s in somersaults])}]
    n_somersault = {nb_somersaults}
    n_half_twist = [{", ".join([str(s["nb_half_twists"]) for s in somersaults])}]

    bio_model = [BiorbdModel(r"{model_path}") for _ in range(n_somersault)]
    # can't use * to have multiple, needs duplication

"""

    generated += f"""
    # Declaration of the constraints and objectives of the ocp
    constraints = ConstraintList()
    objective_functions = ObjectiveList()
"""

    for i in range(nb_somersaults):
        for objective in somersaults[i]["objectives"]:
            generated += f"""
    objective_functions.add(
        objective=ObjectiveFcn.{objective["objective_type"].capitalize()}.{objective["penalty_type"]},
"""
            for argument in objective["arguments"]:
                generated += f"        {arg_to_string(argument)},\n"

            generated += f"""        node=Node.{objective["nodes"].upper()},
        quadratic={objective["quadratic"]},
        weight={objective["weight"]},
"""
            if not objective["expand"]:
                generated += "        expand = False,\n"
            if objective["target"] is not None:
                generated += f"        target = {objective['target']},\n"
            if objective["derivative"]:
                generated += "        derivative = True,\n"
            if (
                objective["objective_type"] == "lagrange"
                and objective["integration_rule"] != "rectangle_left"
            ):
                generated += f"        integration_rule = QuadratureRule.{objective['integration_rule'].upper()},\n"
            if objective["multi_thread"]:
                generated += "        multi_thread = True,\n"
            if nb_somersaults > 1:
                generated += f"        phase={i},\n"

            generated += """    )
"""

        for constraint in somersaults[i]["constraints"]:
            generated += f"""
    constraints.add(
        constraint=ConstraintFcn.{constraint["penalty_type"]},"""

            generated += f"""
        node=Node.{constraint["nodes"].upper()},
        quadratic={constraint["quadratic"]},
"""

            for argument in constraint["arguments"]:
                generated += f"        {arg_to_string(argument)},\n"

            if not constraint["expand"]:
                generated += "        expand = False,\n"
            if constraint["target"] is not None:
                generated += f"        target = {constraint['target']},\n"
            if constraint["derivative"]:
                generated += "        derivative = True,\n"
            if constraint["integration_rule"] != "rectangle_left":
                generated += f"        integration_rule = QuadratureRule.{constraint['integration_rule'].upper()},\n"
            if constraint["multi_thread"]:
                generated += "        multi_thread = True,\n"
            if nb_somersaults > 1:
                generated += f"        phase={i},\n"

            generated += """    )
"""

    generated += f"""
    # Declaration of the dynamics function used during integration
    dynamics = DynamicsList()
"""

    if nb_somersaults == 1:
        generated += f"""
    dynamics.add(
        DynamicsFcn.TORQUE_DRIVEN,
        expand=True,
    )
"""
    else:
        generated += f"""
    for i in range(n_somersault):
        dynamics.add(
            DynamicsFcn.TORQUE_DRIVEN,
            expand=True,
            phase=i,
        )
"""

    generated += f"""
    # Define control path constraint
    tau_min, tau_max, tau_init = -500, 500, 0

    n_q = bio_model[0].nb_q
    n_qdot = bio_model[0].nb_qdot
    n_tau = bio_model[0].nb_tau - bio_model[0].nb_root

    # Declaration of optimization variables bounds and initial guesses
    # Path constraint
    x_bounds = BoundsList()

    for phase in range(n_somersault):
        x_bounds.add("q", bio_model[phase].bounds_from_ranges("q"), phase=phase)
        x_bounds.add("qdot", bio_model[phase].bounds_from_ranges("qdot"), phase=phase)

    # Initial bounds
    x_bounds[0]["q"].min[:, 0] = [0] * n_q
    x_bounds[0]["q"].min[:3, 0] = -0.001
    x_bounds[0]["q"].min[[7, 9], 0] = 2.9, -2.9

    x_bounds[0]["q"].max[:, 0] = -x_bounds[0]["q"].min[:, 0]
    x_bounds[0]["q"].max[[7, 9], 0] = 2.9, -2.9

    intermediate_min_bounds = [
        -1,  # transX
        -1,  # transY
        -0.1,  # transZ
        0,  # somersault to adapt
        -np.pi / 4,  # tilt
        0,  # twist to adapt
        -0.65,  # right upper arm rotation Z
        -0.05,  # right upper arm rotation Y
        -2,  # left upper arm rotation Z
        -3,  # left upper arm rotation Y
    ]

    intermediate_max_bounds = [
        1,  # transX
        1,  # transY
        10,  # transZ
        0,  # somersault to adapt
        np.pi / 4,  # tilt
        0,  # twist to adapt
        2,  # right upper arm rotation Z
        3,  # right upper arm rotation Y
        0.65,  # left upper arm rotation Z
        0.05,  # left upper arm rotation Y
    ]

    for phase in range(n_somersault):
        if phase != 0:
            # initial bounds, same as final bounds of previous phase
            x_bounds[phase]["q"].min[:, 0] = x_bounds[phase - 1]["q"].min[:, 2]
            x_bounds[phase]["q"].max[:, 0] = x_bounds[phase - 1]["q"].max[:, 2]

        # Intermediate bounds, same for every phase
        x_bounds[phase]["q"].min[:, 1] = intermediate_min_bounds
        x_bounds[phase]["q"].min[3, 1] = {is_forward and '2 * np.pi * phase' or '-(2 * np.pi * (phase + 1))'}
        x_bounds[phase]["q"].min[5, 1] = {prefer_left and 'np.pi * sum(n_half_twist[:phase]) - 0.2' or 
                                          '-(np.pi * sum(n_half_twist[: phase + 1])) - 0.2'}

        x_bounds[phase]["q"].max[:, 1] = intermediate_max_bounds
        x_bounds[phase]["q"].max[3, 1] = {is_forward and '2 * np.pi * (phase + 1)' or '-(2 * np.pi * phase)'}
        x_bounds[phase]["q"].max[5, 1] = {prefer_left and 'np.pi * sum(n_half_twist[: phase + 1]) + 0.2' or 
                                          '-(np.pi * sum(n_half_twist[:phase])) + 0.2'}

        # Final bounds, used for next phase initial bounds
        x_bounds[phase]["q"].min[:, 2] = intermediate_min_bounds
        x_bounds[phase]["q"].min[3, 2] = {is_forward and '2 * np.pi * (phase + 1)' or '-2 * np.pi * (phase + 1)'}
        x_bounds[phase]["q"].min[5, 2] = {prefer_left and 'np.pi * sum(n_half_twist[: phase + 1]) - 0.2' or 
                                          '-(np.pi * sum(n_half_twist[: phase + 1])) - 0.2'}

        x_bounds[phase]["q"].max[:, 2] = intermediate_max_bounds
        x_bounds[phase]["q"].max[3, 2] = {is_forward and '2 * np.pi * (phase + 1)' or '-2 * np.pi * (phase + 1)'}
        x_bounds[phase]["q"].max[5, 2] = {prefer_left and 'np.pi * sum(n_half_twist[: phase + 1]) + 0.2' or 
                                          '-(np.pi * sum(n_half_twist[: phase + 1])) + 0.2'}

    # Final and last bounds
    x_bounds[n_somersault - 1]["q"].min[:, 2] = (
        np.array([-0.9, -0.9, 0, 0, 0, 2.9, 0, 0, 0, -2.9]) - 0.1
    )
    x_bounds[n_somersault - 1]["q"].min[3, 2] = {is_forward and '2 * np.pi * n_somersault - 0.1' or 
                                                 '-2 * np.pi * n_somersault - 0.1'}
    x_bounds[n_somersault - 1]["q"].min[5, 2] = {prefer_left and 'np.pi * sum(n_half_twist) - 0.1' or 
                                                 '-np.pi * sum(n_half_twist) - 0.1'}


    x_bounds[n_somersault - 1]["q"].max[:, 2] = np.array([0.9, 0.9, 0, 0, 0, 2.9, 0, 0, 0, -2.9]) + 0.1
    x_bounds[n_somersault - 1]["q"].max[3, 2] = {is_forward and '2 * np.pi * n_somersault + 0.1' or 
                                                 '-2 * np.pi * n_somersault + 0.1'}
    x_bounds[n_somersault - 1]["q"].max[5, 2] = {prefer_left and 'np.pi * sum(n_half_twist) + 0.1' or 
                                                 '-np.pi * sum(n_half_twist) + 0.1'}


    vzinit = (
        9.81 / 2 * {total_time}
    )  # vitesse initiale en z du CoM pour revenir a terre au temps final

    # Initial bounds
    x_bounds[0]["qdot"].min[:, 0] = [0] * n_qdot
    x_bounds[0]["qdot"].min[:2, 0] = -0.5
    x_bounds[0]["qdot"].min[2, 0] = vzinit - 2
    x_bounds[0]["qdot"].min[3, 0] = {is_forward and '0.5' or '-20'}


    x_bounds[0]["qdot"].max[:, 0] = -x_bounds[0]["qdot"].min[:, 0]
    x_bounds[0]["qdot"].max[2, 0] = vzinit + 2
    x_bounds[0]["qdot"].max[3, 0] = {is_forward and '20' or '-0.5'}


    for phase in range(n_somersault):
        if phase != 0:
            # initial bounds, same as final bounds of previous phase
            x_bounds[phase]["qdot"].min[:, 0] = x_bounds[phase - 1]["qdot"].min[:, 2]
            x_bounds[phase]["qdot"].max[:, 0] = x_bounds[phase - 1]["qdot"].max[:, 2]

        # Intermediate bounds
        x_bounds[phase]["qdot"].min[:, 1] = [-100] * n_qdot
        x_bounds[phase]["qdot"].min[:2, 1] = -10
        x_bounds[phase]["qdot"].min[3, 1] = {is_forward and '0.5' or '-20'}


        x_bounds[phase]["qdot"].max[:, 1] = [100] * n_qdot
        x_bounds[phase]["qdot"].max[:2, 1] = 10
        x_bounds[phase]["qdot"].max[3, 1] = {is_forward and '20' or '-0.5'}


        # Final bounds, same as intermediate
        x_bounds[phase]["qdot"].min[:, 2] = x_bounds[phase]["qdot"].min[:, 1]
        x_bounds[phase]["qdot"].max[:, 2] = x_bounds[phase]["qdot"].max[:, 1]

    x_inits = np.zeros((n_somersault, 2, n_q))

    x_inits[0] = np.array([0, 0, 0, 0, 0, 2.9, 0, 0, 0, -2.9])

    for phase in range(n_somersault):
        if phase != 0:
            x_inits[phase][0] = x_inits[phase - 1][1]

        x_inits[phase][1][3] = {is_forward and '2 * np.pi * (phase + 1)' or '-2 * np.pi * (phase + 1)'}


        x_inits[phase][1][5] = {prefer_left and 'np.pi * sum(n_half_twist[: phase + 1])' or 
                                '-np.pi * sum(n_half_twist[: phase + 1])'}


        x_inits[phase][1][[7, 9]] = 2.9, -2.9

    x_initial_guesses = InitialGuessList()

    for phase in range(n_somersault):
        x_initial_guesses.add(
            "q",
            initial_guess=x_inits[phase].T,
            interpolation=InterpolationType.LINEAR,
            phase=phase,
        )

    x_initial_guesses.add(
        "qdot",
        initial_guess=[0.0] * n_qdot,
        interpolation=InterpolationType.CONSTANT,
        phase=0,
    )

    u_bounds = BoundsList()
    for phase in range(n_somersault):
        u_bounds.add(
            "tau",
            min_bound=[tau_min] * n_tau,
            max_bound=[tau_max] * n_tau,
            interpolation=InterpolationType.CONSTANT,
            phase=phase,
        )

    u_initial_guesses = InitialGuessList()
    u_initial_guesses.add(
        "tau",
        initial_guess=[tau_init] * n_tau,
        interpolation=InterpolationType.CONSTANT,
    )

    mapping = BiMappingList()
    mapping.add(
        "tau",
        to_second=[None, None, None, None, None, None, 0, 1, 2, 3],
        to_first=[6, 7, 8, 9],
    )

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
        variable_mappings=mapping,
        use_sx=False,
        assume_phase_dynamics=True,
        constraints=constraints,
    )


if __name__ == "__main__":
    \"\"\"
    If this file is run, then it will perform the optimization
    
    \"\"\"

    # --- Prepare the ocp --- #
    ocp = prepare_ocp()

    solver = Solver.IPOPT()
    # --- Solve the ocp --- #
    sol = ocp.solve(solver=solver)

    out = sol.integrate(merge_phases=True)
    state, time_vector = out._states["unscaled"], out._time_vector

    save = {{
        "solution": sol,
        "unscaled_state": state,
        "time_vector": time_vector,
    }}

    del sol.ocp
    with open(f"somersault.pkl", "wb") as f:
        pkl.dump(save, f)
"""

    return generated
