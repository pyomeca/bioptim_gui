import pytest
from bioptim import ObjectiveFcn, ConstraintFcn
from fastapi.exceptions import HTTPException

from bioptim_gui_api.penalty.penalty_utils import (
    get_args,
    format_arg_type,
    obj_arguments,
    constraint_arguments,
)


@pytest.mark.parametrize(
    "arg_type, expected",
    [
        ("int", "int"),
        ("float", "float"),
        ("str", "str"),
        ("int | str", "int | str"),
        ("list", "list"),
        ("<enum 'Axis'>", "Axis"),
        ("<class 'Axis'>", "Axis"),
        ("<class 'int | str'>", "int | str"),
    ],
)
def test_format_arg_type(arg_type, expected):
    assert format_arg_type(arg_type) == expected


@pytest.mark.parametrize(
    "penalty_fcn, expected",
    [
        (
            ObjectiveFcn.Mayer.MINIMIZE_TIME,
            [
                {"name": "min_bound", "value": None, "type": "float"},
                {"name": "max_bound", "value": None, "type": "float"},
            ],
        ),
        (ObjectiveFcn.Lagrange.MINIMIZE_TIME, []),
        (
            ObjectiveFcn.Lagrange.MINIMIZE_STATE,
            [{"name": "key", "value": None, "type": "str"}],
        ),
        (
            ObjectiveFcn.Lagrange.TRACK_MARKER_WITH_SEGMENT_AXIS,
            [
                {"name": "marker", "value": None, "type": "int | str"},
                {"name": "segment", "value": None, "type": "int | str"},
                {"name": "axis", "value": None, "type": "Axis"},
            ],
        ),
        (
            ObjectiveFcn.Lagrange.PROPORTIONAL_STATE,
            [
                {"name": "key", "value": None, "type": "str"},
                {"name": "first_dof", "value": None, "type": "int"},
                {"name": "second_dof", "value": None, "type": "int"},
                {"name": "coef", "value": None, "type": "float"},
                {"name": "first_dof_intercept", "value": 0.0, "type": "float"},
                {"name": "second_dof_intercept", "value": 0.0, "type": "float"},
            ],
        ),
        (
            ObjectiveFcn.Lagrange.PROPORTIONAL_CONTROL,
            [
                {"name": "key", "value": None, "type": "str"},
                {"name": "first_dof", "value": None, "type": "int"},
                {"name": "second_dof", "value": None, "type": "int"},
                {"name": "coef", "value": None, "type": "float"},
                {"name": "first_dof_intercept", "value": 0.0, "type": "float"},
                {"name": "second_dof_intercept", "value": 0.0, "type": "float"},
            ],
        ),
        (ConstraintFcn.CONTINUITY, []),
    ],
)
def test_get_args(penalty_fcn, expected):
    assert get_args(penalty_fcn) == expected


@pytest.mark.parametrize(
    "objective_fcn, objective_type, penalty_type",
    [
        (ObjectiveFcn.Mayer.MINIMIZE_TIME, "mayer", "MINIMIZE_TIME"),
        (ObjectiveFcn.Lagrange.MINIMIZE_TIME, "lagrange", "MINIMIZE_TIME"),
        (ObjectiveFcn.Lagrange.MINIMIZE_STATE, "lagrange", "MINIMIZE_STATE"),
        (
            ObjectiveFcn.Lagrange.TRACK_MARKER_WITH_SEGMENT_AXIS,
            "lagrange",
            "TRACK_MARKER_WITH_SEGMENT_AXIS",
        ),
        (ObjectiveFcn.Lagrange.PROPORTIONAL_STATE, "lagrange", "PROPORTIONAL_STATE"),
        (
            ObjectiveFcn.Lagrange.PROPORTIONAL_CONTROL,
            "lagrange",
            "PROPORTIONAL_CONTROL",
        ),
    ],
)
def test_obj_arguments(objective_fcn, objective_type, penalty_type):
    assert obj_arguments(objective_type, penalty_type) == get_args(objective_fcn)


@pytest.mark.parametrize(
    "constraint_fcn, penalty_type",
    [
        (ConstraintFcn.CONTINUITY, "CONTINUITY"),
    ],
)
def test_constraint_arguments(constraint_fcn, penalty_type):
    assert constraint_arguments(penalty_type) == get_args(constraint_fcn)


def test_bad_objective_fcn():
    with pytest.raises(HTTPException):
        obj_arguments("not_an_objective", "MINIMIZE_TIME")


def test_bad_constraint_fcn():
    with pytest.raises(HTTPException):
        constraint_arguments("NOT_IMPLEMENTED")
