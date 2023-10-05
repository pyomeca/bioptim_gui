from fastapi import APIRouter, HTTPException

import bioptim_gui_api.penalty.penalty_config as penalty_config
from bioptim_gui_api.generic_ocp.generic_ocp_responses import *
from bioptim_gui_api.generic_ocp.generic_ocp_utils import (
    read_generic_ocp_data,
    update_generic_ocp_data,
)
from bioptim_gui_api.penalty.penalty_utils import constraint_arguments

router = APIRouter()

# constraints endpoints


@router.get("/{phase_index}/constraints", response_model=list)
def get_constraints(phase_index: int):
    phases_info = read_generic_ocp_data("phases_info")
    constraints = phases_info[phase_index]["constraints"]
    return constraints


@router.post("/{phase_index}/constraints", response_model=list)
def add_constraint(phase_index: int):
    phases_info = read_generic_ocp_data("phases_info")
    constraints = phases_info[phase_index]["constraints"]
    constraints.append(penalty_config.DefaultPenaltyConfig.default_constraint)
    phases_info[phase_index]["constraints"] = constraints
    update_generic_ocp_data("phases_info", phases_info)
    return constraints


@router.get(
    "/{phase_index}/constraints/{constraint_index}",
    response_model=list,
)
def get_constraints_dropdown_list():
    # we don't use all the available constraints for now
    return [
        "CONTINUITY",
        "TIME_CONSTRAINT",
    ]
    # if all constraints have to be implemented
    # return [e.name for e in ConstraintFcn]


@router.delete(
    "/{phase_index}/constraints/{constraint_index}",
    response_model=list,
)
def delete_constraint(phase_index: int, constraint_index: int):
    phases_info = read_generic_ocp_data("phases_info")
    constraints = phases_info[phase_index]["constraints"]
    constraints.pop(constraint_index)
    phases_info[phase_index]["constraints"] = constraints
    update_generic_ocp_data("phases_info", phases_info)
    return constraints


# common arguments


@router.put(
    "/{phase_index}/constraints/{constraint_index}/penalty_type",
    response_model=dict,
)
def put_constraint_penalty_type(
    phase_index: int, constraint_index: int, penalty_type: ConstraintFcnRequest
):
    penalty_type_value = penalty_type.penalty_type
    phases_info = read_generic_ocp_data("phases_info")
    phases_info[phase_index]["constraints"][constraint_index][
        "penalty_type"
    ] = penalty_type_value

    arguments = constraint_arguments(penalty_type.penalty_type)
    phases_info[phase_index]["constraints"][constraint_index]["arguments"] = arguments

    update_generic_ocp_data("phases_info", phases_info)
    data = read_generic_ocp_data()
    return data["phases_info"][phase_index]["constraints"][constraint_index]


@router.put(
    "/{phase_index}/constraints/{constraint_index}/nodes",
    response_model=NodesResponse,
)
def put_constraint_nodes(phase_index: int, constraint_index: int, nodes: NodesRequest):
    phases_info = read_generic_ocp_data("phases_info")
    phases_info[phase_index]["constraints"][constraint_index][
        "nodes"
    ] = nodes.nodes.value
    update_generic_ocp_data("phases_info", phases_info)
    return NodesResponse(nodes=nodes.nodes)


@router.put(
    "/{phase_index}/constraints/{constraint_index}/quadratic",
    response_model=QuadraticResponse,
)
def put_constraint_quadratic(
    phase_index: int, constraint_index: int, quadratic: QuadraticRequest
):
    phases_info = read_generic_ocp_data("phases_info")
    phases_info[phase_index]["constraints"][constraint_index][
        "quadratic"
    ] = quadratic.quadratic
    update_generic_ocp_data("phases_info", phases_info)
    return QuadraticResponse(quadratic=quadratic.quadratic)


@router.put(
    "/{phase_index}/constraints/{constraint_index}/expand",
    response_model=ExpandResponse,
)
def put_constraint_expand(
    phase_index: int, constraint_index: int, expand: ExpandRequest
):
    phases_info = read_generic_ocp_data("phases_info")
    phases_info[phase_index]["constraints"][constraint_index]["expand"] = expand.expand
    update_generic_ocp_data("phases_info", phases_info)
    return ExpandResponse(expand=expand.expand)


@router.put(
    "/{phase_index}/constraints/{constraint_index}/target",
    response_model=TargetResponse,
)
def put_constraint_target(
    phase_index: int, constraint_index: int, target: TargetRequest
):
    phases_info = read_generic_ocp_data("phases_info")
    phases_info[phase_index]["constraints"][constraint_index]["target"] = target.target
    update_generic_ocp_data("phases_info", phases_info)
    return TargetResponse(target=target.target)


@router.put(
    "/{phase_index}/constraints/{constraint_index}/derivative",
    response_model=DerivativeResponse,
)
def put_constraint_derivative(
    phase_index: int, constraint_index: int, derivative: DerivativeRequest
):
    phases_info = read_generic_ocp_data("phases_info")
    phases_info[phase_index]["constraints"][constraint_index][
        "derivative"
    ] = derivative.derivative
    update_generic_ocp_data("phases_info", phases_info)
    return DerivativeResponse(derivative=derivative.derivative)


@router.put(
    "/{phase_index}/constraints/{constraint_index}/integration_rule",
    response_model=IntegrationRuleResponse,
)
def put_constraint_integration_rule(
    phase_index: int,
    constraint_index: int,
    integration_rule: IntegrationRuleRequest,
):
    phases_info = read_generic_ocp_data("phases_info")
    phases_info[phase_index]["constraints"][constraint_index][
        "integration_rule"
    ] = integration_rule.integration_rule.value
    update_generic_ocp_data("phases_info", phases_info)
    return IntegrationRuleResponse(integration_rule=integration_rule.integration_rule)


@router.put(
    "/{phase_index}/constraints/{constraint_index}/multi_thread",
    response_model=MultiThreadResponse,
)
def put_constraint_multi_thread(
    phase_index: int, constraint_index: int, multi_thread: MultiThreadRequest
):
    phases_info = read_generic_ocp_data("phases_info")
    phases_info[phase_index]["constraints"][constraint_index][
        "multi_thread"
    ] = multi_thread.multi_thread
    update_generic_ocp_data("phases_info", phases_info)
    return MultiThreadResponse(multi_thread=multi_thread.multi_thread)


@router.get(
    "/{phase_index}/constraints/{constraint_index}/arguments/{key}",
    response_model=ArgumentResponse,
)
def get_constraint_arguments(phase_index: int, constraint_index: int, key: str):
    phases_info = read_generic_ocp_data("phases_info")
    arguments = phases_info[phase_index]["constraints"][constraint_index]["arguments"]

    for argument in arguments:
        if argument["name"] == key:
            return ArgumentResponse(
                key=key, type=argument["type"], value=argument["value"]
            )

    raise HTTPException(
        status_code=404,
        detail=f"{key} not found in arguments of constraint {constraint_index}",
    )


@router.put(
    "/{phase_index}/constraints/{constraint_index}/arguments/{key}",
    response_model=ArgumentResponse,
)
def put_constraint_arguments(
    phase_index: int,
    constraint_index: int,
    key: str,
    argument_req: ArgumentRequest,
):
    phases_info = read_generic_ocp_data("phases_info")
    arguments = phases_info[phase_index]["constraints"][constraint_index]["arguments"]

    for argument in arguments:
        if argument["name"] == key:
            argument["type"] = argument_req.type
            argument["value"] = argument_req.value

            phases_info[phase_index]["constraints"][constraint_index][
                "arguments"
            ] = arguments
            update_generic_ocp_data("phases_info", phases_info)

            return ArgumentResponse(
                key=key, type=argument["type"], value=argument["value"]
            )
    raise HTTPException(
        status_code=404,
        detail=f"{key} not found in arguments of constraint {constraint_index}",
    )
