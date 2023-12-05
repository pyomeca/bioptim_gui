from bioptim_gui_api.penalty.misc.constraint_printer import ConstraintPrinter


def test_regular_str_simple():
    constraint = ConstraintPrinter(
        phase=0,
        penalty_type="TIME_CONSTRAINT",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        arguments=[],
    )
    assert (
        str(constraint)
        == """constraint=ConstraintFcn.TIME_CONSTRAINT,
        node=Node.ALL,
        quadratic=False,
"""
    )


def test_regular_str_simple_phase():
    constraint = ConstraintPrinter(
        phase=30,
        penalty_type="TIME_CONSTRAINT",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        arguments=[],
    )
    assert (
        constraint.__str__(nb_phase=36)
        == """constraint=ConstraintFcn.TIME_CONSTRAINT,
        node=Node.ALL,
        quadratic=False,
        phase=30,
"""
    )


def test_regular_str_indent_8():
    constraint = ConstraintPrinter(
        phase=0,
        penalty_type="TIME_CONSTRAINT",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        arguments=[],
    )
    assert (
        constraint.__str__(indent=12, nb_phase=1)
        == """constraint=ConstraintFcn.TIME_CONSTRAINT,
            node=Node.ALL,
            quadratic=False,
"""
    )


def test_regular_str_indent_8_with_phase():
    constraint = ConstraintPrinter(
        phase=30,
        penalty_type="TIME_CONSTRAINT",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        arguments=[],
    )
    assert (
        constraint.__str__(indent=12, nb_phase=36)
        == """constraint=ConstraintFcn.TIME_CONSTRAINT,
            node=Node.ALL,
            quadratic=False,
            phase=30,
"""
    )


def test_regular_str_indent_8_with_phase_all():
    constraint = ConstraintPrinter(
        phase=30,
        penalty_type="SUPERIMPOSE_MARKERS",
        nodes="all",
        quadratic=False,
        expand=False,
        target=[1, 2],
        derivative=True,
        integration_rule="rectangle_right",
        multi_thread=True,
        arguments=[
            {"name": "min_bound", "value": -0.05, "type": "float"},
            {"name": "max_bound", "value": 0.05, "type": "float"},
            {"name": "first_marker", "value": "MiddleLeftHand", "type": "string"},
            {"name": "second_marker", "value": "TargetLeftHand", "type": "string"},
        ],
    )
    assert (
        constraint.__str__(indent=12, nb_phase=36)
        == """constraint=ConstraintFcn.SUPERIMPOSE_MARKERS,
            min_bound=-0.05,
            max_bound=0.05,
            first_marker="MiddleLeftHand",
            second_marker="TargetLeftHand",
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
