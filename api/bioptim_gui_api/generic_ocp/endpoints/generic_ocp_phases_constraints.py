from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_penalties import GenericOCPPenaltyRouter
from bioptim_gui_api.penalty.endpoints.penalty import get_constraints
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
            return get_constraints()
