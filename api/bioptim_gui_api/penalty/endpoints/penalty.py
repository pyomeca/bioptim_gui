from bioptim import QuadratureRule
from fastapi import APIRouter

from bioptim_gui_api.acrobatics_ocp.misc.enums import Node
from bioptim_gui_api.penalty.misc.penalty_config import DefaultPenaltyConfig

router = APIRouter(
    prefix="/penalties",
    tags=["penalties"],
    responses={404: {"description": "Not found"}},
)


def get_spaced_capitalized(enum) -> list:
    return [e.value.replace("_", " ").capitalize() for e in enum]


@router.get("/nodes", response_model=list[str])
def get_nodes():
    return get_spaced_capitalized(Node)


@router.get("/integration_rules", response_model=list[str])
def get_integration_rules():
    return get_spaced_capitalized(QuadratureRule)


@router.get("/objectives", response_model=dict)
def get_objectives():
    return {
        "minimize": list(DefaultPenaltyConfig.min_to_original_dict.keys()),
        "maximize": list(DefaultPenaltyConfig.max_to_original_dict.keys()),
    }


@router.get("/constraints", response_model=list[str])
def get_constraints():
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


@router.get("/available_values", response_model=dict)
def get_available_values():
    return {
        "nodes": get_nodes(),
        "objectives": get_objectives(),
        "constraints": get_constraints(),
        "integration_rules": get_integration_rules(),
    }
