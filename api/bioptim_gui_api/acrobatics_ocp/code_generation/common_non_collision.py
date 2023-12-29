from bioptim_gui_api.acrobatics_ocp.code_generation.common import AcrobaticsGenerationCommon


class AcrobaticsGenerationCommonNonCollision(AcrobaticsGenerationCommon):
    """
    This class contains the common code for the generation of the acrobatics, including multistart, save, main, ...
    """

    @staticmethod
    def construct_path(half_twists: list[int], side: str, position: str):
        return f"""
def construct_filepath(warming_up, save_path, seed = 0):
    is_warm = "warming" if warming_up else "warm"
    return f"{{save_path}}/{{is_warm}}_acrobatics_{'_'.join(str(i) for i in half_twists)}_{side}_{position}_{{seed}}.pkl"
"""

    @staticmethod
    def save_result():
        return """
def save_results(sol: Solution, *combinatorial_parameters, **extra_parameters) -> None:
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

    save_folder = extra_parameters["save_folder"]
    warming_up = extra_parameters["warming_up"]

    seed, warming_up, pkl_path = combinatorial_parameters
    if not warming_up:
        seed = int(pkl_path.split("_")[-1].split(".")[0])

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    with open(f"{save_folder}/log.txt", "a") as f:
        if sol.status != 0:
            f.write(f"{seed} DVG\\n")
        else:
            f.write(f"{seed} CVG\\n")

    file_path = construct_filepath(warming_up, save_folder, seed)

    integrated = sol.integrate(merge_phases=True)
    integrated_states, time_vector = integrated._states["unscaled"], integrated._time_vector

    time_parameters = sol.parameters["time"]
    fps = 25
    n_frames = [round(time_parameters[i][0] * fps) for i in range(len(time_parameters))]
    interpolated_states = sol.interpolate(n_frames).states

    to_save = {
            "solution": sol,
            "integrated_states": integrated_states,
            "time_vector": time_vector,
            "interpolated_states": interpolated_states,
    }
    del sol.ocp

    with open(file_path, "wb") as file:
        pkl.dump(to_save, file)
"""

    @staticmethod
    def should_solve():
        return """
def should_solve(*combinatorial_parameters, **extra_parameters):
    save_folder = extra_parameters["save_folder"]
    warming_up = extra_parameters["warming_up"]

    if warming_up:
        seed, warming_up, pkl_path = combinatorial_parameters
    else:
        seed, warming_up, pkl_path = combinatorial_parameters
        seed = int(pkl_path.split("_")[-1].split(".")[0])

    file_path = construct_filepath(warming_up, save_folder, seed)
    return not os.path.exists(file_path)
"""

    @staticmethod
    def get_solver():
        return """
def get_solver(warming_up: bool = False):
    solver = Solver.IPOPT(show_online_optim=False, show_options=dict(show_bounds=True))
    solver.set_linear_solver("ma57")

    max_iter = 1000 if warming_up else 3000
    solver.set_maximum_iterations(max_iter)
    solver.set_convergence_tolerance(1e-6)

    if not warming_up:
        solver.set_bound_frac(1e-8)
        solver.set_bound_push(1e-8)

    return solver
"""

    @staticmethod
    def prepare_multi_start():
        return """
def prepare_multi_start(
    combinatorial_parameters: dict,
    save_folder: str = None,
    n_pools: int = 1,
    warming_up: bool = False,
) -> MultiStart:
    \"""
    The initialization of the multi-start
    \"""

    return MultiStart(
        combinatorial_parameters=combinatorial_parameters,
        prepare_ocp_callback=prepare_ocp,
        should_solve_callback=(should_solve, {"save_folder": save_folder, "warming_up": warming_up}),
        post_optimization_callback=(save_results, {"save_folder": save_folder, "warming_up": warming_up}),
        solver=get_solver(warming_up),  # You cannot use show_online_optim with multi-start
        n_pools=n_pools,
    )
"""

    @staticmethod
    def main_function(half_twists: list[int], side: str, position: str) -> str:
        file_addon = f"{'_'.join(str(i) for i in half_twists)}_{side}_{position}"
        return f"""
def main(nb_seeds: int = 1, save_folder: str = "save"):
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    # --- Prepare the multi-start and run it --- #

    seeds = [i for i in range(nb_seeds)]

    combinatorial_parameters = {{
        "seed": seeds,
        "warming_up": [True],
        "pkl_path": [None],
    }}

    multi_start = prepare_multi_start(
        combinatorial_parameters=combinatorial_parameters,
        save_folder=save_folder,
        n_pools=2,
        warming_up=True,
    )

    start_time = time.time()
    multi_start.solve()
    with open(f"{{save_folder}}/timelog.txt", "a") as f:
        f.write(f"warming_{{nb_seeds}}_acrobatics_{file_addon}: {{time.time() - start_time}}\\n")

    pkl_paths = [construct_filepath(True, save_folder, seed) for seed in seeds]

    cost_path = {{}}

    for pkl_path in pkl_paths:
        with open(pkl_path, "rb") as file:
            sol = pkl.load(file)["solution"]
            cost_path[str(sol.cost)] = pkl_path
        
    pkl_paths = cost_path.values()

    combinatorial_parameters = {{
        "seed": [0],
        "warming_up": [False],
        "pkl_path": pkl_paths,
    }}

    multi_start = prepare_multi_start(
        combinatorial_parameters=combinatorial_parameters,
        save_folder=save_folder,
        n_pools=2,
    )

    start_time = time.time()
    multi_start.solve()
    with open(f"{{save_folder}}/timelog.txt", "a") as f:
        f.write(f"warm_{{nb_seeds}}_acrobatics_{file_addon}: {{time.time() - start_time}}\\n")
"""

    @staticmethod
    def name_eq_main():
        return """
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required argument for save folder path
    parser.add_argument('save_folder_path', type=str, help='Path to the save folder')

    parser.add_argument('-m', '--multistart', type=int, help='Number of seeds for multistart', default=1)

    args = parser.parse_args()

    save_folder_path = args.save_folder_path
    nb_seeds = args.multistart

    main(nb_seeds, save_folder_path)
"""

    @staticmethod
    def generate_common(data: dict) -> str:
        half_twists = data["nb_half_twists"]
        side = data["preferred_twist_side"]
        position = data["position"]

        ret = AcrobaticsGenerationCommonNonCollision.construct_path(half_twists, side, position)
        ret += AcrobaticsGenerationCommonNonCollision.save_result()
        ret += AcrobaticsGenerationCommonNonCollision.should_solve()
        ret += AcrobaticsGenerationCommonNonCollision.get_solver()
        ret += AcrobaticsGenerationCommonNonCollision.prepare_multi_start()
        ret += AcrobaticsGenerationCommonNonCollision.main_function(half_twists, side, position)
        ret += AcrobaticsGenerationCommonNonCollision.name_eq_main()
        return ret
