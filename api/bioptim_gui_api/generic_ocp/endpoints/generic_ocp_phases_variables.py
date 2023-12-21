from abc import ABC

import numpy as np
from fastapi import APIRouter

from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_requests import (
    DimensionRequest,
    InterpolationTypeRequest,
    VariableUpdateRequest,
)
from bioptim_gui_api.variables.misc.variables_utils import variables_zeros


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
                shape = np.array(variable["bounds"][bound]).shape
                new_value = np.zeros((new_dimension, shape[1])).tolist()
                variable["bounds"][bound] = new_value

            shape = np.array(variable["initial_guess"]).shape
            new_value = np.zeros((new_dimension, shape[1])).tolist()
            variable["initial_guess"] = new_value

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
