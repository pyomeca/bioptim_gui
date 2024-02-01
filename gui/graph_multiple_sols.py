import argparse
import pickle as pkl
import numpy as np
import bioptim
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathlib import Path


def get_dofs_name(nb_q):
    # vanilla, with vision, with spine, with spine and vision
    straight_nb_q = [10, 14, 22, 26]
    pike_nb_q = [16, 20, 28, 32]
    tuck_nb_q = [17, 21, 29, 33]

    spine_nb_q = [22, 26, 28, 29, 32, 33]
    vision_nb_q = [13, 20, 21, 26, 32, 33]

    vision_dofs = [
        "Head rotation Z",
        "Head rotation X",
        "Eyes rotation Z",
        "Eyes rotation X",
    ]

    spine_dofs = [
        "Stomach rotation X",
        "Stomach rotation Y",
        "Stomach rotation Z",
        "Rib rotation X",
        "Rib rotation Y",
        "Rib rotation Z",
        "Nipple rotation X",
        "Nipple rotation Y",
        "Nipple rotation Z",
        "Shoulder rotation X",
        "Shoulder rotation Y",
        "Shoulder rotation Z",
    ]

    common_dofs = [
        "Pelvis translation X",
        "Pelvis translation Y",
        "Pelvis translation Z",
        "Pelvis rotation X",
        "Pelvis rotation Y",
        "Pelvis rotation Z",
    ]

    sufix_dofs_non_straight = [
        "Right upper arm rotation Z",
        "Right upper arm rotation Y",
        "Right lower arm rotation Z",
        "Right lower arm rotation X",
        "Left upper arm rotation Z",
        "Left upper arm rotation Y",
        "Left lower arm rotation Z",
        "Left lower arm rotation X",
        "Upper legs rotation X",
        "Upper legs rotation Y",
    ]

    straight_arms_dofs = [
        "Right upper arm rotation Z",
        "Right upper arm rotation Y",
        "Left upper arm rotation Z",
        "Left upper arm rotation Y",
    ]

    tuck_sufix_dofs = [
        "Lower legs rotation X",
    ]

    with_spine = nb_q in spine_nb_q
    with_vision = nb_q in vision_nb_q

    dof_names = common_dofs
    if with_spine:
        dof_names += spine_dofs
    if with_vision:
        dof_names += vision_dofs

    if nb_q in straight_nb_q:
        dof_names += straight_arms_dofs
    else:
        dof_names += sufix_dofs_non_straight
        if nb_q in tuck_nb_q:
            dof_names += tuck_sufix_dofs

    return dof_names


def plot_solutions(pkl_paths: list[str], variable: str = "q") -> None:
    assert len(pkl_paths) != 0

    with open(pkl_paths[0], "rb") as f:
        o = pkl.load(f)

    nb_q = len(o["integrated_states"][0][variable])
    name_dof = get_dofs_name(nb_q)

    final_time = round(o["time_vector"][0][-1], 2)
    nb_phases = len(o["solution"].states)
    n_shooting = [len(o["solution"].states[phase][variable][0]) - 1 for phase in range(nb_phases)]

    time = np.linspace(0, final_time, sum(n_shooting) + 1)

    # plot setup
    n_plot_lines = int(nb_q / 4 + 1)
    fig, axs = plt.subplots(n_plot_lines, 4, figsize=(40, 20))
    axs = axs.ravel()

    cmap = matplotlib.colormaps["viridis"]

    legend_handles = []

    for i, pkl_path in enumerate(pkl_paths):
        with open(pkl_path, "rb") as f:
            o = pkl.load(f)

        nb_phases = len(o["solution"].states)
        n_shooting = [len(o["solution"].states[phase][variable][0]) - 1 for phase in range(nb_phases)]
        time = np.linspace(0, final_time, sum(n_shooting) + 1)

        for dof in range(nb_q):
            solution_q = o["integrated_states"][0][variable][dof]

            # plot solution
            color = cmap(i / len(pkl_paths))
            axs[dof].plot(time, solution_q, color=color, marker=".")

            (line,) = axs[dof].plot(time, solution_q, color=color, label=Path(pkl_path).stem)

            # title
            axs[dof].set_title(name_dof[dof], fontsize=18)

            min_bounds_per_phase = [o["x_bounds"][phase][variable].min[dof].tolist() for phase in range(nb_phases)]
            max_bounds_per_phase = [o["x_bounds"][phase][variable].max[dof].tolist() for phase in range(nb_phases)]

            ylims = [
                (np.min(min_bounds_per_phase) - 0.1) * 1.1,
                (np.max(max_bounds_per_phase) + 0.1) * 1.1,
            ]

            # limits
            axs[dof].set_xlim([0, final_time])
            axs[dof].set_ylim(ylims)

            for phase in range(nb_phases):
                # plot bounds
                n_shooting_start, n_shooting_end = sum(n_shooting[:phase]), sum(n_shooting[: phase + 1])
                t_start = time[n_shooting_start]
                t_end = time[n_shooting_end]
                bound_width = 0.005

                # Plot horizontal lines for min and max bound value + vertical line
                for phases_bound in [min_bounds_per_phase, max_bounds_per_phase]:
                    bound = phases_bound[phase]

                    if phase != 0:
                        axs[dof].vlines(
                            t_start,
                            bound[0],
                            phases_bound[phase - 1][2],
                            linewidth=0.5,
                            color="black",
                            linestyles="dashed",
                        )
                    axs[dof].hlines(
                        bound[0], t_start, t_start + bound_width, linewidth=0.5, color="black", linestyles="dashed"
                    )

                    axs[dof].vlines(
                        t_start + bound_width, bound[0], bound[1], linewidth=0.5, color="black", linestyles="dashed"
                    )
                    axs[dof].hlines(
                        bound[1],
                        t_start + bound_width,
                        t_end - bound_width,
                        linewidth=0.5,
                        color="black",
                        linestyles="dashed",
                    )

                    axs[dof].vlines(
                        t_end - bound_width, bound[1], bound[2], linewidth=0.5, color="black", linestyles="dashed"
                    )
                    axs[dof].hlines(
                        bound[2], t_end - bound_width, t_end, linewidth=0.5, color="black", linestyles="dashed"
                    )

        # append to legend for each pickle
        legend_handles.append(line)

    # Add a single legend to the entire figure
    plt.legend(handles=legend_handles, loc="upper right")

    fig.tight_layout()

    outpath = Path(pkl_path).parent / f"{variable}_graphs.png"
    fig.savefig(outpath, dpi=300)


def main():
    parser = argparse.ArgumentParser(description="Process a list of pickle files.")

    parser.add_argument("pickles", nargs="+", help="List of pickle files to process.")

    args = parser.parse_args()

    pickle_paths = args.pickles

    plot_solutions(pickle_paths)
    plot_solutions(pickle_paths, "qdot")


if __name__ == "__main__":
    main()
