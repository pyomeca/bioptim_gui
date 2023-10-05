import numpy as np
from fastapi import APIRouter

from bioptim_gui_api.generic_ocp.generic_ocp_responses import *
from bioptim_gui_api.generic_ocp.generic_ocp_utils import (
    read_generic_ocp_data,
    update_generic_ocp_data,
)
from bioptim_gui_api.variables.variables_utils import variables_zeros

router = APIRouter()


@router.put("/{phase_index}/state_variables/{variable_index}/dimension")
def put_state_variable_dimensions(
    phase_index: int, variable_index: int, dimension: DimensionRequest
):
    phases_info = read_generic_ocp_data("phases_info")

    new_dimension = dimension.dimension

    variable = phases_info[phase_index]["state_variables"][variable_index]

    variable["dimension"] = new_dimension

    for bound in variable["bounds"].keys():
        shape = np.array(variable["bounds"][bound]).shape
        new_value = np.zeros((new_dimension, shape[1])).tolist()
        variable["bounds"][bound] = new_value

    shape = np.array(variable["initial_guess"]).shape
    new_value = np.zeros((new_dimension, shape[1])).tolist()
    variable["initial_guess"] = new_value

    update_generic_ocp_data("phases_info", phases_info)
    return phases_info


@router.put("/{phase_index}/state_variables/{variable_index}/bounds_interpolation_type")
def put_state_variables_bounds_interpolation_type(
    phase_index: int, variable_index: int, interpolation: InterpolationTypeRequest
):
    phases_info = read_generic_ocp_data("phases_info")

    new_interpolation = interpolation.interpolation_type

    variable = phases_info[phase_index]["state_variables"][variable_index]

    variable["bounds_interpolation_type"] = new_interpolation
    dimension = variable["dimension"]

    variable["bounds"]["min_bounds"] = variables_zeros(dimension, new_interpolation)
    variable["bounds"]["max_bounds"] = variables_zeros(dimension, new_interpolation)

    phases_info[phase_index]["state_variables"][variable_index] = variable

    update_generic_ocp_data("phases_info", phases_info)

    return phases_info


@router.put(
    "/{phase_index}/state_variables/{variable_index}/initial_guess_interpolation_type"
)
def put_state_variables_initial_guess_interpolation_type(
    phase_index: int, variable_index: int, interpolation: InterpolationTypeRequest
):
    phases_info = read_generic_ocp_data("phases_info")

    new_interpolation = interpolation.interpolation_type

    variable = phases_info[phase_index]["state_variables"][variable_index]

    variable["initial_guess_interpolation_type"] = new_interpolation
    dimension = variable["dimension"]
    variable["initial_guess"] = variables_zeros(dimension, new_interpolation)

    phases_info[phase_index]["state_variables"][variable_index] = variable

    update_generic_ocp_data("phases_info", phases_info)
    return phases_info


@router.put("/{phase_index}/state_variables/{variable_index}/max_bounds")
def put_state_variables_max_bounds_value(
    phase_index: int, variable_index: int, value: VariableUpdateRequest
):
    phases_info = read_generic_ocp_data("phases_info")
    x, y, new_value = value.x, value.y, value.value

    variable = phases_info[phase_index]["state_variables"][variable_index]

    variable["bounds"]["max_bounds"][x][y] = new_value

    phases_info[phase_index]["state_variables"][variable_index] = variable

    update_generic_ocp_data("phases_info", phases_info)
    return phases_info


@router.put("/{phase_index}/state_variables/{variable_index}/min_bounds")
def put_state_variables_min_bounds_value(
    phase_index: int, variable_index: int, value: VariableUpdateRequest
):
    phases_info = read_generic_ocp_data("phases_info")
    x, y, new_value = value.x, value.y, value.value

    variable = phases_info[phase_index]["state_variables"][variable_index]

    variable["bounds"]["min_bounds"][x][y] = new_value

    phases_info[phase_index]["state_variables"][variable_index] = variable

    update_generic_ocp_data("phases_info", phases_info)
    return phases_info


@router.put("/{phase_index}/state_variables/{variable_index}/initial_guess")
def put_state_variables_initial_guess_value(
    phase_index: int, variable_index: int, value: VariableUpdateRequest
):
    phases_info = read_generic_ocp_data("phases_info")
    x, y, new_value = value.x, value.y, value.value

    variable = phases_info[phase_index]["state_variables"][variable_index]

    variable["initial_guess"][x][y] = new_value

    phases_info[phase_index]["state_variables"][variable_index] = variable

    update_generic_ocp_data("phases_info", phases_info)
    return phases_info
