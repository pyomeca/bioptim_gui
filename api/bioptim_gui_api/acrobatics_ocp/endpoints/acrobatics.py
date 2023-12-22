from fastapi import APIRouter, HTTPException

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_code_generation import (
    router as acrobatics_code_generation_router,
)
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_phases import (
    AcrobaticsPhaseRouter,
)
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_requests import (
    CollisionConstraintRequest,
    FinalTimeMarginRequest,
    FinalTimeRequest,
    NbHalfTwistsRequest,
    NbSomersaultsRequest,
    PositionRequest,
    PreferredTwistSideRequest,
    SportTypeRequest,
    VisualCriteriaRequest,
    WithSpineRequest,
)
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_responses import (
    FinalTimeMarginResponse,
    FinalTimeResponse,
    PreferredTwistSideResponse,
    SportTypeResponse,
)
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_data import AcrobaticsOCPData
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_utils import (
    acrobatics_phase_names,
    update_phase_info,
    adapt_dynamics,
)
from bioptim_gui_api.acrobatics_ocp.misc.enums import (
    Position,
    PreferredTwistSide,
    SportType,
)
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp import GenericOCPBaseFieldRegistrar
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_phases_constraints import GenericOCPConstraintRouter
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_phases_objectives import GenericOCPObjectiveRouter
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_phases_variables import (
    GenericControlVariableRouter,
    GenericStateVariableRouter,
)
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_requests import DynamicsRequest


class AcrobaticsOCPBaseFieldRegistrar(GenericOCPBaseFieldRegistrar):
    def __init__(self, data):
        super().__init__(data)

    def register(self, route: APIRouter) -> None:
        super().register(route)

        # register additional endpoints
        self.register_put_nb_somersaults()
        self.register_put_nb_half_twists()
        self.register_put_final_time()
        self.register_put_final_time_margin()
        self.register_get_positions()
        self.register_put_position()
        self.register_get_sport_types()
        self.register_put_sport_type()
        self.register_get_preferred_twist_side()
        self.register_put_preferred_twist_side()
        self.register_put_with_visual_criteria()
        self.register_put_collision_constraint()
        self.register_get_dynamics()
        self.register_put_dynamics()
        self.register_put_with_spine()

    def register_update_nb_phases(self) -> None:
        # disable the endpoint
        pass

    def register_put_nb_somersaults(self):
        @self.router.put("/nb_somersaults", response_model=dict)
        def update_nb_somersaults(nb_somersaults: NbSomersaultsRequest):
            """
            Append or pop the half_twists list
            Update the number of somersaults of the acrobatics ocp
            Update the phase info of the acrobatics ocp accordingly
            """
            nb_max_somersaults = 5
            old_value = self.data.read_data("nb_somersaults")
            new_nb_somersaults = nb_somersaults.nb_somersaults

            if new_nb_somersaults <= 0 or new_nb_somersaults > nb_max_somersaults:
                raise HTTPException(status_code=400, detail="nb_somersaults must be positive")

            data = self.data.read_data()
            position = data["position"]
            updated_half_twists = data["nb_half_twists"][:new_nb_somersaults] + [0] * (new_nb_somersaults - old_value)

            # 1 somersault tuck/pike are not allowed, set the position to straight
            if new_nb_somersaults == 1 and position != "straight":
                self.data.update_data("position", "straight")
                new_phase_names = acrobatics_phase_names(new_nb_somersaults, "straight", updated_half_twists)
            else:
                new_phase_names = acrobatics_phase_names(new_nb_somersaults, position, updated_half_twists)

            self.data.update_data("nb_somersaults", new_nb_somersaults)
            self.data.update_data("nb_half_twists", updated_half_twists)
            update_phase_info(new_phase_names)

            return self.data.read_data()

    def register_put_nb_half_twists(self):
        @self.router.put("/nb_half_twists/{somersault_index}", response_model=list)
        def put_nb_half_twist(somersault_index: int, half_twists_request: NbHalfTwistsRequest):
            if half_twists_request.nb_half_twists < 0:
                raise HTTPException(status_code=400, detail="nb_half_twists must be positive or zero")
            half_twists = self.data.read_data("nb_half_twists")
            half_twists[somersault_index] = half_twists_request.nb_half_twists
            self.data.update_data("nb_half_twists", half_twists)

            data = self.data.read_data()
            nb_somersaults = data["nb_somersaults"]
            position = data["position"]
            half_twists = data["nb_half_twists"]

            new_phase_names = acrobatics_phase_names(nb_somersaults, position, half_twists)
            update_phase_info(new_phase_names)

            phases_info = self.data.read_data("phases_info")
            return phases_info

    def register_put_final_time(self):
        @self.router.put("/final_time", response_model=FinalTimeResponse)
        def put_final_time(final_time: FinalTimeRequest):
            new_value = final_time.final_time
            if new_value < 0:
                raise HTTPException(status_code=400, detail="final_time must be positive")
            self.data.update_data("final_time", new_value)
            return FinalTimeResponse(final_time=new_value)

    def register_put_final_time_margin(self):
        @self.router.put("/final_time_margin", response_model=FinalTimeMarginResponse)
        def put_final_time_margin(final_time_margin: FinalTimeMarginRequest):
            new_value = final_time_margin.final_time_margin
            if new_value < 0:
                raise HTTPException(status_code=400, detail="final_time_margin must be positive")
            self.data.update_data("final_time_margin", new_value)
            return FinalTimeMarginResponse(final_time_margin=new_value)

    def register_get_positions(self):
        @self.router.get("/position", response_model=list)
        def get_position():
            return [side.capitalize() for side in Position]

    def register_put_position(self):
        @self.router.put("/position", response_model=dict)
        def put_position(position: PositionRequest):
            new_value = position.position.value
            old_value = self.data.read_data("position")

            if old_value == new_value:
                raise HTTPException(
                    status_code=304,
                    detail=f"position is already {position}",
                )

            self.data.update_data("position", new_value)

            data = self.data.read_data()
            nb_somersaults = data["nb_somersaults"]
            half_twists = data["nb_half_twists"]

            # 1 somersault tuck/pike are not allowed, set the nb_somersault to 2
            if old_value == "straight" and nb_somersaults == 1:
                self.data.update_data("nb_somersaults", 2)

                half_twists = data["nb_half_twists"] + [0]
                self.data.update_data("nb_half_twists", half_twists)

            new_phase_names = acrobatics_phase_names(nb_somersaults, new_value, half_twists)
            update_phase_info(new_phase_names)

            return self.data.read_data()

    def register_get_sport_types(self):
        @self.router.get("/sport_type", response_model=list)
        def get_sport_type():
            return [side.capitalize() for side in SportType]

    def register_put_sport_type(self):
        @self.router.put("/sport_type", response_model=SportTypeResponse)
        def put_sport_type(sport_type: SportTypeRequest):
            new_value = sport_type.sport_type.value
            old_value = self.data.read_data("sport_type")

            if old_value == new_value:
                raise HTTPException(
                    status_code=304,
                    detail=f"sport_type is already {sport_type}",
                )

            self.data.update_data("sport_type", new_value)
            return SportTypeResponse(sport_type=new_value)

    def register_get_preferred_twist_side(self):
        @self.router.get("/preferred_twist_side", response_model=list)
        def get_preferred_twist_side():
            return [side.capitalize() for side in PreferredTwistSide]

    def register_put_preferred_twist_side(self):
        @self.router.put("/preferred_twist_side", response_model=PreferredTwistSideResponse)
        def put_preferred_twist_side(preferred_twist_side: PreferredTwistSideRequest):
            new_value = preferred_twist_side.preferred_twist_side.value
            old_value = self.data.read_data("preferred_twist_side")
            if old_value == new_value:
                raise HTTPException(
                    status_code=304,
                    detail=f"preferred_twist_side is already {preferred_twist_side}",
                )

            self.data.update_data("preferred_twist_side", new_value)
            return PreferredTwistSideResponse(preferred_twist_side=new_value)

    def register_put_with_visual_criteria(self):
        @self.router.put("/with_visual_criteria", response_model=list)
        def put_with_visual_criteria(visual_criteria: VisualCriteriaRequest):
            new_value = visual_criteria.with_visual_criteria
            old_value = self.data.read_data("with_visual_criteria")
            if old_value == new_value:
                raise HTTPException(
                    status_code=304,
                    detail=f"with_visual_criteria is already {old_value}",
                )

            self.data.update_data("with_visual_criteria", new_value)

            data = self.data.read_data()
            nb_somersaults = data["nb_somersaults"]
            position = data["position"]
            half_twists = data["nb_half_twists"]

            new_phase_names = acrobatics_phase_names(nb_somersaults, position, half_twists)
            update_phase_info(new_phase_names)

            phases_info = self.data.read_data("phases_info")
            return phases_info

    def register_put_collision_constraint(self):
        @self.router.put("/collision_constraint", response_model=list)
        def put_collision_constraint(collision_constraint: CollisionConstraintRequest):
            new_value = collision_constraint.collision_constraint
            old_value = self.data.read_data("collision_constraint")
            if old_value == new_value:
                raise HTTPException(
                    status_code=304,
                    detail=f"collision_constraint is already {old_value}",
                )

            self.data.update_data("collision_constraint", new_value)

            data = self.data.read_data()
            nb_somersaults = data["nb_somersaults"]
            position = data["position"]
            half_twists = data["nb_half_twists"]

            new_phase_names = acrobatics_phase_names(nb_somersaults, position, half_twists)
            update_phase_info(new_phase_names)

            phases_info = self.data.read_data("phases_info")
            return phases_info

    def register_get_dynamics(self):
        @self.router.get("/dynamics", response_model=list)
        def get_dynamics():
            return ["torque_driven", "joints_acceleration_driven"]

    def register_put_dynamics(self):
        @self.router.put("/dynamics", response_model=list)
        def put_dynamics(dynamics: DynamicsRequest):
            new_value = dynamics.dynamics
            old_value = self.data.read_data("dynamics")
            if old_value == new_value:
                raise HTTPException(
                    status_code=304,
                    detail=f"dynamics is already {old_value}",
                )

            self.data.update_data("dynamics", new_value)

            phases_info = self.data.read_data("phases_info")

            for phase in phases_info:
                adapt_dynamics(phase, new_value)

            self.data.update_data("phases_info", phases_info)

            phases_info = self.data.read_data("phases_info")
            return phases_info

    def register_put_with_spine(self):
        @self.router.put("/with_spine", response_model=list)
        def put_with_spine(with_spine: WithSpineRequest):
            new_value = with_spine.with_spine
            old_value = self.data.read_data("with_spine")
            if old_value == new_value:
                raise HTTPException(
                    status_code=304,
                    detail=f"with_spine is already {old_value}",
                )

            self.data.update_data("with_spine", new_value)
            if new_value:
                self.data.update_data("dynamics", "joints_acceleration_driven")
            else:
                self.data.update_data("dynamics", "torque_driven")

            data = self.data.read_data()
            nb_somersaults = data["nb_somersaults"]
            position = data["position"]
            half_twists = data["nb_half_twists"]

            new_phase_names = acrobatics_phase_names(nb_somersaults, position, half_twists)
            update_phase_info(new_phase_names)

            phases_info = self.data.read_data("phases_info")
            return phases_info


router = APIRouter(
    prefix="/acrobatics",
    tags=["acrobatics"],
    responses={404: {"description": "Not found"}},
)
AcrobaticsOCPBaseFieldRegistrar(AcrobaticsOCPData).register(router)

phase_router = APIRouter(
    prefix="/phases_info",
    responses={404: {"description": "Not found"}},
)
AcrobaticsPhaseRouter().register(phase_router)
GenericOCPObjectiveRouter(AcrobaticsOCPData).register(phase_router)
GenericOCPConstraintRouter(AcrobaticsOCPData).register(phase_router)
GenericControlVariableRouter(AcrobaticsOCPData).register(phase_router)
GenericStateVariableRouter(AcrobaticsOCPData).register(phase_router)

router.include_router(phase_router)

router.include_router(acrobatics_code_generation_router)
