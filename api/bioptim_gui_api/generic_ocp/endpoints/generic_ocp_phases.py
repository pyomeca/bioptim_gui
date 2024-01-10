from fastapi import APIRouter, HTTPException

from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_requests import (
    DynamicsRequest,
    NbShootingPointsRequest,
    PhaseDurationRequest,
)
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_responses import (
    NbShootingPointsResponse,
    PhaseDurationResponse,
)
from bioptim_gui_api.utils.format_utils import get_spaced_capitalized
from bioptim_gui_api.variables.misc.enums import Dynamics
from bioptim_gui_api.variables.misc.variables_config import get_dynamics_decision_variables


# phases info endpoints


class GenericPhaseRouter:
    def __init__(self, data):
        self.data = data
        self.router = None

    def register(self, route: APIRouter) -> None:
        self.router = route

        self.register_phase_root()
        self.register_get_phase_index()
        self.register_put_phase_index_nb_shooting_points()
        self.register_put_phase_index_duration()
        self.register_get_phase_index_dynamics()
        self.register_put_phase_index_dynamics()

    def register_phase_root(self):
        @self.router.get("/", response_model=list)
        def get_phases_info():
            phases_info = self.data.read_data("phases_info")
            return phases_info

    def register_get_phase_index(self):
        @self.router.get("/{phase_index}", response_model=dict)
        def get_phase_info(phase_index: int):
            n_phases = self.data.read_data("nb_phases")
            if phase_index < 0 or phase_index >= n_phases:
                raise HTTPException(
                    status_code=404,
                    detail=f"phase_index must be between 0 and {n_phases - 1}",
                )
            phases_info = self.data.read_data("phases_info")
            return phases_info[phase_index]

    def register_put_phase_index_nb_shooting_points(self):
        @self.router.put(
            "/{phase_index}/nb_shooting_points",
            response_model=NbShootingPointsResponse,
        )
        def put_nb_shooting_points(phase_index: int, nb_shooting_points: NbShootingPointsRequest):
            if nb_shooting_points.nb_shooting_points <= 0:
                raise HTTPException(status_code=400, detail="nb_shooting_points must be positive")
            phases_info = self.data.read_data("phases_info")
            phases_info[phase_index]["nb_shooting_points"] = nb_shooting_points.nb_shooting_points
            self.data.update_data("phases_info", phases_info)
            return NbShootingPointsResponse(nb_shooting_points=nb_shooting_points.nb_shooting_points)

    def register_put_phase_index_duration(self):
        @self.router.put(
            "/{phase_index}/duration",
            response_model=PhaseDurationResponse,
        )
        def put_duration(phase_index: int, duration: PhaseDurationRequest):
            if duration.duration <= 0:
                raise HTTPException(status_code=400, detail="duration must be positive")
            infos = self.data.read_data()
            phases_info = infos["phases_info"]
            phases_info[phase_index]["duration"] = duration.duration
            self.data.update_data("phases_info", phases_info)
            return PhaseDurationResponse(duration=duration.duration)

    def register_get_phase_index_dynamics(self):
        @self.router.get("/{phase_index}/dynamics", response_model=list)
        def get_dynamics_list():
            return get_spaced_capitalized(Dynamics)

    def register_put_phase_index_dynamics(self):
        @self.router.put("/{phase_index}/dynamics", response_model=list)
        def put_dynamics_list(phase_index: int, dynamic_req: DynamicsRequest):
            phases_info = self.data.read_data("phases_info")

            new_dynamic = dynamic_req.dynamics

            phases_info[phase_index]["dynamics"] = new_dynamic

            new_variables = get_dynamics_decision_variables(new_dynamic)

            phases_info[phase_index]["state_variables"] = new_variables["state_variables"]
            phases_info[phase_index]["control_variables"] = new_variables["control_variables"]

            self.data.update_data("phases_info", phases_info)
            return phases_info
