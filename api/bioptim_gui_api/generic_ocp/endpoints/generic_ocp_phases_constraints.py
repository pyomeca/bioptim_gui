from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_penalties import GenericOCPPenaltyRouter
from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig
from bioptim_gui_api.penalty.misc.penalty_utils import constraint_arguments


class GenericOCPConstraintRouter(GenericOCPPenaltyRouter):
    def __init__(self, data):
        super().__init__(data, "constraints")
        self.arg_getter = constraint_arguments
        self.default = DefaultPenaltyConfig.default_constraint

    def register_get_phase_penalty_list(self):
        @self.router.get("/{phase_index}/constraints/{constraint_index}", response_model=list)
        def get_constraints_dropdown_list():
            # we don't use all the available constraints for now
            return [
                "CUSTOM",
                "PROPORTIONAL_CONTROL",
                "PROPORTIONAL_STATE",
                "SUPERIMPOSE_MARKERS",
                "SUPERIMPOSE_MARKERS_VELOCITY",
                "TIME_CONSTRAINT",
                "TRACK_ANGULAR_MOMENTUM",
                "TRACK_COM_POSITION",
                "TRACK_COM_VELOCITY",
                "TRACK_CONTROL",
                "TRACK_LINEAR_MOMENTUM",
                "TRACK_MARKER_WITH_SEGMENT_AXIS",
                "TRACK_MARKERS",
                "TRACK_MARKERS_ACCELERATION",
                "TRACK_MARKERS_VELOCITY",
                "TRACK_POWER",
                "TRACK_QDDOT",
                "TRACK_SEGMENT_ROTATION",
                "TRACK_SEGMENT_VELOCITY",
                "TRACK_SEGMENT_WITH_CUSTOM_RT",
                "TRACK_STATE",
                "TRACK_VECTOR_ORIENTATIONS_FROM_MARKERS",
            ]
