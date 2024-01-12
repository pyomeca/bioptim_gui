class AcrobaticsGenerationCommon:
    """
    This class contains the common code for the generation of the acrobatics, including multistart, save, main, ...
    """

    @staticmethod
    def construct_path(half_twists: list[int], side: str, position: str):
        return f"""
def construct_filepath(save_path, seed = 0):
    return f"{{save_path}}/acrobatics_{'_'.join(str(i) for i in half_twists)}_{side}_{position}_{{seed}}.pkl"
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

    try:
        seed, is_multistart = combinatorial_parameters
    except:
        seed, is_multistart = 0, False

    save_folder = extra_parameters["save_folder"]
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    with open(f"{save_folder}/log.txt", "a") as f:
        if sol.status != 0:
            f.write(f"{seed} DVG\\n")
            return # don't save the results if it didn't converge
        else:
            f.write(f"{seed} CVG\\n")

    file_path = construct_filepath(save_folder, seed)

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
"""

    @staticmethod
    def get_solver():
        return """
def get_solver():
    solver = Solver.IPOPT(show_online_optim=False, show_options=dict(show_bounds=True))
    solver.set_linear_solver("ma57")
    solver.set_maximum_iterations(3000)
    solver.set_convergence_tolerance(1e-6)
    return solver
"""

    @staticmethod
    def prepare_multi_start():
        return """
def prepare_multi_start(
    combinatorial_parameters: dict,
    save_folder: str = None,
    n_pools: int = 2,
) -> MultiStart:
    \"""
    The initialization of the multi-start
    \"""

    return MultiStart(
        combinatorial_parameters=combinatorial_parameters,
        prepare_ocp_callback=prepare_ocp,
        post_optimization_callback=(save_results, {"save_folder": save_folder}),
        should_solve_callback=(should_solve, {"save_folder": save_folder}),
        solver=get_solver(),  # You cannot use show_online_optim with multi-start
        n_pools=n_pools,
    )
"""

    @staticmethod
    def main_function(half_twists: list[int], side: str, position: str) -> str:
        file_addon = f"{'_'.join(str(i) for i in half_twists)}_{side}_{position}"
        return f"""
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
            f.write(f"multi_{{nb_seeds}}_acrobatics_{file_addon}: {{time.time() - start_time}}\\n")

    else:
        ocp = prepare_ocp()
        solver = get_solver()

        start_time = time.time()
        sol = ocp.solve(solver=solver)
        with open(f"{{save_folder}}/timelog.txt", "a") as f:
            f.write(f"acrobatics_{file_addon}: {{time.time() - start_time}}\\n")

        save_results(sol, save_folder=save_folder)
"""

    @staticmethod
    def name_eq_main():
        return """
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

    @staticmethod
    def generate_common(data: dict) -> str:
        half_twists = data["nb_half_twists"]
        side = data["preferred_twist_side"]
        position = data["position"]

        ret = AcrobaticsGenerationCommon.construct_path(half_twists, side, position)
        ret += AcrobaticsGenerationCommon.save_result()
        ret += AcrobaticsGenerationCommon.should_solve()
        ret += AcrobaticsGenerationCommon.get_solver()
        ret += AcrobaticsGenerationCommon.prepare_multi_start()
        ret += AcrobaticsGenerationCommon.main_function(half_twists, side, position)
        ret += AcrobaticsGenerationCommon.name_eq_main()
        return ret
