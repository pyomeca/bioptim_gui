import pytest

from bioptim_gui_api.variables.variables_utils import variables_zeros


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
