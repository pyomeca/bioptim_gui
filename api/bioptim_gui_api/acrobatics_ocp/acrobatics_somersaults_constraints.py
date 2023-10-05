from fastapi import APIRouter, HTTPException

import bioptim_gui_api.penalty.penalty_config as penalty_config
from bioptim_gui_api.acrobatics_ocp.acrobatics_responses import *
from bioptim_gui_api.acrobatics_ocp.acrobatics_utils import (
    read_acrobatics_data,
    update_acrobatics_data,
)
from bioptim_gui_api.penalty.penalty_utils import constraint_arguments

router = APIRouter()

# constraints endpoints


@router.get("/{somersault_index}/constraints", response_model=list)
def get_constraints(somersault_index: int):
    somersaults_info = read_acrobatics_data("somersaults_info")
    constraints = somersaults_info[somersault_index]["constraints"]
    return constraints


@router.post("/{somersault_index}/constraints", response_model=list)
def add_constraint(somersault_index: int):
    somersaults_info = read_acrobatics_data("somersaults_info")
    constraints = somersaults_info[somersault_index]["constraints"]
    constraints.append(penalty_config.DefaultPenaltyConfig.default_constraint)
    somersaults_info[somersault_index]["constraints"] = constraints
    update_acrobatics_data("somersaults_info", somersaults_info)
    return constraints


@router.get(
    "/{somersault_index}/constraints/{constraint_index}",
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
    "/{somersault_index}/constraints/{constraint_index}",
    response_model=list,
)
def delete_constraint(somersault_index: int, constraint_index: int):
    somersaults_info = read_acrobatics_data("somersaults_info")
    constraints = somersaults_info[somersault_index]["constraints"]
    constraints.pop(constraint_index)
    somersaults_info[somersault_index]["constraints"] = constraints
    update_acrobatics_data("somersaults_info", somersaults_info)
    return constraints


# common arguments


@router.put(
    "/{somersault_index}/constraints/{constraint_index}/penalty_type",
    response_model=dict,
)
def put_constraint_penalty_type(
    somersault_index: int, constraint_index: int, penalty_type: ConstraintFcnRequest
):
    penalty_type_value = penalty_type.penalty_type
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index]["constraints"][constraint_index][
        "penalty_type"
    ] = penalty_type_value

    arguments = constraint_arguments(penalty_type.penalty_type)
    somersaults_info[somersault_index]["constraints"][constraint_index][
        "arguments"
    ] = arguments

    update_acrobatics_data("somersaults_info", somersaults_info)
    data = read_acrobatics_data()
    return data["somersaults_info"][somersault_index]["constraints"][constraint_index]


@router.put(
    "/{somersault_index}/constraints/{constraint_index}/nodes",
    response_model=NodesResponse,
)
def put_constraint_nodes(
    somersault_index: int, constraint_index: int, nodes: NodesRequest
):
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index]["constraints"][constraint_index][
        "nodes"
    ] = nodes.nodes.value
    update_acrobatics_data("somersaults_info", somersaults_info)
    return NodesResponse(nodes=nodes.nodes)


@router.put(
    "/{somersault_index}/constraints/{constraint_index}/quadratic",
    response_model=QuadraticResponse,
)
def put_constraint_quadratic(
    somersault_index: int, constraint_index: int, quadratic: QuadraticRequest
):
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index]["constraints"][constraint_index][
        "quadratic"
    ] = quadratic.quadratic
    update_acrobatics_data("somersaults_info", somersaults_info)
    return QuadraticResponse(quadratic=quadratic.quadratic)


@router.put(
    "/{somersault_index}/constraints/{constraint_index}/expand",
    response_model=ExpandResponse,
)
def put_constraint_expand(
    somersault_index: int, constraint_index: int, expand: ExpandRequest
):
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index]["constraints"][constraint_index][
        "expand"
    ] = expand.expand
    update_acrobatics_data("somersaults_info", somersaults_info)
    return ExpandResponse(expand=expand.expand)


@router.put(
    "/{somersault_index}/constraints/{constraint_index}/target",
    response_model=TargetResponse,
)
def put_constraint_target(
    somersault_index: int, constraint_index: int, target: TargetRequest
):
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index]["constraints"][constraint_index][
        "target"
    ] = target.target
    update_acrobatics_data("somersaults_info", somersaults_info)
    return TargetResponse(target=target.target)


@router.put(
    "/{somersault_index}/constraints/{constraint_index}/derivative",
    response_model=DerivativeResponse,
)
def put_constraint_derivative(
    somersault_index: int, constraint_index: int, derivative: DerivativeRequest
):
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index]["constraints"][constraint_index][
        "derivative"
    ] = derivative.derivative
    update_acrobatics_data("somersaults_info", somersaults_info)
    return DerivativeResponse(derivative=derivative.derivative)


@router.put(
    "/{somersault_index}/constraints/{constraint_index}/integration_rule",
    response_model=IntegrationRuleResponse,
)
def put_constraint_integration_rule(
    somersault_index: int,
    constraint_index: int,
    integration_rule: IntegrationRuleRequest,
):
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index]["constraints"][constraint_index][
        "integration_rule"
    ] = integration_rule.integration_rule.value
    update_acrobatics_data("somersaults_info", somersaults_info)
    return IntegrationRuleResponse(integration_rule=integration_rule.integration_rule)


@router.put(
    "/{somersault_index}/constraints/{constraint_index}/multi_thread",
    response_model=MultiThreadResponse,
)
def put_constraint_multi_thread(
    somersault_index: int, constraint_index: int, multi_thread: MultiThreadRequest
):
    somersaults_info = read_acrobatics_data("somersaults_info")
    somersaults_info[somersault_index]["constraints"][constraint_index][
        "multi_thread"
    ] = multi_thread.multi_thread
    update_acrobatics_data("somersaults_info", somersaults_info)
    return MultiThreadResponse(multi_thread=multi_thread.multi_thread)


@router.get(
    "/{somersault_index}/constraints/{constraint_index}/arguments/{key}",
    response_model=ArgumentResponse,
)
def get_constraint_arguments(somersault_index: int, constraint_index: int, key: str):
    somersaults_info = read_acrobatics_data("somersaults_info")
    arguments = somersaults_info[somersault_index]["constraints"][constraint_index][
        "arguments"
    ]

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
    "/{somersault_index}/constraints/{constraint_index}/arguments/{key}",
    response_model=ArgumentResponse,
)
def put_constraint_arguments(
    somersault_index: int,
    constraint_index: int,
    key: str,
    argument_req: ArgumentRequest,
):
    somersaults_info = read_acrobatics_data("somersaults_info")
    arguments = somersaults_info[somersault_index]["constraints"][constraint_index][
        "arguments"
    ]

    for argument in arguments:
        if argument["name"] == key:
            argument["type"] = argument_req.type
            argument["value"] = argument_req.value

            somersaults_info[somersault_index]["constraints"][constraint_index][
                "arguments"
            ] = arguments
            update_acrobatics_data("somersaults_info", somersaults_info)

            return ArgumentResponse(
                key=key, type=argument["type"], value=argument["value"]
            )
    raise HTTPException(
        status_code=404,
        detail=f"{key} not found in arguments of constraint {constraint_index}",
    )
