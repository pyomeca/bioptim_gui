import numpy as np
import pytest

from bioptim_gui_api.variables.misc.variables_utils import init_guess_after_interpolation_type_change


@pytest.fixture
def default_const_variable():
    return {
        "name": "test",
        "dimension": 5,
        "bounds_interpolation_type": "CONSTANT",
        "bounds": {
            "min_bounds": [
                [-1.0],
                [-2.0],
                [-3.0],
                [-4.0],
                [-5.0],
            ],
            "max_bounds": [
                [0.0],
                [1.0],
                [2.0],
                [3.0],
                [5.0],
            ],
        },
        "initial_guess_interpolation_type": "CONSTANT",
        "initial_guess": [
            [-1.0],
            [-2.0],
            [-3.0],
            [-4.0],
            [-5.0],
        ],
    }


@pytest.fixture
def default_linear_variable():
    return {
        "name": "test",
        "dimension": 5,
        "bounds_interpolation_type": "LINEAR",
        "bounds": {
            "min_bounds": [
                [-1.0, 1.0],
                [-2.0, 2.0],
                [-3.0, 3.0],
                [-4.0, 4.0],
                [-5.0, 5.0],
            ],
            "max_bounds": [
                [0.0, 2.0],
                [1.0, 3.0],
                [2.0, 4.0],
                [3.0, 5.0],
                [5.0, 5.0],
            ],
        },
        "initial_guess_interpolation_type": "LINEAR",
        "initial_guess": [
            [-1.0, 1.0],
            [-2.0, 2.0],
            [-3.0, 3.0],
            [-4.0, 4.0],
            [-5.0, 10.0],
        ],
    }


@pytest.fixture
def default_cwfld_variable():
    return {
        "name": "test",
        "dimension": 5,
        "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
        "bounds": {
            "min_bounds": [
                [-1.0, -1.5, 1.0],
                [-2.0, -3.0, 2.0],
                [-3.0, -4.0, 3.0],
                [-4.0, -5.0, 4.0],
                [-5.0, -6.0, 5.0],
            ],
            "max_bounds": [
                [0.0, 2.0, 2.0],
                [1.0, 3.0, 3.0],
                [2.0, 4.0, 4.0],
                [3.0, 5.0, 5.0],
                [5.0, 5.0, 10.0],
            ],
        },
        "initial_guess_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
        "initial_guess": [
            [-1.0, 1.0, 1.0],
            [-2.0, 2.0, 2.0],
            [-3.0, 3.0, 3.0],
            [-4.0, 4.0, 4.0],
            [-5.0, 10.0, 10.0],
        ],
    }


def test_constant_to_constant(default_const_variable):
    init_guess_after_interpolation_type_change(default_const_variable, "CONSTANT")
    assert np.allclose(
        default_const_variable["bounds"]["min_bounds"],
        [
            [-1.0],
            [-2.0],
            [-3.0],
            [-4.0],
            [-5.0],
        ],
    )
    assert np.allclose(
        default_const_variable["bounds"]["max_bounds"],
        [
            [0.0],
            [1.0],
            [2.0],
            [3.0],
            [5.0],
        ],
    )
    assert np.allclose(
        default_const_variable["initial_guess"],
        [
            [-1.0],
            [-2.0],
            [-3.0],
            [-4.0],
            [-5.0],
        ],
    )


def test_constant_to_linear(default_const_variable):
    init_guess_after_interpolation_type_change(default_const_variable, "LINEAR")
    assert np.allclose(
        default_const_variable["bounds"]["min_bounds"],
        [
            [-1.0],
            [-2.0],
            [-3.0],
            [-4.0],
            [-5.0],
        ],
    )
    assert np.allclose(
        default_const_variable["bounds"]["max_bounds"],
        [
            [0.0],
            [1.0],
            [2.0],
            [3.0],
            [5.0],
        ],
    )
    assert np.allclose(
        default_const_variable["initial_guess"],
        [
            [-1.0, -1.0],
            [-2.0, -2.0],
            [-3.0, -3.0],
            [-4.0, -4.0],
            [-5.0, -5.0],
        ],
    )


def test_constant_to_constant_with_first_and_last_different(default_const_variable):
    init_guess_after_interpolation_type_change(default_const_variable, "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT")
    assert np.allclose(
        default_const_variable["bounds"]["min_bounds"],
        [
            [-1.0],
            [-2.0],
            [-3.0],
            [-4.0],
            [-5.0],
        ],
    )
    assert np.allclose(
        default_const_variable["bounds"]["max_bounds"],
        [
            [0.0],
            [1.0],
            [2.0],
            [3.0],
            [5.0],
        ],
    )
    assert np.allclose(
        default_const_variable["initial_guess"],
        [
            [-1.0, -1.0, -1.0],
            [-2.0, -2.0, -2.0],
            [-3.0, -3.0, -3.0],
            [-4.0, -4.0, -4.0],
            [-5.0, -5.0, -5.0],
        ],
    )


def test_linear_to_constant(default_linear_variable):
    init_guess_after_interpolation_type_change(default_linear_variable, "CONSTANT")
    assert np.allclose(
        default_linear_variable["bounds"]["min_bounds"],
        [
            [-1.0, 1.0],
            [-2.0, 2.0],
            [-3.0, 3.0],
            [-4.0, 4.0],
            [-5.0, 5.0],
        ],
    )
    assert np.allclose(
        default_linear_variable["bounds"]["max_bounds"],
        [
            [0.0, 2.0],
            [1.0, 3.0],
            [2.0, 4.0],
            [3.0, 5.0],
            [5.0, 5.0],
        ],
    )
    assert np.allclose(
        default_linear_variable["initial_guess"],
        [
            [0.0],
            [0.0],
            [0.0],
            [0.0],
            [2.5],
        ],
    )


def test_linear_to_linear(default_linear_variable):
    init_guess_after_interpolation_type_change(default_linear_variable, "LINEAR")
    assert np.allclose(
        default_linear_variable["bounds"]["min_bounds"],
        [
            [-1.0, 1.0],
            [-2.0, 2.0],
            [-3.0, 3.0],
            [-4.0, 4.0],
            [-5.0, 5.0],
        ],
    )
    assert np.allclose(
        default_linear_variable["bounds"]["max_bounds"],
        [
            [0.0, 2.0],
            [1.0, 3.0],
            [2.0, 4.0],
            [3.0, 5.0],
            [5.0, 5.0],
        ],
    )
    assert np.allclose(
        default_linear_variable["initial_guess"],
        [
            [-1.0, 1.0],
            [-2.0, 2.0],
            [-3.0, 3.0],
            [-4.0, 4.0],
            [-5.0, 10.0],
        ],
    )


def test_linear_to_constant_with_first_and_last_different(default_linear_variable):
    init_guess_after_interpolation_type_change(default_linear_variable, "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT")
    assert np.allclose(
        default_linear_variable["bounds"]["min_bounds"],
        [
            [-1.0, 1.0],
            [-2.0, 2.0],
            [-3.0, 3.0],
            [-4.0, 4.0],
            [-5.0, 5.0],
        ],
    )
    assert np.allclose(
        default_linear_variable["bounds"]["max_bounds"],
        [
            [0.0, 2.0],
            [1.0, 3.0],
            [2.0, 4.0],
            [3.0, 5.0],
            [5.0, 5.0],
        ],
    )
    assert np.allclose(
        default_linear_variable["initial_guess"],
        [
            [-1.0, 0.0, 1.0],
            [-2.0, 0.0, 2.0],
            [-3.0, 0.0, 3.0],
            [-4.0, 0.0, 4.0],
            [-5.0, 2.5, 10.0],
        ],
    )


def test_constant_with_first_and_last_different_to_constant(default_cwfld_variable):
    init_guess_after_interpolation_type_change(default_cwfld_variable, "CONSTANT")
    assert np.allclose(
        default_cwfld_variable["bounds"]["min_bounds"],
        [
            [-1.0, -1.5, 1.0],
            [-2.0, -3.0, 2.0],
            [-3.0, -4.0, 3.0],
            [-4.0, -5.0, 4.0],
            [-5.0, -6.0, 5.0],
        ],
    )
    assert np.allclose(
        default_cwfld_variable["bounds"]["max_bounds"],
        [
            [0.0, 2.0, 2.0],
            [1.0, 3.0, 3.0],
            [2.0, 4.0, 4.0],
            [3.0, 5.0, 5.0],
            [5.0, 5.0, 10.0],
        ],
    )
    assert np.allclose(
        default_cwfld_variable["initial_guess"],
        [
            [0.0],
            [0.0],
            [0.0],
            [0.0],
            [2.5],
        ],
    )


def test_constant_with_first_and_last_different_to_linear(default_cwfld_variable):
    init_guess_after_interpolation_type_change(default_cwfld_variable, "LINEAR")
    assert np.allclose(
        default_cwfld_variable["bounds"]["min_bounds"],
        [
            [-1.0, -1.5, 1.0],
            [-2.0, -3.0, 2.0],
            [-3.0, -4.0, 3.0],
            [-4.0, -5.0, 4.0],
            [-5.0, -6.0, 5.0],
        ],
    )
    assert np.allclose(
        default_cwfld_variable["bounds"]["max_bounds"],
        [
            [0.0, 2.0, 2.0],
            [1.0, 3.0, 3.0],
            [2.0, 4.0, 4.0],
            [3.0, 5.0, 5.0],
            [5.0, 5.0, 10.0],
        ],
    )
    assert np.allclose(
        default_cwfld_variable["initial_guess"],
        [
            [-1.0, 1.0],
            [-2.0, 2.0],
            [-3.0, 3.0],
            [-4.0, 4.0],
            [-5.0, 10.0],
        ],
    )


def test_constant_with_first_and_last_different_to_constant_with_first_and_last_different(default_cwfld_variable):
    init_guess_after_interpolation_type_change(default_cwfld_variable, "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT")
    assert np.allclose(
        default_cwfld_variable["bounds"]["min_bounds"],
        [
            [-1.0, -1.5, 1.0],
            [-2.0, -3.0, 2.0],
            [-3.0, -4.0, 3.0],
            [-4.0, -5.0, 4.0],
            [-5.0, -6.0, 5.0],
        ],
    )
    assert np.allclose(
        default_cwfld_variable["bounds"]["max_bounds"],
        [
            [0.0, 2.0, 2.0],
            [1.0, 3.0, 3.0],
            [2.0, 4.0, 4.0],
            [3.0, 5.0, 5.0],
            [5.0, 5.0, 10.0],
        ],
    )
    assert np.allclose(
        default_cwfld_variable["initial_guess"],
        [
            [-1.0, 1.0, 1.0],
            [-2.0, 2.0, 2.0],
            [-3.0, 3.0, 3.0],
            [-4.0, 4.0, 4.0],
            [-5.0, 10.0, 10.0],
        ],
    )
