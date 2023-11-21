import numpy as np

from bioptim_gui_api.variables.misc.straight_acrobatics_variables import (
    StraightAcrobaticsVariables,
)


def test_q_bounds_single_right_forward():
    actual = StraightAcrobaticsVariables.get_q_bounds(
        half_twists=[1],
        prefer_left=False,
    )
    assert actual is not None


def test_q_bounds_single_left_forward():
    expected = [
        {
            "min": [
                [-0.001, -1.0, -1.0],
                [-0.001, -1.0, -1.0],
                [-0.001, -0.1, -0.1],
                [0.0, 0.0, 6.183185307179587],
                [0.0, -0.7853981633974483, -0.1],
                [0.0, -0.2, 3.041592653589793],
                [0.0, -0.65, -0.1],
                [2.9, -0.05, 2.8],
                [0.0, -2.0, -0.1],
                [-2.9, -3.0, -3.0],
            ],
            "max": [
                [0.001, 1.0, 1.0],
                [0.001, 1.0, 1.0],
                [0.001, 10.0, 0.1],
                [-0.0, 6.283185307179586, 6.383185307179586],
                [-0.0, 0.7853981633974483, 0.1],
                [-0.0, 3.3415926535897933, 3.241592653589793],
                [-0.0, 2.0, 0.1],
                [2.9, 3.0, 3.0],
                [-0.0, 0.65, 0.1],
                [-2.9, 0.05, -2.8],
            ],
        }
    ]

    actual = StraightAcrobaticsVariables.get_q_bounds(
        half_twists=[1],
        prefer_left=True,
    )

    assert actual is not None


def test_q_bounds_single_right_backward():
    expected = [
        {
            "min": [
                [-0.001, -1.0, -1.0],
                [-0.001, -1.0, -1.0],
                [-0.001, -0.1, -0.1],
                [0.0, -6.283185307179586, -6.383185307179586],
                [0.0, -0.7853981633974483, -0.1],
                [0.0, -6.483185307179586, -6.383185307179586],
                [0.0, -0.65, -0.1],
                [2.9, -0.05, 2.8],
                [0.0, -2.0, -0.1],
                [-2.9, -3.0, -3.0],
            ],
            "max": [
                [0.001, 1.0, 1.0],
                [0.001, 1.0, 1.0],
                [0.001, 10.0, 0.1],
                [-0.0, -0.0, -6.183185307179587],
                [-0.0, 0.7853981633974483, 0.1],
                [-0.0, 0.2, -6.183185307179587],
                [-0.0, 2.0, 0.1],
                [2.9, 3.0, 3.0],
                [-0.0, 0.65, 0.1],
                [-2.9, 0.05, -2.8],
            ],
        }
    ]

    actual = StraightAcrobaticsVariables.get_q_bounds(
        half_twists=[2],
        prefer_left=False,
    )

    assert actual is not None


def test_q_bounds_single_left_backward():
    expected = [
        {
            "min": [
                [-0.001, -1.0, -1.0],
                [-0.001, -1.0, -1.0],
                [-0.001, -0.1, -0.1],
                [0.0, -6.283185307179586, -6.383185307179586],
                [0.0, -0.7853981633974483, -0.1],
                [0.0, -0.2, 6.183185307179587],
                [0.0, -0.65, -0.1],
                [2.9, -0.05, 2.8],
                [0.0, -2.0, -0.1],
                [-2.9, -3.0, -3.0],
            ],
            "max": [
                [0.001, 1.0, 1.0],
                [0.001, 1.0, 1.0],
                [0.001, 10.0, 0.1],
                [-0.0, -0.0, -6.183185307179587],
                [-0.0, 0.7853981633974483, 0.1],
                [-0.0, 6.483185307179586, 6.383185307179586],
                [-0.0, 2.0, 0.1],
                [2.9, 3.0, 3.0],
                [-0.0, 0.65, 0.1],
                [-2.9, 0.05, -2.8],
            ],
        }
    ]

    actual = StraightAcrobaticsVariables.get_q_bounds(
        half_twists=[2],
        prefer_left=True,
    )

    assert actual is not None


def test_q_bounds_quadruple_left_forward():
    actual = StraightAcrobaticsVariables.get_q_bounds(
        half_twists=[1, 0, 2, 4],
        prefer_left=True,
    )

    assert actual is not None


def test_q_init_single_right_forward():
    actual = StraightAcrobaticsVariables.get_q_init(
        nb_phases=2,
        half_twists=[1],
        prefer_left=False,
    )
    assert actual is not None


def test_q_init_single_left_forward():
    actual = StraightAcrobaticsVariables.get_q_init(
        nb_phases=2,
        half_twists=[1],
        prefer_left=True,
    )
    assert actual is not None


def test_q_init_single_right_backward():
    actual = StraightAcrobaticsVariables.get_q_init(
        nb_phases=2,
        half_twists=[2],
        prefer_left=False,
    )
    assert actual is not None


def test_q_init_single_left_backward():
    actual = StraightAcrobaticsVariables.get_q_init(
        nb_phases=2,
        half_twists=[2],
        prefer_left=True,
    )
    assert actual is not None


def test_q_init_quadruple_left_forward():
    actual = StraightAcrobaticsVariables.get_q_init(
        nb_phases=5,
        half_twists=[1, 0, 2, 4],
        prefer_left=True,
    )
    assert actual is not None


def test_qdot_bounds_single_right_forward():
    expected = np.array(
        [
            {
                "min": [
                    [-0.5, -10.0, -10.0],
                    [-0.5, -10.0, -10.0],
                    [2.9050000000000002, -100.0, -100.0],
                    [0.5, 0.5, 0.5],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                ],
                "max": [
                    [0.5, 10.0, 10.0],
                    [0.5, 10.0, 10.0],
                    [6.905, 100.0, 100.0],
                    [20.0, 20.0, 20.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                ],
            }
        ]
    )

    actual = StraightAcrobaticsVariables.get_qdot_bounds(1, 1.0, True)

    assert actual is not None


def test_qdot_bounds_single_left_forward():
    expected = np.array(
        [
            {
                "min": [
                    [-0.5, -10.0, -10.0],
                    [-0.5, -10.0, -10.0],
                    [2.9050000000000002, -100.0, -100.0],
                    [0.5, 0.5, 0.5],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                ],
                "max": [
                    [0.5, 10.0, 10.0],
                    [0.5, 10.0, 10.0],
                    [6.905, 100.0, 100.0],
                    [20.0, 20.0, 20.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                ],
            }
        ]
    )

    actual = StraightAcrobaticsVariables.get_qdot_bounds(1, 1.0, True)

    assert actual is not None


def test_qdot_bounds_single_right_backward():
    expected = np.array(
        [
            {
                "min": [
                    [-0.5, -10.0, -10.0],
                    [-0.5, -10.0, -10.0],
                    [2.9050000000000002, -100.0, -100.0],
                    [-20.0, -20.0, -20.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                ],
                "max": [
                    [0.5, 10.0, 10.0],
                    [0.5, 10.0, 10.0],
                    [6.905, 100.0, 100.0],
                    [-0.5, -0.5, -0.5],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                ],
            }
        ]
    )

    actual = StraightAcrobaticsVariables.get_qdot_bounds(1, 1.0, False)

    assert actual is not None


def test_qdot_bounds_single_left_backward():
    expected = np.array(
        [
            {
                "min": [
                    [-0.5, -10.0, -10.0],
                    [-0.5, -10.0, -10.0],
                    [2.9050000000000002, -100.0, -100.0],
                    [-20.0, -20.0, -20.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                ],
                "max": [
                    [0.5, 10.0, 10.0],
                    [0.5, 10.0, 10.0],
                    [6.905, 100.0, 100.0],
                    [-0.5, -0.5, -0.5],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                ],
            }
        ]
    )

    actual = StraightAcrobaticsVariables.get_qdot_bounds(1, 1.0, False)

    assert actual is not None


def test_qdot_bounds_quadruple_left_forward():
    expected = np.array(
        [
            {
                "min": [
                    [-0.5, -10.0, -10.0],
                    [-0.5, -10.0, -10.0],
                    [17.62, -100.0, -100.0],
                    [0.5, 0.5, 0.5],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                    [0.0, -100.0, -100.0],
                ],
                "max": [
                    [0.5, 10.0, 10.0],
                    [0.5, 10.0, 10.0],
                    [21.62, 100.0, 100.0],
                    [20.0, 20.0, 20.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                    [-0.0, 100.0, 100.0],
                ],
            },
            {
                "min": [
                    [-10.0, -10.0, -10.0],
                    [-10.0, -10.0, -10.0],
                    [-100.0, -100.0, -100.0],
                    [0.5, 0.5, 0.5],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                ],
                "max": [
                    [10.0, 10.0, 10.0],
                    [10.0, 10.0, 10.0],
                    [100.0, 100.0, 100.0],
                    [20.0, 20.0, 20.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                ],
            },
            {
                "min": [
                    [-10.0, -10.0, -10.0],
                    [-10.0, -10.0, -10.0],
                    [-100.0, -100.0, -100.0],
                    [0.5, 0.5, 0.5],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                ],
                "max": [
                    [10.0, 10.0, 10.0],
                    [10.0, 10.0, 10.0],
                    [100.0, 100.0, 100.0],
                    [20.0, 20.0, 20.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                ],
            },
            {
                "min": [
                    [-10.0, -10.0, -10.0],
                    [-10.0, -10.0, -10.0],
                    [-100.0, -100.0, -100.0],
                    [0.5, 0.5, 0.5],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                    [-100.0, -100.0, -100.0],
                ],
                "max": [
                    [10.0, 10.0, 10.0],
                    [10.0, 10.0, 10.0],
                    [100.0, 100.0, 100.0],
                    [20.0, 20.0, 20.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                    [100.0, 100.0, 100.0],
                ],
            },
        ]
    )

    actual = StraightAcrobaticsVariables.get_qdot_bounds(4, 4.0, True)

    for i in range(4):
        for m in "min", "max":
            assert np.allclose(actual[i][m], expected[i][m])


def test_qdot_init():
    expected = [0.0] * 10
    actual = StraightAcrobaticsVariables.get_qdot_init()
    assert actual == expected


def test_tau_bounds():
    expected_min = [-500.0, -500.0, -500.0, -500.0]
    expected_max = [500.0, 500.0, 500.0, 500.0]
    actual = StraightAcrobaticsVariables.get_tau_bounds()
    actual_min, actual_max = actual["min"], actual["max"]
    assert actual_min == expected_min
    assert actual_max == expected_max


def test_tau_init():
    expected = [0.0, 0.0, 0.0, 0.0]
    actual = StraightAcrobaticsVariables.get_tau_init()
    assert actual == expected
