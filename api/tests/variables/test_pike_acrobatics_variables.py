import numpy as np
import pytest

from bioptim_gui_api.variables.pike_acrobatics_variables import (
    PikeAcrobaticsVariables,
)


# P pike
# S somersault
# K kick out
# T twist
# L landing
@pytest.mark.parametrize(
    ("half_twists", "expected_number_of_phase", "phases_str"),
    [
        ([0, 0], 4, "PSKL"),
        ([1, 0], 5, "TPSKL"),
        ([0, 1], 5, "PSKTL"),
        ([1, 1], 6, "TPSKTL"),
        ([0, 0, 0], 4, "PSKL"),
        ([0, 0, 1], 5, "PSKTL"),
        ([0, 1, 0], 8, "PSKTPSKL"),
        ([0, 1, 1], 9, "PSKTPSKTL"),
        ([1, 0, 0], 5, "TPSKL"),
        ([1, 0, 1], 6, "TPSKTL"),
        ([1, 1, 0], 9, "TPSKTPSKL"),
        ([0, 0, 0, 0], 4, "PSKL"),
        ([0, 0, 0, 1], 5, "PSKTL"),
        ([0, 0, 1, 0], 8, "PSKTPSKL"),
        ([0, 0, 1, 1], 9, "PSKTPSKTL"),
        ([0, 1, 0, 0], 8, "PSKTPSKL"),
        ([0, 1, 0, 1], 9, "PSKTPSKTL"),
        ([0, 1, 1, 0], 12, "PSKTPSKTPSKL"),
        ([0, 1, 1, 1], 13, "PSKTPSKTPSKTL"),
        ([1, 0, 0, 0], 5, "TPSKL"),
        ([1, 0, 0, 1], 6, "TPSKTL"),
        ([1, 0, 1, 0], 9, "TPSKTPSKL"),
        ([1, 0, 1, 1], 10, "TPSKTPSKTL"),
        ([1, 1, 0, 0], 9, "TPSKTPSKL"),
        ([1, 1, 0, 1], 10, "TPSKTPSKTL"),
        ([1, 1, 1, 0], 13, "TPSKTPSKTPSKL"),
        ([1, 1, 1, 1], 14, "TPSKTPSKTPSKTL"),
    ],
)
def test_q_bounds_number(half_twists, expected_number_of_phase, phases_str):
    phases = PikeAcrobaticsVariables.get_q_bounds(
        half_twists=half_twists,
        prefer_left=False,
    )
    assert len(phases) == expected_number_of_phase
    # assert expected_number_of_phase == len(phases_str) # to check if the test is correctly written
    # assert "".join(phases) == phases_str


def test_q_bounds_quadruple_left_forward():
    expected = [
        {
            "min": [
                [-0.001, -1.0, -1.0],
                [-0.001, -1.0, -1.0],
                [-0.001, -0.1, -0.1],
                [0.0, 0.0, 6.283185307179586],
                [0.0, -0.7853981633974483, -0.7853981633974483],
                [0.0, -0.2, 2.941592653589793],
                [0.0, -0.65, -0.65],
                [2.9, -0.05, -0.05],
                [0.0, -1.8, -1.8],
                [0.0, -2.65, -2.65],
                [0.0, -2.0, -2.0],
                [-2.9, -3.0, -3.0],
                [0.0, -1.1, -1.1],
                [0.0, -2.65, -2.65],
                [0.0, -2.7, -2.7],
                [0.0, -0.1, -0.1],
            ],
            "max": [
                [0.001, 1.0, 1.0],
                [0.001, 1.0, 1.0],
                [0.001, 10.0, 10.0],
                [-0.0, 6.283185307179586, 6.283185307179586],
                [-0.0, 0.7853981633974483, 0.7853981633974483],
                [-0.0, 3.3415926535897933, 3.3415926535897933],
                [-0.0, 2.0, 2.0],
                [2.9, 3.0, 3.0],
                [-0.0, 1.1, 1.1],
                [-0.0, 0.0, 0.0],
                [-0.0, 0.65, 0.65],
                [-2.9, 0.05, 0.05],
                [-0.0, 1.8, 1.8],
                [-0.0, 0.0, 0.0],
                [-0.0, 0.3, 0.3],
                [-0.0, 0.1, 0.1],
            ],
        },
        {
            "min": [
                [-1.0, -1.0, -1.0],
                [-1.0, -1.0, -1.0],
                [-0.1, -0.1, -0.1],
                [6.283185307179586, 6.283185307179586, 12.566370614359172],
                [-0.7853981633974483, -0.7853981633974483, -0.7853981633974483],
                [2.941592653589793, 2.941592653589793, 2.941592653589793],
                [-0.65, -0.65, -0.65],
                [-0.05, -0.05, -0.05],
                [-1.8, -1.8, -1.8],
                [-2.65, -2.65, -2.65],
                [-2.0, -2.0, -2.0],
                [-3.0, -3.0, -3.0],
                [-1.1, -1.1, -1.1],
                [-2.65, -2.65, -2.65],
                [-2.7, -2.7, -2.7],
                [-0.1, -0.1, -0.1],
            ],
            "max": [
                [1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0],
                [10.0, 10.0, 10.0],
                [6.283185307179586, 12.566370614359172, 12.566370614359172],
                [0.7853981633974483, 0.7853981633974483, 0.7853981633974483],
                [3.3415926535897933, 3.3415926535897933, 3.3415926535897933],
                [2.0, 2.0, 2.0],
                [3.0, 3.0, 3.0],
                [1.1, 1.1, 1.1],
                [0.0, 0.0, 0.0],
                [0.65, 0.65, 0.65],
                [0.05, 0.05, 0.05],
                [1.8, 1.8, 1.8],
                [0.0, 0.0, 0.0],
                [0.3, 0.3, 0.3],
                [0.1, 0.1, 0.1],
            ],
        },
        {
            "min": [
                [-1.0, -1.0, -1.0],
                [-1.0, -1.0, -1.0],
                [-0.1, -0.1, -0.1],
                [12.566370614359172, 12.566370614359172, 18.84955592153876],
                [-0.7853981633974483, -0.7853981633974483, -0.7853981633974483],
                [2.941592653589793, 2.941592653589793, 9.22477796076938],
                [-0.65, -0.65, -0.65],
                [-0.05, -0.05, -0.05],
                [-1.8, -1.8, -1.8],
                [-2.65, -2.65, -2.65],
                [-2.0, -2.0, -2.0],
                [-3.0, -3.0, -3.0],
                [-1.1, -1.1, -1.1],
                [-2.65, -2.65, -2.65],
                [-2.7, -2.7, -2.7],
                [-0.1, -0.1, -0.1],
            ],
            "max": [
                [1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0],
                [10.0, 10.0, 10.0],
                [12.566370614359172, 18.84955592153876, 18.84955592153876],
                [0.7853981633974483, 0.7853981633974483, 0.7853981633974483],
                [3.3415926535897933, 9.624777960769379, 9.624777960769379],
                [2.0, 2.0, 2.0],
                [3.0, 3.0, 3.0],
                [1.1, 1.1, 1.1],
                [0.0, 0.0, 0.0],
                [0.65, 0.65, 0.65],
                [0.05, 0.05, 0.05],
                [1.8, 1.8, 1.8],
                [0.0, 0.0, 0.0],
                [0.3, 0.3, 0.3],
                [0.1, 0.1, 0.1],
            ],
        },
        {
            "min": [
                [-1.0, -1.0, -1.0],
                [-1.0, -1.0, -1.0],
                [-0.1, -0.1, -0.1],
                [18.84955592153876, 18.84955592153876, 25.032741228718344],
                [-0.7853981633974483, -0.7853981633974483, -0.1],
                [9.22477796076938, 9.22477796076938, 21.89114857512855],
                [-0.65, -0.65, -0.1],
                [-0.05, -0.05, 2.8],
                [-1.8, -1.8, -0.1],
                [-2.65, -2.65, -0.1],
                [-2.0, -2.0, -0.1],
                [-3.0, -3.0, -3.0],
                [-1.1, -1.1, -0.1],
                [-2.65, -2.65, -0.1],
                [-2.7, -2.7, -0.1],
                [-0.1, -0.1, -0.1],
            ],
            "max": [
                [1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0],
                [10.0, 10.0, 0.1],
                [18.84955592153876, 25.132741228718345, 25.232741228718346],
                [0.7853981633974483, 0.7853981633974483, 0.1],
                [9.624777960769379, 22.19114857512855, 22.091148575128553],
                [2.0, 2.0, 0.1],
                [3.0, 3.0, 3.0],
                [1.1, 1.1, 0.1],
                [0.0, 0.0, 0.1],
                [0.65, 0.65, 0.1],
                [0.05, 0.05, -2.8],
                [1.8, 1.8, 0.1],
                [0.0, 0.0, 0.1],
                [0.3, 0.3, 0.1],
                [0.1, 0.1, 0.1],
            ],
        },
    ]

    actual = PikeAcrobaticsVariables.get_q_bounds(
        half_twists=[1, 0, 2, 4],
        prefer_left=True,
    )

    for i in range(4):
        for m in "min", "max":
            assert np.allclose(actual[i][m], expected[i][m])


def test_q_init_quadruple_left_forward():
    expected = [
        [
            [
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                2.9,
                0.0,
                0.0,
                0.0,
                -2.9,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
            [
                0.0,
                0.0,
                0.0,
                6.28318531,
                0.0,
                3.14159265,
                0.0,
                2.9,
                0.0,
                0.0,
                0.0,
                -2.9,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
        ],
        [
            [
                0.0,
                0.0,
                0.0,
                6.28318531,
                0.0,
                3.14159265,
                0.0,
                2.9,
                0.0,
                0.0,
                0.0,
                -2.9,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
            [
                0.0,
                0.0,
                0.0,
                12.56637061,
                0.0,
                3.14159265,
                0.0,
                2.9,
                0.0,
                0.0,
                0.0,
                -2.9,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
        ],
        [
            [
                0.0,
                0.0,
                0.0,
                12.56637061,
                0.0,
                3.14159265,
                0.0,
                2.9,
                0.0,
                0.0,
                0.0,
                -2.9,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
            [
                0.0,
                0.0,
                0.0,
                18.84955592,
                0.0,
                9.42477796,
                0.0,
                2.9,
                0.0,
                0.0,
                0.0,
                -2.9,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
        ],
        [
            [
                0.0,
                0.0,
                0.0,
                18.84955592,
                0.0,
                9.42477796,
                0.0,
                2.9,
                0.0,
                0.0,
                0.0,
                -2.9,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
            [
                0.0,
                0.0,
                0.0,
                25.13274123,
                0.0,
                21.99114858,
                0.0,
                2.9,
                0.0,
                0.0,
                0.0,
                -2.9,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
        ],
    ]

    actual = PikeAcrobaticsVariables.get_q_init(
        half_twists=[1, 0, 2, 4],
        prefer_left=True,
    )
    assert np.allclose(actual, expected)


def test_qdot_bounds_quadruple_left_forward():
    expected = [
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
                [100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0],
            ],
        },
    ]

    actual = PikeAcrobaticsVariables.get_qdot_bounds(4, 4.0, True)

    for i in range(4):
        for m in "min", "max":
            assert np.allclose(actual[i][m], expected[i][m])


def test_qdot_init():
    expected = [0.0] * 16
    actual = PikeAcrobaticsVariables.get_qdot_init()
    assert actual == expected


def test_tau_bounds():
    expected_min = [-500.0] * 10
    expected_max = [500.0] * 10
    actual = PikeAcrobaticsVariables.get_tau_bounds()
    actual_min, actual_max = actual["min"], actual["max"]
    assert actual_min == expected_min
    assert actual_max == expected_max


def test_tau_init():
    expected = [0.0] * 10
    actual = PikeAcrobaticsVariables.get_tau_init()
    assert actual == expected
