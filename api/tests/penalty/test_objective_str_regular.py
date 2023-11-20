from bioptim_gui_api.penalty.objective import Objective


def test_regular_str_simple():
    objective = Objective(
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
        str(objective)
        == """objective=ObjectiveFcn.Lagrange.MINIMIZE_STATE,
        key="q",
        index=[1, 2],
        node=Node.ALL,
        quadratic=False,
        weight=1.0,
"""
    )


def test_mayer_no_integration_rule():
    objective = Objective(
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
        str(objective)
        == """objective=ObjectiveFcn.Mayer.MINIMIZE_STATE,
        key="q",
        index=[1, 2],
        node=Node.ALL,
        quadratic=False,
        weight=1.0,
"""
    )


def test_regular_str_simple_phase():
    objective = Objective(
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
        objective.__str__(nb_phase=36)
        == """objective=ObjectiveFcn.Mayer.MINIMIZE_STATE,
        key="q",
        index=[1, 2],
        node=Node.ALL,
        quadratic=False,
        weight=1.0,
        phase=30,
"""
    )


def test_regular_str_indent_8():
    objective = Objective(
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
        objective.__str__(indent=12, nb_phase=1)
        == """objective=ObjectiveFcn.Lagrange.MINIMIZE_STATE,
            key="q",
            index=[1, 2],
            node=Node.ALL,
            quadratic=False,
            weight=1.0,
"""
    )


def test_regular_str_indent_8_with_phase():
    objective = Objective(
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
        objective.__str__(indent=12, nb_phase=36)
        == """objective=ObjectiveFcn.Lagrange.MINIMIZE_STATE,
            key="q",
            index=[1, 2],
            node=Node.ALL,
            quadratic=False,
            weight=1.0,
            phase=30,
"""
    )


def test_regular_str_indent_8_with_phase_all():
    objective = Objective(
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
        objective.__str__(indent=12, nb_phase=36)
        == """objective=ObjectiveFcn.Lagrange.MINIMIZE_STATE,
            key="q",
            index=[1, 2],
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
