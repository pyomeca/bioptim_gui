from fastapi import APIRouter, HTTPException

import bioptim_gui_api.penalty.misc.penalty_config as penalty_config
from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics_responses import *
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_utils import (
    read_acrobatics_data,
    update_acrobatics_data,
)
from bioptim_gui_api.penalty.misc.penalty_utils import obj_arguments

router = APIRouter()

# objectives endpoints


@router.get("/{phase_index}/objectives", response_model=list)
def get_objectives(phase_index: int):
    phases_info = read_acrobatics_data("phases_info")
    objectives = phases_info[phase_index]["objectives"]
    return objectives


@router.post("/{phase_index}/objectives", response_model=list)
def add_objective(phase_index: int):
    phases_info = read_acrobatics_data("phases_info")
    objectives = phases_info[phase_index]["objectives"]
    objectives.append(penalty_config.DefaultPenaltyConfig.default_objective)
    phases_info[phase_index]["objectives"] = objectives
    update_acrobatics_data("phases_info", phases_info)
    return objectives


@router.get(
    "/{phase_index}/objectives/{objective_index}",
    response_model=list,
)
def get_objective_dropdown_list(phase_index: int, objective_index: int):
    phases_info = read_acrobatics_data("phases_info")
    objective = phases_info[phase_index]["objectives"][objective_index]
    weight = objective["weight"]

    if weight > 0:
        return penalty_config.DefaultPenaltyConfig.min_to_original_dict.keys()
    else:
        return penalty_config.DefaultPenaltyConfig.max_to_original_dict.keys()


@router.delete(
    "/{phase_index}/objectives/{objective_index}",
    response_model=list,
)
def delete_objective(phase_index: int, objective_index: int):
    phases_info = read_acrobatics_data("phases_info")
    objectives = phases_info[phase_index]["objectives"]
    objectives.pop(objective_index)
    phases_info[phase_index]["objectives"] = objectives
    update_acrobatics_data("phases_info", phases_info)
    return objectives


@router.put(
    "/{phase_index}/objectives/{objective_index}/objective_type",
    response_model=dict,
)
def put_objective_type(phase_index: int, objective_index: int, objective_type: ObjectiveTypeRequest):
    phases_info = read_acrobatics_data("phases_info")
    phases_info[phase_index]["objectives"][objective_index]["objective_type"] = objective_type.objective_type.value

    objective_type_value = objective_type.objective_type.value
    penalty_type = phases_info[phase_index]["objectives"][objective_index]["penalty_type"]

    weight = phases_info[phase_index]["objectives"][objective_index]["weight"]

    if weight > 0:
        penalty_type = penalty_config.DefaultPenaltyConfig.min_to_original_dict[penalty_type]
    else:
        penalty_type = penalty_config.DefaultPenaltyConfig.max_to_original_dict[penalty_type]

    arguments = obj_arguments(objective_type_value, penalty_type)

    phases_info[phase_index]["objectives"][objective_index]["arguments"] = arguments

    update_acrobatics_data("phases_info", phases_info)
    data = read_acrobatics_data()
    return data["phases_info"][phase_index]["objectives"][objective_index]


# common arguments


@router.put(
    "/{phase_index}/objectives/{objective_index}/penalty_type",
    response_model=dict,
)
def put_objective_penalty_type(phase_index: int, objective_index: int, penalty_type: ObjectiveFcnRequest):
    penalty_type_value = penalty_type.penalty_type
    phases_info = read_acrobatics_data("phases_info")

    phases_info[phase_index]["objectives"][objective_index]["penalty_type"] = penalty_type_value

    objective_type = phases_info[phase_index]["objectives"][objective_index]["objective_type"]
    weight = phases_info[phase_index]["objectives"][objective_index]["weight"]

    if weight > 0:
        penalty_type_value = penalty_config.DefaultPenaltyConfig.min_to_original_dict[penalty_type_value]
    else:
        penalty_type_value = penalty_config.DefaultPenaltyConfig.max_to_original_dict[penalty_type_value]

    try:
        arguments = obj_arguments(objective_type=objective_type, penalty_type=penalty_type_value)
    except:
        other_objective_type = "lagrange" if objective_type == "mayer" else "mayer"
        phases_info[phase_index]["objectives"][objective_index]["objective_type"] = other_objective_type
        arguments = obj_arguments(objective_type=other_objective_type, penalty_type=penalty_type_value)

    phases_info[phase_index]["objectives"][objective_index]["arguments"] = arguments

    update_acrobatics_data("phases_info", phases_info)

    data = read_acrobatics_data()
    return data["phases_info"][phase_index]["objectives"][objective_index]


@router.put(
    "/{phase_index}/objectives/{objective_index}/nodes",
    response_model=NodesResponse,
)
def put_objective_nodes(phase_index: int, objective_index: int, nodes: NodesRequest):
    phases_info = read_acrobatics_data("phases_info")
    phases_info[phase_index]["objectives"][objective_index]["nodes"] = nodes.nodes.value
    update_acrobatics_data("phases_info", phases_info)
    return NodesResponse(nodes=nodes.nodes)


@router.put(
    "/{phase_index}/objectives/{objective_index}/quadratic",
    response_model=QuadraticResponse,
)
def put_objective_quadratic(phase_index: int, objective_index: int, quadratic: QuadraticRequest):
    phases_info = read_acrobatics_data("phases_info")
    phases_info[phase_index]["objectives"][objective_index]["quadratic"] = quadratic.quadratic
    update_acrobatics_data("phases_info", phases_info)
    return QuadraticResponse(quadratic=quadratic.quadratic)


@router.put(
    "/{phase_index}/objectives/{objective_index}/expand",
    response_model=ExpandResponse,
)
def put_objective_expand(phase_index: int, objective_index: int, expand: ExpandRequest):
    phases_info = read_acrobatics_data("phases_info")
    phases_info[phase_index]["objectives"][objective_index]["expand"] = expand.expand
    update_acrobatics_data("phases_info", phases_info)
    return ExpandResponse(expand=expand.expand)


@router.put(
    "/{phase_index}/objectives/{objective_index}/target",
    response_model=TargetResponse,
)
def put_objective_target(phase_index: int, objective_index: int, target: TargetRequest):
    phases_info = read_acrobatics_data("phases_info")
    phases_info[phase_index]["objectives"][objective_index]["target"] = target.target
    update_acrobatics_data("phases_info", phases_info)
    return TargetResponse(target=target.target)


@router.put(
    "/{phase_index}/objectives/{objective_index}/derivative",
    response_model=DerivativeResponse,
)
def put_objective_derivative(phase_index: int, objective_index: int, derivative: DerivativeRequest):
    phases_info = read_acrobatics_data("phases_info")
    phases_info[phase_index]["objectives"][objective_index]["derivative"] = derivative.derivative
    update_acrobatics_data("phases_info", phases_info)
    return DerivativeResponse(derivative=derivative.derivative)


@router.put(
    "/{phase_index}/objectives/{objective_index}/integration_rule",
    response_model=IntegrationRuleResponse,
)
def put_objective_integration_rule(
    phase_index: int,
    objective_index: int,
    integration_rule: IntegrationRuleRequest,
):
    phases_info = read_acrobatics_data("phases_info")
    phases_info[phase_index]["objectives"][objective_index][
        "integration_rule"
    ] = integration_rule.integration_rule.value
    update_acrobatics_data("phases_info", phases_info)
    return IntegrationRuleResponse(integration_rule=integration_rule.integration_rule)


@router.put(
    "/{phase_index}/objectives/{objective_index}/multi_thread",
    response_model=MultiThreadResponse,
)
def put_objective_multi_thread(phase_index: int, objective_index: int, multi_thread: MultiThreadRequest):
    phases_info = read_acrobatics_data("phases_info")
    phases_info[phase_index]["objectives"][objective_index]["multi_thread"] = multi_thread.multi_thread
    update_acrobatics_data("phases_info", phases_info)
    return MultiThreadResponse(multi_thread=multi_thread.multi_thread)


@router.put(
    "/{phase_index}/objectives/{objective_index}/weight",
    response_model=WeightResponse,
)
def put_objective_weight(phase_index: int, objective_index: int, weight: WeightRequest):
    phases_info = read_acrobatics_data("phases_info")
    old_weight = phases_info[phase_index]["objectives"][objective_index]["weight"]

    phases_info[phase_index]["objectives"][objective_index]["weight"] = (
        weight.weight if old_weight > 0 else -weight.weight
    )
    update_acrobatics_data("phases_info", phases_info)
    return WeightResponse(weight=weight.weight)


@router.put(
    "/{phase_index}/objectives/{objective_index}/weight/maximize",
    response_model=dict,
)
def put_objective_weight_maximize(phase_index: int, objective_index: int):
    phases_info = read_acrobatics_data("phases_info")
    old_weight = phases_info[phase_index]["objectives"][objective_index]["weight"]
    new_weight = -abs(old_weight)

    phases_info[phase_index]["objectives"][objective_index]["weight"] = new_weight
    penalty_type = phases_info[phase_index]["objectives"][objective_index]["penalty_type"]

    if old_weight > 0:
        phases_info[phase_index]["objectives"][objective_index][
            "penalty_type"
        ] = penalty_config.DefaultPenaltyConfig.min_to_max(penalty_type)

    update_acrobatics_data("phases_info", phases_info)
    return phases_info[phase_index]["objectives"][objective_index]


@router.put(
    "/{phase_index}/objectives/{objective_index}/weight/minimize",
    response_model=dict,
)
def put_objective_weight_minimize(phase_index: int, objective_index: int):
    phases_info = read_acrobatics_data("phases_info")
    old_weight = phases_info[phase_index]["objectives"][objective_index]["weight"]
    new_weight = abs(old_weight)

    phases_info[phase_index]["objectives"][objective_index]["weight"] = new_weight
    penalty_type = phases_info[phase_index]["objectives"][objective_index]["penalty_type"]

    if old_weight < 0:
        phases_info[phase_index]["objectives"][objective_index][
            "penalty_type"
        ] = penalty_config.DefaultPenaltyConfig.max_to_min(penalty_type)

    update_acrobatics_data("phases_info", phases_info)
    return phases_info[phase_index]["objectives"][objective_index]


@router.get(
    "/{phase_index}/objectives/{objective_index}/arguments/{key}",
    response_model=ArgumentResponse,
)
def get_objective_arguments(phase_index: int, objective_index: int, key: str):
    phases_info = read_acrobatics_data("phases_info")
    arguments = phases_info[phase_index]["objectives"][objective_index]["arguments"]

    for argument in arguments:
        if argument["name"] == key:
            return ArgumentResponse(key=key, type=argument["type"], value=argument["value"])

    raise HTTPException(
        status_code=404,
        detail=f"{key} not found in arguments of objective {objective_index}",
    )


@router.put(
    "/{phase_index}/objectives/{objective_index}/arguments/{key}",
    response_model=ArgumentResponse,
)
def put_objective_arguments(phase_index: int, objective_index: int, key: str, argument_req: ArgumentRequest):
    phases_info = read_acrobatics_data("phases_info")

    arguments = phases_info[phase_index]["objectives"][objective_index]["arguments"]

    for argument in arguments:
        if argument["name"] == key:
            argument["type"] = argument_req.type
            argument["value"] = argument_req.value

            phases_info[phase_index]["objectives"][objective_index]["arguments"] = arguments
            update_acrobatics_data("phases_info", phases_info)

            return ArgumentResponse(key=key, type=argument["type"], value=argument["value"])
    raise HTTPException(
        status_code=404,
        detail=f"{key} not found in arguments of objective {objective_index}",
    )
