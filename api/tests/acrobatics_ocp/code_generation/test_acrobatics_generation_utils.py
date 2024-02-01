# tests used for refactor purposes (no logic changes) only
# to assure that the result if not modified by the refactor
# by testing it with the baseline, being the duplicate files in tests/acrobatics_ocp/misc/code_generation
# and tests/acrobatics_ocp/misc/acrobatics_generation_utils.py

import json

import pytest

from bioptim_gui_api.acrobatics_ocp.code_generation.acrobatics_generation_utils import generated_code
from tests.acrobatics_ocp.code_generation.acrobatics_generation_utils import generated_code as baseline_generated_code

config_examples_path = "acrobatics_ocp/config_examples"


@pytest.mark.parametrize("position", ["straight", "pike", "tuck"])
@pytest.mark.parametrize(
    "folder", ["with_collision_and_visual", "with_visual", "with_collision", "vanilla", "everything"]
)
@pytest.mark.parametrize("config", ["simple", "no_penalties", "penalties", "more_phases", "modified_penalties"])
def test_generated_code_stay_same(position, folder, config):
    config_file = f"{config_examples_path}/{config}/{folder}/{position}.json"

    with open(config_file, "r") as json_file:
        config_data = json.load(json_file)

    actual = generated_code(config_data, "test/model.bioMod")
    expected = baseline_generated_code(config_data, "test/model.bioMod")

    assert actual == expected
