from fastapi import HTTPException

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_responses import AcrobaticPhaseDurationResponse
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_data import (
    AcrobaticsOCPData,
)
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_phases import GenericPhaseRouter
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_requests import PhaseDurationRequest


class AcrobaticsPhaseRouter(GenericPhaseRouter):
    def __init__(self):
        super().__init__(AcrobaticsOCPData)

    def register_put_phase_index_duration(self) -> None:
        @self.router.put("/{phase_index}/duration", response_model=AcrobaticPhaseDurationResponse)
        def put_duration(phase_index: int, duration: PhaseDurationRequest):
            if duration.duration <= 0:
                raise HTTPException(status_code=400, detail="duration must be positive")

            # read data
            infos = self.data.read_data()
            phases_info = infos["phases_info"]

            # logic
            phases_info[phase_index]["duration"] = duration.duration
            new_final_time = sum(somersault["duration"] for somersault in phases_info)
            infos["final_time"] = new_final_time

            # update
            self.data.update_data("phases_info", phases_info)
            self.data.update_data("final_time", infos["final_time"])

            return AcrobaticPhaseDurationResponse(
                duration=duration.duration,
                new_final_time=round(new_final_time, 2),
            )

    def register_get_phase_index_dynamics(self):
        pass  # disable

    def register_put_phase_index_dynamics(self):
        pass  # disable
