import inspect
import re

import bioptim
from bioptim import ObjectiveFcn
from fastapi import HTTPException


def format_arg_type(arg_type: str) -> str:
    """
    Format the type of the argument

    Parameters
    ----------
    arg_type: str
        The type of the argument (e.g. "<class 'list'>", "float")

    Returns
    -------
    The formatted type (e.g. "list", "float")
    """
    pattern = r"<(class|enum) '(.*)'>"
    arg_type = str(arg_type)
    match = re.search(pattern, arg_type)
    return match and match.group(2) or arg_type


def get_args(penalty_fcn) -> list:
    """
    Get the arguments of the penalty function

    Parameters
    ----------
    penalty_fcn: ObjectiveFcn or ConstraintFcn
        The penalty function

    Returns
    -------
    The list of arguments (e.g. [{"name": "state_idx", "value": None, "type": "list"}])
    with "value" being the defaults value
    """
    penalty_fcn = penalty_fcn.value[0]
    # arguments
    arg_specs = inspect.getfullargspec(penalty_fcn)
    defaults = arg_specs.defaults
    arguments = arg_specs.annotations

    formatted_arguments = [
        {"name": k, "value": None, "type": format_arg_type(v)}
        for k, v in arguments.items()
    ]

    if defaults:
        l_defaults = len(defaults)
        for i in range(l_defaults):
            formatted_arguments[-l_defaults + i]["value"] = defaults[i]

    formatted_arguments = [
        arg
        for arg in formatted_arguments
        if arg["name"] not in ("_", "penalty", "controller")
    ]

    return formatted_arguments


def obj_arguments(objective_type: str, penalty_type: str) -> list:
    """
    Get the arguments of the objective function

    Parameters
    ----------
    objective_type: str
        The type of objective ("mayer" or "lagrange")
    penalty_type: str
        The type of penalty (ObjectiveFcn.Mayer or ObjectiveFcn.Lagrange, e.g. "MINIMIZE_STATE")

    Returns
    -------
    The list of arguments (e.g. [{"name": "state_idx", "value": None, "type": "list"}])
    """
    penalty_type = penalty_type.upper().replace(" ", "_")
    if objective_type == "mayer":
        penalty_fcn = getattr(ObjectiveFcn.Mayer, penalty_type)
    elif objective_type == "lagrange":
        penalty_fcn = getattr(ObjectiveFcn.Lagrange, penalty_type)
    else:
        raise HTTPException(404, f"{objective_type} not found")

    arguments = get_args(penalty_fcn)
    return arguments


def constraint_arguments(penalty_type: str) -> list:
    """
    Get the arguments of the constraint function

    Parameters
    ----------
    penalty_type: str
        The type of penalty (ConstraintFcn, e.g. "CONTINUITY")

    Returns
    -------
    The list of arguments (e.g. [{"name": "state_idx", "value": None, "type": "list"}])
    """
    penalty_type = penalty_type.upper().replace(" ", "_")
    try:
        penalty_fcn = getattr(bioptim.ConstraintFcn, penalty_type)
    except AttributeError:
        raise HTTPException(404, f"{penalty_type} not found")

    arguments = get_args(penalty_fcn)
    return arguments
