import json

from fastapi import APIRouter

import bioptim_gui_api.generic_ocp.generic_ocp_config as config

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


def read_generic_ocp_data(key: str = None) -> dict:
    with open(config.DefaultGenericOCPConfig.datafile, "r") as f:
        data = json.load(f)
    return data if key is None else data[key]


def arg_to_string(argument: dict) -> str:
    name, type, value = argument["name"], argument["type"], argument["value"]
    if type == "int" or type == "float":
        return f"{name}={value}"
    else:
        return f'{name}="{value}"'


@router.get("/generate_code", response_model=str)
def get_generic_ocp_generated_code():
    data = read_generic_ocp_data()

    nb_phases = data["nb_phases"]
    model_path = data["model_path"]
    phases = data["phases_info"]

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
    InterpolationType,
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
    nb_phases = {nb_phases}
    bio_model = [BiorbdModel(r"{model_path}") for _ in range(nb_phases)]
    n_shooting = [{", ".join([str(p["nb_shooting_points"]) for p in phases])}]
    phase_time = [{", ".join([str(p["duration"]) for p in phases])}]
"""
    generated += f"""
    # Declaration of the dynamics function used during integration
    dynamics = DynamicsList()
    """

    if nb_phases == 1:
        generated += f"""
    dynamics.add(
        DynamicsFcn.TORQUE_DRIVEN,
        expand=True,
    )
    """
    else:
        generated += f"""
    for i in range(nb_phases):
        dynamics.add(
            DynamicsFcn.TORQUE_DRIVEN,
            expand=True,
            phase=i,
        )
"""

    generated += f"""
    # Declaration of the constraints and objectives of the ocp
    constraints = ConstraintList()
    objective_functions = ObjectiveList()
"""

    for i in range(nb_phases):
        for objective in phases[i]["objectives"]:
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
            if nb_phases > 1:
                generated += f"        phase={i},\n"

            generated += """
    )"""

        for constraint in phases[i]["constraints"]:
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
            if nb_phases > 1:
                generated += f"        phase={i},\n"

            generated += """    )
"""

    generated += f"""
    # Declaration of optimization variables bounds and initial guesses
    x_bounds = BoundsList()
    x_initial_guesses = InitialGuessList()

    u_bounds = BoundsList()
    u_initial_guesses = InitialGuessList()
"""

    for i in range(nb_phases):
        for state_variable in phases[i]["state_variables"]:
            generated += f"""
    x_bounds.add(
        "{state_variable["name"]}",
        min_bound={state_variable["bounds"]["min_bounds"]},
        max_bound={state_variable["bounds"]["max_bounds"]},
        interpolation=InterpolationType.{state_variable["bounds_interpolation_type"]},"""

            if nb_phases > 1:
                generated += f"""
        phase={i},
"""

            generated += """    )
"""

            generated += f"""
    x_initial_guesses.add(
        "{state_variable["name"]}",
        initial_guess={state_variable["initial_guess"]},
        interpolation=InterpolationType.{state_variable["initial_guess_interpolation_type"]},
"""

            if nb_phases > 1:
                generated += f"""        phase={i},"""

            generated += """
    )
"""

    for i in range(nb_phases):
        for control_variable in phases[i]["control_variables"]:
            generated += f"""
    u_bounds.add(
        "{control_variable["name"]}",
        min_bound={control_variable["bounds"]["min_bounds"]},
        max_bound={control_variable["bounds"]["max_bounds"]},
        interpolation=InterpolationType.{control_variable["bounds_interpolation_type"]},
"""

            if nb_phases > 1:
                generated += f"""        phase={i},
"""

            generated += """    )
"""

        generated += f"""
    u_initial_guesses.add(
        "{control_variable["name"]}",
        initial_guess={control_variable["initial_guess"]},
        interpolation=InterpolationType.{control_variable["initial_guess_interpolation_type"]},
"""

        if nb_phases > 1:
            generated += f"""        phase={i},
"""

        generated += """    )
"""

    generated += """
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
        constraints=constraints,
        objective_functions=objective_functions,
        use_sx=True,
    )


def main():
    \"""
    If this file is run, then it will perform the optimization
    \"""

    # --- Prepare the ocp --- #
    ocp = prepare_ocp()

    # --- Solve the ocp --- #
    sol = ocp.solve(solver=Solver.IPOPT())
    sol.animate()


if __name__ == "__main__":
    main()

"""

    return generated
