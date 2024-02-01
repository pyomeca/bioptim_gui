import numpy as np
import pytest

from bioptim_gui_api.variables.misc.variables_utils import (
    variables_zeros,
    define_loose_bounds,
    LooseValue,
)


@pytest.mark.parametrize(
    "dimension, interpolation_type, expected",
    [
        (0, "LINEAR", []),
        (0, "CONSTANT", []),
        (0, "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT", []),
        (1, "LINEAR", [[0.0, 0.0]]),
        (1, "CONSTANT", [[0.0]]),
        (1, "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT", [[0.0, 0.0, 0.0]]),
        (2, "LINEAR", [[0.0, 0.0], [0.0, 0.0]]),
        (2, "CONSTANT", [[0.0], [0.0]]),
        (
            2,
            "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
            [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        ),
        (5, "LINEAR", [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]),
        (5, "CONSTANT", [[0.0], [0.0], [0.0], [0.0], [0.0]]),
        (
            5,
            "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
        ),
    ],
)
def test_variables_zeros(dimension, interpolation_type, expected):
    assert variables_zeros(dimension, interpolation_type) == expected


def test_variables_zeros_error():
    with pytest.raises(ValueError):
        variables_zeros(1, "NOT_IMPLEMENTED")


def test_define_loose():
    bound = [
        {
            "min": np.zeros((10, 3)),
            "max": np.zeros((10, 3)),
        }
    ]
    define_loose_bounds(bound[0], 5, 2, LooseValue(0.9, 0.1))
    assert bound[0]["min"][5, 2] == 0.8
    assert bound[0]["max"][5, 2] == 1.0
