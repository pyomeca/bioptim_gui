from bioptim_gui_api.penalty.misc.objective_printer import ObjectivePrinter


def test_regular_str_simple():
    objective = ObjectivePrinter(
        phase=0,
        objective_type="lagrange",
        penalty_type="MINIMIZE_STATE",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        weight=1.0,
        arguments=[
            {"name": "key", "value": "q", "type": "string"},
            {"name": "index", "value": [1, 2], "type": "list"},
        ],
    )
    assert (
        objective.stringify()
        == """objective=ObjectiveFcn.Lagrange.MINIMIZE_STATE,
        weight=1.0,
        key="q",
        index=[1, 2],
        node=Node.ALL,
        quadratic=False,
"""
    )


def test_mayer_no_integration_rule():
    objective = ObjectivePrinter(
        phase=0,
        objective_type="mayer",
        penalty_type="MINIMIZE_STATE",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_right",
        multi_thread=False,
        weight=1.0,
        arguments=[
            {"name": "key", "value": "q", "type": "string"},
            {"name": "index", "value": [1, 2], "type": "list"},
        ],
    )
    assert (
        objective.stringify()
        == """objective=ObjectiveFcn.Mayer.MINIMIZE_STATE,
        weight=1.0,
        key="q",
        index=[1, 2],
        node=Node.ALL,
        quadratic=False,
"""
    )


def test_regular_str_simple_phase():
    objective = ObjectivePrinter(
        phase=30,
        objective_type="mayer",
        penalty_type="MINIMIZE_STATE",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        weight=1.0,
        arguments=[
            {"name": "key", "value": "q", "type": "string"},
            {"name": "index", "value": [1, 2], "type": "list"},
        ],
    )
    assert (
        objective.stringify()
        == """objective=ObjectiveFcn.Mayer.MINIMIZE_STATE,
        weight=1.0,
        key="q",
        index=[1, 2],
        node=Node.ALL,
        quadratic=False,
        phase=30,
"""
    )


def test_regular_str_indent_8():
    objective = ObjectivePrinter(
        phase=0,
        objective_type="lagrange",
        penalty_type="MINIMIZE_STATE",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        weight=1.0,
        arguments=[
            {"name": "key", "value": "q", "type": "string"},
            {"name": "index", "value": [1, 2], "type": "list"},
        ],
    )
    assert (
        objective.stringify(indent=12)
        == """objective=ObjectiveFcn.Lagrange.MINIMIZE_STATE,
            weight=1.0,
            key="q",
            index=[1, 2],
            node=Node.ALL,
            quadratic=False,
"""
    )


def test_regular_str_indent_8_with_phase():
    objective = ObjectivePrinter(
        phase=30,
        objective_type="lagrange",
        penalty_type="MINIMIZE_STATE",
        nodes="all",
        quadratic=False,
        expand=True,
        target=None,
        derivative=False,
        integration_rule="rectangle_left",
        multi_thread=False,
        weight=1.0,
        arguments=[
            {"name": "key", "value": "q", "type": "string"},
            {"name": "index", "value": [1, 2], "type": "list"},
        ],
    )
    assert (
        objective.stringify(indent=12)
        == """objective=ObjectiveFcn.Lagrange.MINIMIZE_STATE,
            weight=1.0,
            key="q",
            index=[1, 2],
            node=Node.ALL,
            quadratic=False,
            phase=30,
"""
    )


def test_regular_str_indent_8_with_phase_all():
    objective = ObjectivePrinter(
        phase=30,
        objective_type="lagrange",
        penalty_type="MAXIMIZE_STATE",
        nodes="all",
        quadratic=False,
        expand=False,
        target=[1, 2],
        derivative=True,
        integration_rule="rectangle_right",
        multi_thread=True,
        weight=-10.0,
        arguments=[
            {"name": "key", "value": "q", "type": "string"},
            {"name": "index", "value": [1, 2], "type": "list"},
        ],
    )
    assert (
        objective.stringify(indent=12)
        == """objective=ObjectiveFcn.Lagrange.MINIMIZE_STATE,
            weight=-10.0,
            key="q",
            index=[1, 2],
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
