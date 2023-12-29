import pytest

from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria
from bioptim_gui_api.acrobatics_ocp.variables.variable_compute import get_variable_computer
from bioptim_gui_api.acrobatics_ocp.variables.variable_computers.straight_with_visual_acrobatics_variables_with_spine import (
    StraightAcrobaticsWithVisualVariablesWithSpine,
)


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
