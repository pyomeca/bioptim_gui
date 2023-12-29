from abc import ABC

import numpy as np
from fastapi import APIRouter

from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_requests import (
    DimensionRequest,
    InterpolationTypeRequest,
    VariableUpdateRequest,
)
from bioptim_gui_api.variables.misc.variables_utils import variables_zeros


def new_shape(array: list, new_dimension: int) -> tuple:
    shape = np.array(array).shape
    if len(shape) == 1:
        return (new_dimension,)
    else:
        return new_dimension, shape[1]


class GenericVariableRouter(ABC):
    def __init__(self, data, variable_type: str):
        self.data = data
        self.variable_type = variable_type
        self.router = None

    def register(self, route: APIRouter):
        self.router = route
        self.register_put_variable_dimension()
        self.register_put_variable_bounds_interpolation_type()
        self.register_put_variable_initial_guess_interpolation_type()
        self.register_put_variable_max_bounds_value()
        self.register_put_variable_min_bounds_value()
        self.register_put_variable_initial_guess_value()

    def register_put_variable_dimension(self):
        @self.router.put(f"/{{phase_index}}/{self.variable_type}/{{variable_index}}/dimension")
        def put_variables_dimensions(phase_index: int, variable_index: int, dimension: DimensionRequest):
            phases_info = self.data.read_data("phases_info")

            new_dimension = dimension.dimension
            variable = phases_info[phase_index][self.variable_type][variable_index]
            variable["dimension"] = new_dimension

            for bound in variable["bounds"].keys():
                new_bound_shape = new_shape(variable["bounds"][bound], new_dimension)
                variable["bounds"][bound] = np.zeros(new_bound_shape).tolist()

            new_init_shape = new_shape(variable["initial_guess"], new_dimension)
            variable["initial_guess"] = np.zeros(new_init_shape).tolist()

            self.data.update_data("phases_info", phases_info)
            return phases_info

    def register_put_variable_bounds_interpolation_type(self):
        @self.router.put(f"/{{phase_index}}/{self.variable_type}/{{variable_index}}/bounds_interpolation_type")
        def put_variables_bounds_interpolation_type(
            phase_index: int, variable_index: int, interpolation: InterpolationTypeRequest
        ):
            phases_info = self.data.read_data("phases_info")

            new_interpolation = interpolation.interpolation_type

            variable = phases_info[phase_index][self.variable_type][variable_index]

            variable["bounds_interpolation_type"] = new_interpolation
            dimension = variable["dimension"]

            variable["bounds"]["min_bounds"] = variables_zeros(dimension, new_interpolation)
            variable["bounds"]["max_bounds"] = variables_zeros(dimension, new_interpolation)

            phases_info[phase_index][self.variable_type][variable_index] = variable

            self.data.update_data("phases_info", phases_info)

            return phases_info

    def register_put_variable_initial_guess_interpolation_type(self):
        @self.router.put(f"/{{phase_index}}/{self.variable_type}/{{variable_index}}/initial_guess_interpolation_type")
        def put_variables_initial_guess_interpolation_type(
            phase_index: int, variable_index: int, interpolation: InterpolationTypeRequest
        ):
            phases_info = self.data.read_data("phases_info")

            new_interpolation = interpolation.interpolation_type

            variable = phases_info[phase_index][self.variable_type][variable_index]

            variable["initial_guess_interpolation_type"] = new_interpolation
            dimension = variable["dimension"]
            variable["initial_guess"] = variables_zeros(dimension, new_interpolation)

            phases_info[phase_index][self.variable_type][variable_index] = variable

            self.data.update_data("phases_info", phases_info)
            return phases_info

    def register_put_variable_max_bounds_value(self):
        @self.router.put(f"/{{phase_index}}/{self.variable_type}/{{variable_index}}/max_bounds")
        def put_variables_max_bounds_value(phase_index: int, variable_index: int, value: VariableUpdateRequest):
            phases_info = self.data.read_data("phases_info")
            x, y, new_value = value.x, value.y, value.value

            variable = phases_info[phase_index][self.variable_type][variable_index]

            if variable["bounds_interpolation_type"] == "CONSTANT":
                variable["bounds"]["max_bounds"][x] = new_value
            else:
                variable["bounds"]["max_bounds"][x][y] = new_value

            phases_info[phase_index][self.variable_type][variable_index] = variable

            self.data.update_data("phases_info", phases_info)
            return phases_info

    def register_put_variable_min_bounds_value(self):
        @self.router.put(f"/{{phase_index}}/{self.variable_type}/{{variable_index}}/min_bounds")
        def put_variables_min_bounds_value(phase_index: int, variable_index: int, value: VariableUpdateRequest):
            phases_info = self.data.read_data("phases_info")
            x, y, new_value = value.x, value.y, value.value

            variable = phases_info[phase_index][self.variable_type][variable_index]

            if variable["bounds_interpolation_type"] == "CONSTANT":
                variable["bounds"]["min_bounds"][x] = new_value
            else:
                variable["bounds"]["min_bounds"][x][y] = new_value

            phases_info[phase_index][self.variable_type][variable_index] = variable

            self.data.update_data("phases_info", phases_info)
            return phases_info

    def register_put_variable_initial_guess_value(self):
        @self.router.put(f"/{{phase_index}}/{self.variable_type}/{{variable_index}}/initial_guess")
        def put_variables_initial_guess_value(phase_index: int, variable_index: int, value: VariableUpdateRequest):
            phases_info = self.data.read_data("phases_info")
            x, y, new_value = value.x, value.y, value.value

            variable = phases_info[phase_index][self.variable_type][variable_index]

            if variable["initial_guess_interpolation_type"] == "CONSTANT":
                variable["initial_guess"][x] = new_value
            else:
                variable["initial_guess"][x][y] = new_value

            phases_info[phase_index][self.variable_type][variable_index] = variable

            self.data.update_data("phases_info", phases_info)
            return phases_info


class GenericControlVariableRouter(GenericVariableRouter):
    def __init__(self, data):
        super().__init__(data, "control_variables")


class GenericStateVariableRouter(GenericVariableRouter):
    def __init__(self, data):
        super().__init__(data, "state_variables")
