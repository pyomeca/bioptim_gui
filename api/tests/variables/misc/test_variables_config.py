import pytest

from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.variables.misc.straight_with_visual_acrobatics_variables_with_spine import (
    StraightAcrobaticsWithVisualVariablesWithSpine,
)
from bioptim_gui_api.variables.misc.variables_config import default_bounds_initial_guess, get_variable_computer


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


@pytest.mark.parametrize("position", ["straight", "pike", "tuck"])
@pytest.mark.parametrize("with_visual_criteria", [True, False])
@pytest.mark.parametrize("collision_constraint", [True, False])
@pytest.mark.parametrize("with_spine", [True, False])
def test_get_variable_computer(position, with_visual_criteria, collision_constraint, with_spine):
    additional_criteria = AdditionalCriteria(
        with_visual_criteria=with_visual_criteria, collision_constraint=collision_constraint, with_spine=with_spine
    )
    assert get_variable_computer(position, additional_criteria)


def test_get_variable_computer_simple():
    additional_criteria = AdditionalCriteria(with_visual_criteria=True, collision_constraint=True, with_spine=True)
    actual = get_variable_computer("straight", additional_criteria)
    assert actual == StraightAcrobaticsWithVisualVariablesWithSpine
