import pytest

from bioptim_gui_api.penalty.misc.constraint_printer import ConstraintPrinter


def test_custom_str_simple():
    constraint = ConstraintPrinter(
        phase=0,
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        str(constraint)
        == """my_func,
        node=Node.ALL,
        quadratic=False,
"""
    )


def test_custom_str_simple_phase():
    constraint = ConstraintPrinter(
        phase=30,
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        constraint.__str__(nb_phase=36)
        == """my_func,
        node=Node.ALL,
        quadratic=False,
        phase=30,
"""
    )


def test_custom_str_indent_8():
    constraint = ConstraintPrinter(
        phase=0,
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        constraint.__str__(indent=12, nb_phase=1)
        == """my_func,
            node=Node.ALL,
            quadratic=False,
"""
    )


def test_custom_str_indent_8_with_phase():
    constraint = ConstraintPrinter(
        phase=30,
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        constraint.__str__(indent=12, nb_phase=36)
        == """my_func,
            node=Node.ALL,
            quadratic=False,
            phase=30,
"""
    )


def test_custom_str_indent_8_with_phase_all():
    constraint = ConstraintPrinter(
        phase=30,
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=False,
        target=[1, 2],
        derivative=True,
        integration_rule="rectangle_right",
        multi_thread=True,
        arguments=[{"name": "function", "value": "my_func", "type": "function"}],
    )
    assert (
        constraint.__str__(indent=12, nb_phase=36)
        == """my_func,
            node=Node.ALL,
            quadratic=False,
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
            "SUPERIMPOSE_MARKERS",
            [{"name": "function", "value": "my_func", "type": "function"}],
        ),  # bad penalty_type
    ],
)
def test_custom_str_assert_error(penalty_type, arguments):
    constraint = ConstraintPrinter(
        phase=0,
        penalty_type=penalty_type,
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        arguments=arguments,
    )

    with pytest.raises(AssertionError):
        constraint._custom_str()


def test_custom_multiple_arguments():
    objective = ConstraintPrinter(
        phase=30,
        penalty_type="CUSTOM",
        nodes="all",
        quadratic=False,
        expand=False,
        target=[1, 2],
        derivative=True,
        integration_rule="rectangle_right",
        multi_thread=True,
        arguments=[
            {"name": "function2", "value": "haha", "type": "str"},
            {"name": "function", "value": "my_func", "type": "function"},
            {"name": "additional", "value": "1", "type": "int"},
        ],
    )
    assert (
        objective.__str__(indent=12, nb_phase=36)
        == """my_func,
            function2="haha",
            additional=1,
            node=Node.ALL,
            quadratic=False,
            expand=False,
            target=[1, 2],
            derivative=True,
            integration_rule=QuadratureRule.RECTANGLE_RIGHT,
            multi_thread=True,
            phase=30,
"""
    )
