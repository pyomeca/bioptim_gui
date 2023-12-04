from multiprocessing import cpu_count
from pathlib import Path

from fastapi import APIRouter, HTTPException

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_requests import CodeGenerationRequest
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_responses import CodeGenerationResponse
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_utils import read_acrobatics_data
from bioptim_gui_api.model_converter.utils import get_converter
from bioptim_gui_api.penalty.misc.constraint import Constraint
from bioptim_gui_api.penalty.misc.objective import Objective
from bioptim_gui_api.utils.format_utils import format_2d_array
from bioptim_gui_api.variables.misc.variables_utils import get_variable_computer

router = APIRouter()


@router.post("/generate_code", response_model=CodeGenerationResponse)
def get_acrobatics_generated_code(req: CodeGenerationRequest):
    data = read_acrobatics_data()
    with_visual_criteria = data["with_visual_criteria"]
    model_path = data["model_path"]
    position = data["position"]

    save_path = req.save_path
    save_folder = Path(save_path).parent
    original_filename = Path(model_path).name.split(".")[0]
    new_model_path = save_folder / f"{original_filename}-{position}.bioMod"

    if not model_path:
        raise HTTPException(status_code=400, detail="No model path provided")

    converter = get_converter(data["position"], with_visual_criteria)
    new_bio_model = converter.convert(model_path)

    phases = data["phases_info"]
    half_twists = data["nb_half_twists"]
    total_half_twists = sum(half_twists)

    is_forward = (total_half_twists % 2) != 0
    side = data["preferred_twist_side"]
    prefer_left = side == "left"
    total_time = sum([s["duration"] for s in phases])

    acrobatics_variables = get_variable_computer(position, with_visual_criteria)

    q_bounds = acrobatics_variables.get_q_bounds(half_twists, prefer_left)
    nb_phases = len(q_bounds)

    q_init = acrobatics_variables.get_q_init(half_twists, prefer_left)

    qdot_bounds = acrobatics_variables.get_qdot_bounds(nb_phases, total_time, is_forward)

    qdot_init = acrobatics_variables.get_qdot_init()

    tau_bounds = acrobatics_variables.get_tau_bounds()
    tau_init = acrobatics_variables.get_tau_init()

    nb_q = acrobatics_variables.nb_q
    nb_tau = acrobatics_variables.nb_tau

    n_threads = cpu_count() - 2

    generated = f"""\"""This file was automatically generated using BioptimGUI version 0.0.1\"""

import argparse
import os
import pickle as pkl
import casadi as cas
import time

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
    PenaltyController,
    QuadratureRule,
    Solution,
    Solver,
)

BIOMODEL_PATH = "{new_model_path}"

def custom_trampoline_bed_in_peripheral_vision(controller: PenaltyController) -> cas.MX:
    \"""
    This function aims to encourage the avatar to keep the trampoline bed in his peripheral vision.
    It is done by discretizing the vision cone into vectors and determining if the vector projection of the gaze are inside the trampoline bed.
    \"""

    a = 1.07  # Trampoline with/2
    b = 2.14  # Trampoline length/2
    n = 6  # order of the polynomial for the trampoline bed rectangle equation

    # Get the gaze vector
    eyes_vect_start_marker_idx = controller.model.marker_index(f'eyes_vect_start')
    eyes_vect_end_marker_idx = controller.model.marker_index(f'eyes_vect_end')
    gaze_vector = controller.model.markers(controller.states["q"].mx)[eyes_vect_end_marker_idx] - controller.model.markers(controller.states["q"].mx)[eyes_vect_start_marker_idx]

    point_in_the_plane = np.array([1, 2, -0.83])
    vector_normal_to_the_plane = np.array([0, 0, 1])
    obj = 0
    for i_r in range(11):
        for i_th in range(10):

            # Get this vector from the vision cone
            marker_idx = controller.model.marker_index(f'cone_approx_{{i_r}}_{{i_th}}')
            vector_origin = controller.model.markers(controller.states["q"].mx)[eyes_vect_start_marker_idx]
            vector_end = controller.model.markers(controller.states["q"].mx)[marker_idx]
            vector = vector_end - vector_origin

            # Get the intersection between the vector and the trampoline plane
            t = (cas.dot(point_in_the_plane, vector_normal_to_the_plane) - cas.dot(vector_normal_to_the_plane, vector_origin)) / cas.dot(
                vector, vector_normal_to_the_plane
            )
            point_projection = vector_origin + vector * cas.fabs(t)

            # Determine if the point is inside the trampoline bed
            # Rectangle equation : (x/a)**n + (y/b)**n = 1
            # The function is convoluted with tanh to make it:
            # 1. Continuous
            # 2. Not encourage to look to the middle of the trampoline bed
            # 3. Largely penalized when outside the trampoline bed
            # 4. Equaly penalized when looking upward
            obj += cas.tanh(((point_projection[0]/a)**n + (point_projection[1]/b)**n) - 1) + 1

    val = cas.if_else(gaze_vector[2] > -0.01, 2*10*11,
                cas.if_else(cas.fabs(gaze_vector[0]/gaze_vector[2]) > np.tan(3*np.pi/8), 2*10*11,
                            cas.if_else(cas.fabs(gaze_vector[1]/gaze_vector[2]) > np.tan(3*np.pi/8), 2*10*11, obj)))
    out = controller.mx_to_cx("peripheral_vision", val, controller.states["q"])

    return out

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

    bio_model = [BiorbdModel(r"{new_model_path}") for _ in range(nb_phases)]
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
            generated += f"""
    objective_functions.add(
        {Objective(i, **objective).__str__(nb_phase=nb_phases)}    )
"""

        for constraint in phases[i]["constraints"]:
            generated += f"""
    constraints.add(
        {Constraint(i, **constraint).__str__(nb_phase=nb_phases)}    )
"""

    # DYNAMICS

    generated += f"""
    # Declaration of the dynamics function used during integration
    dynamics = DynamicsList()

    for i in range(nb_phases):
        dynamics.add(
            DynamicsFcn.TORQUE_DRIVEN,
            phase=i,
        )

    multinode_constraints = MultinodeConstraintList()
    multinode_constraints.add(
        MultinodeConstraintFcn.TRACK_TOTAL_TIME,
        nodes_phase=({", ".join([str(i) for i in range(nb_phases)])}),
        nodes=({", ".join(["Node.END" for _ in range(nb_phases)])}),
        min_bound={total_time} - 0.02,
        max_bound={total_time} + 0.02,
    )
    
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
        phase=0,
    )

    for phase in range(nb_phases):
        u_bounds.add(
            "tau",
            min_bound={tau_bounds["min"]},
            max_bound={tau_bounds["max"]},
            interpolation=InterpolationType.CONSTANT,
            phase=phase,
        )

    u_initial_guesses.add(
        "tau",
        initial_guess={tau_init},
        interpolation=InterpolationType.CONSTANT,
        phase=0,
    )

    if is_multistart:
        for i in range(nb_phases):
            x_initial_guesses[i]["q"].add_noise(
                bounds=x_bounds[i]["q"],
                n_shooting=np.array(n_shooting[i])+1,
                magnitude=0.2,
                magnitude_type=MagnitudeType.RELATIVE,
                seed=seed,
            )
        x_initial_guesses[0]["qdot"].add_noise(
            bounds=x_bounds[0]["qdot"],
            n_shooting=np.array(n_shooting[0])+1,
            magnitude=0.2,
            magnitude_type=MagnitudeType.RELATIVE,
            seed=seed,
        )

        u_initial_guesses[0]["tau"].add_noise(
            bounds=u_bounds[0]["tau"],
            magnitude=0.2,
            magnitude_type=MagnitudeType.RELATIVE,
            n_shooting=n_shooting[0],
            seed=seed,
        )
        
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
        n_threads=({int(n_threads / 2)} if is_multistart else {n_threads}),
    )

def construct_filepath(save_path, seed = 0):
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
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    
    with open(f"{{save_folder}}/log.txt", "a") as f:
        if sol.status != 0:
            f.write(f"{{seed}} DVG\\n")
            return # don't save the results if it didn't converge
        else:
            f.write(f"{{seed}} CVG\\n")

    file_path = construct_filepath(save_folder, seed)

    integrated = sol.integrate(merge_phases=True)
    integrated_states, time_vector = integrated._states["unscaled"], integrated._time_vector
    
    time_parameters = sol.parameters["time"]
    fps = 25
    n_frames = [round(time_parameters[i][0] * fps) for i in range(len(time_parameters))]
    interpolated_states = sol.interpolate(n_frames).states

    to_save = {{
            "solution": sol,
            "integrated_states": integrated_states,
            "time_vector": time_vector,
            "interpolated_states": interpolated_states,
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

    return MultiStart(
        combinatorial_parameters=combinatorial_parameters,
        prepare_ocp_callback=prepare_ocp,
        post_optimization_callback=(save_results, {{"save_folder": save_folder}}),
        should_solve_callback=(should_solve, {{"save_folder": save_folder}}),
        solver=get_solver(),  # You cannot use show_online_optim with multi-start
        n_pools=n_pools,
    )

def main(is_multistart: bool = False, nb_seeds: int = 1, save_folder: str = "save"):
    # --- Prepare the multi-start and run it --- #

    seed = [i for i in range(nb_seeds)]

    combinatorial_parameters = {{
        "seed": seed,
        "is_multistart": [is_multistart],
    }}

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    if is_multistart:
        multi_start = prepare_multi_start(
            combinatorial_parameters=combinatorial_parameters,
            save_folder=save_folder,
            n_pools=2,
        )

        start_time = time.time()
        multi_start.solve()
        with open(f"{{save_folder}}/timelog.txt", "a") as f:
            f.write(f"multi_{{nb_seeds}}_acrobatics_{'_'.join(str(i) for i in half_twists)}_{side}_{position}: {{time.time() - start_time}}\\n")
            
    else:
        ocp = prepare_ocp()
        solver = get_solver()
        
        start_time = time.time()
        sol = ocp.solve(solver=solver)
        with open(f"{{save_folder}}/timelog.txt", "a") as f:
            f.write(f"acrobatics_{'_'.join(str(i) for i in half_twists)}_{side}_{position}: {{time.time() - start_time}}\\n")

        save_results(sol, save_folder=save_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required argument for save folder path
    parser.add_argument('save_folder_path', type=str, help='Path to the save folder')

    # Optional argument for multistart
    parser.add_argument('-m', '--multistart', type=int, help='Number of seeds for multistart')

    args = parser.parse_args()

    save_folder_path = args.save_folder_path
    nb_seeds = args.multistart or 1
    is_multi = args.multistart is not None

    main(is_multi, nb_seeds, save_folder_path) 

"""

    return CodeGenerationResponse(
        generated_code=generated,
        new_model=new_bio_model,
        new_model_path=str(new_model_path),
    )
