from abc import ABC, abstractmethod

from fastapi import APIRouter, HTTPException

from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_requests import (
    ArgumentRequest,
    ConstraintFcnRequest,
    DerivativeRequest,
    ExpandRequest,
    IntegrationRuleRequest,
    MultiThreadRequest,
    NodesRequest,
    QuadraticRequest,
    TargetRequest,
)
from bioptim_gui_api.generic_ocp.endpoints.generic_ocp_responses import (
    ArgumentResponse,
    DerivativeResponse,
    ExpandResponse,
    IntegrationRuleResponse,
    MultiThreadResponse,
    NodesResponse,
    QuadraticResponse,
    TargetResponse,
)


class GenericOCPPenaltyRouter(ABC):
    def __init__(self, data, penalty_type: str):
        self.router = None
        self.data = data
        self.penalty_type = penalty_type
        self.arg_getter = None
        self.default = None

    def register(self, route: APIRouter) -> None:
        self.router = route
        self.register_get_phase_penalties()
        self.register_post_phase_penalties()
        self.register_get_phase_penalty_list()
        self.register_delete_phase_penalty()
        self.register_put_penalty_type()
        self.register_put_penalty_nodes()
        self.register_put_penalty_quadratic()
        self.register_put_penalty_expand()
        self.register_put_penalty_target()
        self.register_put_penalty_derivative()
        self.register_put_penalty_integration_rule()
        self.register_put_penalty_multi_thread()
        self.register_get_penalty_arguments()
        self.register_put_penalty_arguments()

    def register_get_phase_penalties(self):
        @self.router.get(f"/{{phase_index}}/{self.penalty_type}", response_model=list)
        def get_penalties(phase_index: int):
            phases_info = self.data.read_data("phases_info")
            penalties = phases_info[phase_index][self.penalty_type]
            return penalties

    def register_post_phase_penalties(self):
        @self.router.post(f"/{{phase_index}}/{self.penalty_type}", response_model=list)
        def add_penalty(phase_index: int):
            phases_info = self.data.read_data("phases_info")
            penalties = phases_info[phase_index][self.penalty_type]
            penalties.append(self.default)
            phases_info[phase_index][self.penalty_type] = penalties
            self.data.update_data("phases_info", phases_info)
            return penalties

    @abstractmethod
    def register_get_phase_penalty_list(self):
        ...

    def register_delete_phase_penalty(self):
        @self.router.delete(f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}", response_model=list)
        def delete_penalty(phase_index: int, penalty_index: int):
            phases_info = self.data.read_data("phases_info")
            penalties = phases_info[phase_index][self.penalty_type]
            penalties.pop(penalty_index)
            phases_info[phase_index][self.penalty_type] = penalties
            self.data.update_data("phases_info", phases_info)
            return penalties

        # common arguments

    def register_put_penalty_type(self):
        @self.router.put(f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/penalty_type", response_model=dict)
        def put_penalty_penalty_type(phase_index: int, penalty_index: int, penalty_type: ConstraintFcnRequest):
            penalty_type_value = penalty_type.penalty_type
            phases_info = self.data.read_data("phases_info")
            phases_info[phase_index][self.penalty_type][penalty_index]["penalty_type"] = penalty_type_value

            arguments = self.arg_getter(penalty_type_value)
            phases_info[phase_index][self.penalty_type][penalty_index]["arguments"] = arguments

            self.data.update_data("phases_info", phases_info)
            data = self.data.read_data()
            return data["phases_info"][phase_index][self.penalty_type][penalty_index]

    def register_put_penalty_nodes(self):
        @self.router.put(f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/nodes", response_model=NodesResponse)
        def put_penalty_nodes(phase_index: int, penalty_index: int, nodes: NodesRequest):
            phases_info = self.data.read_data("phases_info")
            phases_info[phase_index][self.penalty_type][penalty_index]["nodes"] = nodes.nodes.value
            self.data.update_data("phases_info", phases_info)
            return NodesResponse(nodes=nodes.nodes)

    def register_put_penalty_quadratic(self):
        @self.router.put(
            f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/quadratic", response_model=QuadraticResponse
        )
        def put_penalty_quadratic(phase_index: int, penalty_index: int, quadratic: QuadraticRequest):
            phases_info = self.data.read_data("phases_info")
            phases_info[phase_index][self.penalty_type][penalty_index]["quadratic"] = quadratic.quadratic
            self.data.update_data("phases_info", phases_info)
            return QuadraticResponse(quadratic=quadratic.quadratic)

    def register_put_penalty_expand(self):
        @self.router.put(
            f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/expand", response_model=ExpandResponse
        )
        def put_penalty_expand(phase_index: int, penalty_index: int, expand: ExpandRequest):
            phases_info = self.data.read_data("phases_info")
            phases_info[phase_index][self.penalty_type][penalty_index]["expand"] = expand.expand
            self.data.update_data("phases_info", phases_info)
            return ExpandResponse(expand=expand.expand)

    def register_put_penalty_target(self):
        @self.router.put(
            f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/target", response_model=TargetResponse
        )
        def put_penalty_target(phase_index: int, penalty_index: int, target: TargetRequest):
            phases_info = self.data.read_data("phases_info")
            phases_info[phase_index][self.penalty_type][penalty_index]["target"] = target.target
            self.data.update_data("phases_info", phases_info)
            return TargetResponse(target=target.target)

    def register_put_penalty_derivative(self):
        @self.router.put(
            f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/derivative", response_model=DerivativeResponse
        )
        def put_penalty_derivative(phase_index: int, penalty_index: int, derivative: DerivativeRequest):
            phases_info = self.data.read_data("phases_info")
            phases_info[phase_index][self.penalty_type][penalty_index]["derivative"] = derivative.derivative
            self.data.update_data("phases_info", phases_info)
            return DerivativeResponse(derivative=derivative.derivative)

    def register_put_penalty_integration_rule(self):
        @self.router.put(
            f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/integration_rule",
            response_model=IntegrationRuleResponse,
        )
        def put_penalty_integration_rule(
            phase_index: int,
            penalty_index: int,
            integration_rule: IntegrationRuleRequest,
        ):
            phases_info = self.data.read_data("phases_info")
            phases_info[phase_index][self.penalty_type][penalty_index][
                "integration_rule"
            ] = integration_rule.integration_rule.value
            self.data.update_data("phases_info", phases_info)
            return IntegrationRuleResponse(integration_rule=integration_rule.integration_rule)

    def register_put_penalty_multi_thread(self):
        @self.router.put(
            f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/multi_thread", response_model=MultiThreadResponse
        )
        def put_penalty_multi_thread(phase_index: int, penalty_index: int, multi_thread: MultiThreadRequest):
            phases_info = self.data.read_data("phases_info")
            phases_info[phase_index][self.penalty_type][penalty_index]["multi_thread"] = multi_thread.multi_thread
            self.data.update_data("phases_info", phases_info)
            return MultiThreadResponse(multi_thread=multi_thread.multi_thread)

    def register_get_penalty_arguments(self):
        @self.router.get(
            f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/arguments/{{key}}", response_model=ArgumentResponse
        )
        def get_penalty_arguments(phase_index: int, penalty_index: int, key: str):
            phases_info = self.data.read_data("phases_info")
            arguments = phases_info[phase_index][self.penalty_type][penalty_index]["arguments"]

            for argument in arguments:
                if argument["name"] == key:
                    return ArgumentResponse(key=key, type=argument["type"], value=argument["value"])

            raise HTTPException(
                status_code=404,
                detail=f"{key} not found in arguments of penalty {penalty_index}",
            )

    def register_put_penalty_arguments(self):
        @self.router.put(
            f"/{{phase_index}}/{self.penalty_type}/{{penalty_index}}/arguments/{{key}}", response_model=ArgumentResponse
        )
        def put_penalty_arguments(
            phase_index: int,
            penalty_index: int,
            key: str,
            argument_req: ArgumentRequest,
        ):
            phases_info = self.data.read_data("phases_info")
            arguments = phases_info[phase_index][self.penalty_type][penalty_index]["arguments"]

            for argument in arguments:
                if argument["name"] == key:
                    argument["type"] = argument_req.type
                    argument["value"] = argument_req.value

                    phases_info[phase_index][self.penalty_type][penalty_index]["arguments"] = arguments
                    self.data.update_data("phases_info", phases_info)

                    return ArgumentResponse(key=key, type=argument["type"], value=argument["value"])
            raise HTTPException(
                status_code=404,
                detail=f"{key} not found in arguments of {self.penalty_type} {penalty_index}",
            )
