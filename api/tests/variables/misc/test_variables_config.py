from bioptim_gui_api.variables.misc.variables_config import default_bounds_initial_guess


def test_default_bounds_initial_guess_default():
    default = default_bounds_initial_guess("test")

    expected = {
        "name": "test",
        "dimension": 1,
        "bounds_interpolation_type": "CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT",
        "bounds": {
            "min_bounds": [[0.0, 0.0, 0.0]],
            "max_bounds": [[0.0, 0.0, 0.0]],
        },
        "initial_guess_interpolation_type": "CONSTANT",
        "initial_guess": [[0.0]],
    }

    assert default["name"] == expected["name"]
    assert default["dimension"] == expected["dimension"]
    assert default["bounds_interpolation_type"] == expected["bounds_interpolation_type"]
    assert default["bounds"]["min_bounds"] == expected["bounds"]["min_bounds"]
    assert default["bounds"]["max_bounds"] == expected["bounds"]["max_bounds"]
    assert default["initial_guess_interpolation_type"] == expected["initial_guess_interpolation_type"]
    assert default["initial_guess"] == expected["initial_guess"]

    # check that the min and max bounds are not the same address
    default["bounds"]["min_bounds"][0][0] = 1.0
    assert default["bounds"]["min_bounds"][0][0] == 1.0
    assert default["bounds"]["max_bounds"][0][0] == 0.0
