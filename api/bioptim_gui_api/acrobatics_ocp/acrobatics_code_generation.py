from fastapi import APIRouter, HTTPException

from bioptim_gui_api.acrobatics_ocp.acrobatics_utils import read_acrobatics_data
from bioptim_gui_api.penalty.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.utils.format_utils import format_2d_array, arg_to_string
from bioptim_gui_api.variables.pike_acrobatics_variables import PikeAcrobaticsVariables
from bioptim_gui_api.variables.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)
from bioptim_gui_api.variables.tuck_acrobatics_variables import TuckAcrobaticsVariables
from multiprocessing import cpu_count

router = APIRouter()


@router.get("/generate_code", response_model=str)
def get_acrobatics_generated_code():
    data = read_acrobatics_data()
    nb_somersaults = data["nb_somersaults"]

    model_path = data["model_path"]
    if not model_path:
        raise HTTPException(status_code=400, detail="No model path provided")

    # TODO generate a file with the correct DoF with model_converter

    phases = data["phases_info"]
    half_twists = data["nb_half_twists"]
    total_half_twists = sum(half_twists)
    save_path = "save_path" # TODO

    position = data["position"]
    is_forward = (total_half_twists % 2) != 0
    side = data["preferred_twist_side"]
    prefer_left = side == "left"
    total_time = sum([s["duration"] for s in phases])

    acrobatics_variables = PikeAcrobaticsVariables
    if position == "straight":
        acrobatics_variables = StraightAcrobaticsVariables
    elif position == "tuck":
        acrobatics_variables = TuckAcrobaticsVariables

    q_bounds = acrobatics_variables.get_q_bounds(half_twists, prefer_left)
    nb_phases = len(q_bounds)

    q_init = acrobatics_variables.get_q_init(nb_phases, half_twists, prefer_left)

    qdot_bounds = acrobatics_variables.get_qdot_bounds(
        nb_phases, total_time, is_forward
    )

    qdot_init = acrobatics_variables.get_qdot_init()

    tau_bounds = acrobatics_variables.get_tau_bounds()
    tau_init = acrobatics_variables.get_tau_init()

    nb_q = acrobatics_variables.nb_q
    nb_tau = acrobatics_variables.nb_tau

    n_threads = cpu_count() - 2

    generated = """\"""This file was automatically generated using BioptimGUI version 0.0.1\"""

import os
import pickle as pkl
import sys

import numpy as np
from bioptim import (
    Axis,
    BiMappingList,
    BiorbdModel,
    BoundsList,
    ConstraintFcn,
    ConstraintList,
    DynamicsFcn,
    DynamicsList,
    InitialGuessList,
    InterpolationType,
    MagnitudeType,
    MultinodeConstraintFcn,
    MultinodeConstraintList,
    MultiStart,
    Node,
    ObjectiveFcn,
    ObjectiveList,
    OptimalControlProgram,
    QuadratureRule,
    Solution,
    Solver,
)

"""

    generated += """
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

    generated += f"""

    # Declaration of generic elements
    n_shooting = [{", ".join([str(s["nb_shooting_points"]) for s in phases])}]
    phase_time = [{", ".join([str(s["duration"]) for s in phases])}]
    nb_phases = {nb_phases}

    bio_model = [BiorbdModel(r"{model_path}") for _ in range(nb_phases)]
    # can't use * to have multiple, needs duplication

"""

    # OBJECTIVES/CONSTRAINTS

    generated += f"""
    # Declaration of the constraints and objectives of the ocp
    constraints = ConstraintList()
    objective_functions = ObjectiveList()
"""

    for i in range(nb_phases):
        for objective in phases[i]["objectives"]:
            weight = objective["weight"]
            penalty_type = (
                DefaultPenaltyConfig.min_to_original_dict[objective["penalty_type"]]
                if weight > 0
                else DefaultPenaltyConfig.max_to_original_dict[
                    objective["penalty_type"]
                ]
            )
            generated += f"""
    objective_functions.add(
        objective=ObjectiveFcn.{objective["objective_type"].capitalize()}.{penalty_type},
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
            if nb_phases > 1:
                generated += f"        phase={i},\n"

            generated += """    )
"""

        for constraint in phases[i]["constraints"]:
            generated += f"""
    constraints.add(
        constraint=ConstraintFcn.{constraint["penalty_type"]},
"""
            for argument in constraint["arguments"]:
                generated += f"        {arg_to_string(argument)},\n"

            generated += f"""        node=Node.{constraint["nodes"].upper()},
        quadratic={constraint["quadratic"]},
"""

            # we don't have constraints with arguments yet
            # for argument in constraint["arguments"]:
            #     generated += f"        {arg_to_string(argument)},\n"

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
            if nb_phases > 1:
                generated += f"        phase={i},\n"

            generated += """    )
"""

    # DYNAMICS

    generated += f"""
    # Declaration of the dynamics function used during integration
    dynamics = DynamicsList()
"""

    if nb_phases == 1:
        generated += f"""
    dynamics.add(
        DynamicsFcn.TORQUE_DRIVEN,
    )
"""
    else:
        generated += f"""
    for i in range(nb_phases):
        dynamics.add(
            DynamicsFcn.TORQUE_DRIVEN,
            phase=i,
        )
"""

    generated += f"""
    multinode_constraints = MultinodeConstraintList()
    multinode_constraints.add(
        MultinodeConstraintFcn.TRACK_TOTAL_TIME,
        nodes_phase=({", ".join([str(i) for i in range(nb_phases)])}),
        nodes=({", ".join(["Node.END" for _ in range(nb_phases)])}),
        min_bound={total_time} - 0.02,
        max_bound={total_time} + 0.02,
    )
"""

    # PATH CONSTRAINTS

    generated += f"""
    # Declaration of optimization variables bounds and initial guesses
    # Path constraint
    x_bounds = BoundsList()
    x_initial_guesses = InitialGuessList()

    u_bounds = BoundsList()
    u_initial_guesses = InitialGuessList()
"""

    n_phases = len(q_bounds)

    for i in range(n_phases):
        generated += f"""
    x_bounds.add(
        "q",
        min_bound={format_2d_array(q_bounds[i]["min"])},
        max_bound={format_2d_array(q_bounds[i]["max"])},
        interpolation=InterpolationType.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT,
        phase={i},
    )
"""

    for i in range(nb_phases):
        generated += f"""
    x_bounds.add(
        "qdot",
        min_bound={format_2d_array(qdot_bounds[i]["min"])},
        max_bound={format_2d_array(qdot_bounds[i]["max"])},
        interpolation=InterpolationType.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT,
        phase={i},
    )
"""

    for i in range(nb_phases):
        generated += f"""
    x_initial_guesses.add(
        "q",
        initial_guess={format_2d_array(q_init[i].T)},
        interpolation=InterpolationType.LINEAR,
        phase={i},
    )
"""
    generated += f"""
    x_initial_guesses.add(
        "qdot",
        initial_guess={qdot_init},
        interpolation=InterpolationType.CONSTANT,
    )
"""

    generated += f"""
    for phase in range(nb_phases):
        u_bounds.add(
            "tau",
            min_bound={tau_bounds["min"]},
            max_bound={tau_bounds["max"]},
            interpolation=InterpolationType.CONSTANT,
            phase=phase,
        )
"""

    generated += f"""
    u_initial_guesses.add(
        "tau",
        initial_guess={tau_init},
        interpolation=InterpolationType.CONSTANT,
    )
"""

    generated += f"""
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
    
            u_initial_guesses[i]["tau"].add_noise(
                bounds=u_bounds[i]["tau"],
                magnitude=0.2,
                magnitude_type=MagnitudeType.RELATIVE,
                n_shooting=n_shooting[i],
                seed=seed,
            )
"""

    generated += f"""
    mapping = BiMappingList()
    mapping.add(
        "tau",
        to_second=[None, None, None, None, None, None, {", ".join([str(i) for i in range(nb_tau)])}],
        to_first=[{", ".join([str(i + (nb_q - nb_tau)) for i in range(nb_tau)])}],
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
        constraints=constraints,
        multinode_constraints=multinode_constraints,
        n_threads=(1 if is_multistart else {n_threads}),
    )

def construct_filepath(save_path, seed):
    return f"{{save_path}}/acrobatics_{'_'.join(str(i) for i in half_twists)}_{side}_{position}_{{seed}}.pkl"

def save_results(
    sol: Solution,
    *combinatorial_parameters,
    **extra_parameters,
) -> None:
    \"""
    Callback of the post_optimization_callback, this can be used to save the results

    Parameters
    ----------
    sol: Solution
        The solution to the ocp at the current pool
    combinatorial_parameters:
        The current values of the combinatorial_parameters being treated
    extra_parameters:
        All the non-combinatorial parameters sent by the user
    \"""
    try:
        seed, is_multistart = combinatorial_parameters
    except:
        seed, is_multistart = 0, False

    save_folder = extra_parameters["save_folder"]
    
    with open(f"{{save_folder}}/log.txt", "a") as f:
        if sol.status != 0:
            f.write(f"{{seed}} DVG\\n")
            return # don't save the results if it didn't converge
        else:
            f.write(f"{{seed}} CVG\\n")

    file_path = construct_filepath(save_folder, seed)

    integrated = sol.integrate(merge_phases=True)
    unscaled_states, time_vector = integrated._states["unscaled"], integrated._time_vector

    to_save = {{
            "solution": sol,
            "unscaled_states": unscaled_states,
            "time_vector": time_vector,
    }}
    del sol.ocp

    with open(file_path, "wb") as file:
        pkl.dump(to_save, file)

def should_solve(*combinatorial_parameters, **extra_parameters):
    \"""
    Callback of the should_solve_callback, this allows the user to instruct bioptim

    Parameters
    ----------
    combinatorial_parameters:
        The current values of the combinatorial_parameters being treated
    extra_parameters:
        All the non-combinatorial parameters sent by the user
    \"""

    seed, is_multistart = combinatorial_parameters
    save_folder = extra_parameters["save_folder"]

    file_path = construct_filepath(save_folder, seed)
    return not os.path.exists(file_path)

def get_solver():
    solver = Solver.IPOPT(show_online_optim=False, show_options=dict(show_bounds=True))
    solver.set_linear_solver("ma57")
    solver.set_maximum_iterations(3000)
    solver.set_convergence_tolerance(1e-6)
    return solver

def prepare_multi_start(
    combinatorial_parameters: dict,
    save_folder: str = None,
    n_pools: int = 1,
) -> MultiStart:
    \"""
    The initialization of the multi-start
    \"""
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    return MultiStart(
        combinatorial_parameters=combinatorial_parameters,
        prepare_ocp_callback=prepare_ocp,
        post_optimization_callback=(save_results, {{"save_folder": save_folder}}),
        should_solve_callback=(should_solve, {{"save_folder": save_folder}}),
        solver=get_solver(),  # You cannot use show_online_optim with multi-start
        n_pools=n_pools,
    )

def main(is_multistart: bool = False, nb_seeds: int = 1):
    # --- Prepare the multi-start and run it --- #

    seed = [i for i in range(nb_seeds)]

    combinatorial_parameters = {{
        "seed": seed,
        "is_multistart": [is_multistart],
    }}

    save_folder = "{save_path}"

    if is_multistart:
        multi_start = prepare_multi_start(
            combinatorial_parameters=combinatorial_parameters,
            save_folder=save_folder,
            n_pools=2,
        )

        multi_start.solve()
    else:
        ocp = prepare_ocp()
        solver = get_solver()
        sol = ocp.solve(solver=solver)

        save_results(sol, save_folder=save_folder)


if __name__ == "__main__":
    is_multi = False
    nb_seeds = 1
    if len(sys.argv) > 2 and sys.argv[1] == "multistart":
        is_multi = True
        nb_seeds = int(sys.argv[2])

    main(is_multi, nb_seeds)   

"""

    return generated
