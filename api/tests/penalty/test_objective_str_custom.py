import pytest

from bioptim_gui_api.penalty.objective import Objective


def test_custom_str_simple():
    objective = Objective(
        phase=0,
        objective_type="lagrange",
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        weight=1.0,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        str(objective)
        == """my_func,
        custom_type=ObjectiveFcn.Lagrange,
        node=Node.ALL,
        quadratic=False,
        weight=1.0,
"""
    )


def test_custom_str_simple_phase():
    objective = Objective(
        phase=30,
        objective_type="lagrange",
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        weight=1.0,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        objective.__str__(nb_phase=36)
        == """my_func,
        custom_type=ObjectiveFcn.Lagrange,
        node=Node.ALL,
        quadratic=False,
        weight=1.0,
        phase=30,
"""
    )


def test_custom_str_indent_8():
    objective = Objective(
        phase=0,
        objective_type="lagrange",
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        weight=1.0,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        objective.__str__(indent=12, nb_phase=1)
        == """my_func,
            custom_type=ObjectiveFcn.Lagrange,
            node=Node.ALL,
            quadratic=False,
            weight=1.0,
"""
    )


def test_custom_str_indent_8_with_phase():
    objective = Objective(
        phase=30,
        objective_type="lagrange",
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        weight=1.0,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        objective.__str__(indent=12, nb_phase=36)
        == """my_func,
            custom_type=ObjectiveFcn.Lagrange,
            node=Node.ALL,
            quadratic=False,
            weight=1.0,
            phase=30,
"""
    )


def test_custom_str_indent_8_with_phase_all():
    objective = Objective(
        phase=30,
        objective_type="lagrange",
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=False,
        target=[1, 2],
        derivative=True,
        integration_rule="rectangle_right",
        multi_thread=True,
        weight=-10.0,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        objective.__str__(indent=12, nb_phase=36)
        == """my_func,
            custom_type=ObjectiveFcn.Lagrange,
            node=Node.ALL,
            quadratic=False,
            weight=-10.0,
            expand=False,
            target=[1, 2],
            derivative=True,
            integration_rule=QuadratureRule.RECTANGLE_RIGHT,
            multi_thread=True,
            phase=30,
"""
    )


@pytest.mark.parametrize(
    ("penalty_type", "arguments"),
    [
        (
            "MINIMIZE_STATE",
            [{"name": "function", "value": "my_func", "type": "function"}],
        ),  # bad penalty_type
        (
            "CUSTOM",
            [
                {"name": "function", "value": "my_func", "type": "function"},
                {"name": "function2", "value": "my_func", "type": "function"},
            ],
        ),  # bad argument length
        (
            "CUSTOM",
            [{"name": "bad", "value": "my_func", "type": "function"}],
        ),  # bad first argument name
        (
            "MINIMIZE_STATE",
            [
                {"name": "function1", "value": "my_func", "type": "bad"},
                {"name": "function2", "value": "my_func", "type": "bad"},
            ],
        ),  # combo
    ],
)
def test_custom_str_assert_error(penalty_type, arguments):
    objective = Objective(
        phase=0,
        objective_type="lagrange",
        penalty_type=penalty_type,
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        weight=1.0,
        arguments=arguments,
    )

    with pytest.raises(AssertionError):
        objective._custom_str()
