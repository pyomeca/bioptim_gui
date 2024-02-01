import numpy as np
import pytest

from bioptim_gui_api.acrobatics_ocp.variables.utils import maximum_fig_arms_angle


@pytest.mark.parametrize(
    "half_twists",
    [
        [0],
        [1],
        [2],
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
        [2, 0],
        [2, 1],
        [3, 0],
        [3, 1],
        [4, 0],
        [4, 1],
    ],
)
def test_fig_max_arms_angle_45(half_twists):
    assert maximum_fig_arms_angle(half_twists) == np.deg2rad(45)


@pytest.mark.parametrize(
    "half_twists",
    [
        [3],
        [4],
        [0, 2],
        [0, 3],
        [1, 2],
        [1, 3],
        [2, 2],
        [2, 3],
        [3, 2],
        [3, 3],
        [4, 2],
        [4, 13],
    ],
)
def test_fig_max_arms_angle_90(half_twists):
    assert maximum_fig_arms_angle(half_twists) == np.deg2rad(90)
