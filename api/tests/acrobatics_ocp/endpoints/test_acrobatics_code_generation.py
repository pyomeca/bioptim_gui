import json
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bioptim_gui_api.acrobatics_ocp.endpoints.acrobatics import router
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_config import (
    DefaultAcrobaticsConfig,
)
from bioptim_gui_api.acrobatics_ocp.misc.acrobatics_utils import phase_name_to_info
from bioptim_gui_api.acrobatics_ocp.misc.models import AdditionalCriteria

test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


@pytest.fixture(autouse=True)
def run_for_all():
    # before test: create file

    datafile = DefaultAcrobaticsConfig.datafile

    with open(datafile, "w") as f:
        base_data = DefaultAcrobaticsConfig.base_data
        json.dump(base_data, f)

    phase_names = ["Somersault 1", "Landing"]
    base_phases = [
        phase_name_to_info("straight", phase_names, i, AdditionalCriteria()) for i, _ in enumerate(phase_names)
    ]
    base_phases[0]["phase_name"] = "Somersault 1"
    base_phases[1]["phase_name"] = "Landing"

    base_data["phases_info"] = base_phases

    with open(datafile, "w") as f:
        json.dump(base_data, f)

    yield

    # after test : delete file
    import os

    os.remove(datafile)


def test_generate_code_no_model():
    response = client.post("/acrobatics/generate_code", json={"model_path": "", "save_path": "saver/cheh.py"})
    assert response.status_code == 400


@pytest.mark.parametrize("position", ["straight", "pike", "tuck"])
@pytest.mark.parametrize(
    ("with_visual_criteria", "non_collision", "with_spine", "folder"),
    [
        (True, True, False, "with_collision_and_visual"),
        (True, False, False, "with_visual"),
        (False, True, False, "with_collision"),
        (False, False, False, "vanilla"),
        (True, True, True, "everything"),
    ],
)
def test_generate_code_simple_position(position, with_visual_criteria, non_collision, with_spine, folder):
    # using base data and a position model (16 degrees of freedom)
    model_path = Path(f"test_biomods/{folder}/good/{position}.bioMod").absolute()
    response = client.put("/acrobatics/model_path", json={"model_path": str(model_path)})
    assert response.status_code == 200, response

    if with_visual_criteria:
        response = client.put("/acrobatics/with_visual_criteria", json={"with_visual_criteria": True})
        assert response.status_code == 200, response

    if non_collision:
        response = client.put("/acrobatics/collision_constraint", json={"collision_constraint": True})
        assert response.status_code == 200, response

    if with_spine:
        response = client.put("/acrobatics/with_spine", json={"with_spine": True})
        assert response.status_code == 200, response

    response = client.put("/acrobatics/position", json={"position": f"{position}"})
    assert response.status_code != 400, response

    with open(f"acrobatics_ocp/generated_examples/{position}/base_{position}.txt", "r") as f:
        base_position_content = f.read()

    response = client.post("/acrobatics/generate_code", json={"model_path": "", "save_path": "saver/cheh.py"})
    assert response.status_code == 200, response
    data = response.json()
    assert data["new_models"][0][1] == f"saver/{position}-{position}.bioMod"
    assert data["new_models"][0][1] in data["generated_code"]

    # data = response.json()
    #
    # # filter out the bio_model line, because of absolute path that may vary between devs
    # data = "\n".join([line for line in data.split("\n") if not line.startswith("    bio_model")])
    # base_position_content = "\n".join(
    #     [line for line in base_position_content.split("\n") if not line.startswith("    bio_model")]
    # )
    #
    # assert data == base_position_content


@pytest.mark.parametrize("position", ["straight", "pike", "tuck"])
@pytest.mark.parametrize(
    ("with_visual_criteria", "non_collision", "with_spine", "folder"),
    [
        (True, True, False, "with_collision_and_visual"),
        (True, False, False, "with_visual"),
        (False, True, False, "with_collision"),
        (False, False, False, "vanilla"),
        (True, True, True, "everything"),
    ],
)
def test_generate_code_position_no_objective_no_constraint(
    position, with_visual_criteria, non_collision, with_spine, folder
):
    # using base data and a position model (16 degrees of freedom)
    model_path = Path(f"test_biomods/{folder}/good/{position}.bioMod").absolute()
    response = client.put("/acrobatics/model_path", json={"model_path": str(model_path)})
    assert response.status_code == 200, response

    if with_visual_criteria:
        response = client.put("/acrobatics/with_visual_criteria", json={"with_visual_criteria": True})
        assert response.status_code == 200, response

    if non_collision:
        response = client.put("/acrobatics/collision_constraint", json={"collision_constraint": True})
        assert response.status_code == 200, response

    if with_spine:
        response = client.put("/acrobatics/with_spine", json={"with_spine": True})
        assert response.status_code == 200, response

    response = client.put("/acrobatics/position", json={"position": f"{position}"})
    assert response.status_code != 400, response

    client.delete("/acrobatics/phases_info/0/objectives/0")
    client.delete("/acrobatics/phases_info/0/objectives/0")

    with open(
        f"acrobatics_ocp/generated_examples/{position}/base_{position}_no_objectives_no_constraints.txt",
        "r",
    ) as f:
        base_position_content = f.read()

    response = client.post("/acrobatics/generate_code", json={"model_path": "", "save_path": "saver/cheh.py"})
    assert response.status_code == 200, response
    data = response.json()
    assert data["new_models"][0][1] == f"saver/{position}-{position}.bioMod"
    assert data["new_models"][0][1] in data["generated_code"]

    # data = response.json()
    #
    # # filter out the bio_model line, because of absolute path that may vary between devs
    # data = "\n".join([line for line in data.split("\n") if not line.startswith("    bio_model")])
    # base_position_content = "\n".join(
    #     [line for line in base_position_content.split("\n") if not line.startswith("    bio_model")]
    # )
    #
    # assert data == base_position_content


@pytest.mark.parametrize("position", ["straight", "pike", "tuck"])
@pytest.mark.parametrize(
    ("with_visual_criteria", "non_collision", "with_spine", "folder"),
    [
        (True, True, False, "with_collision_and_visual"),
        (True, False, False, "with_visual"),
        (False, True, False, "with_collision"),
        (False, False, False, "vanilla"),
        (True, True, True, "everything"),
    ],
)
def test_generate_code_position_objective_and_constraint(
    position, with_visual_criteria, non_collision, with_spine, folder
):
    # using base data and a position model (16 degrees of freedom)
    model_path = Path(f"test_biomods/{folder}/good/{position}.bioMod").absolute()
    client.put("/acrobatics/model_path", json={"model_path": str(model_path)})

    response = client.put("/acrobatics/position", json={"position": f"{position}"})
    assert response.status_code != 400, response

    if with_visual_criteria:
        response = client.put("/acrobatics/with_visual_criteria", json={"with_visual_criteria": True})
        assert response.status_code == 200, response

    if non_collision:
        response = client.put("/acrobatics/collision_constraint", json={"collision_constraint": True})
        assert response.status_code == 200, response

    if with_spine:
        response = client.put("/acrobatics/with_spine", json={"with_spine": True})
        assert response.status_code == 200, response

    client.post("/acrobatics/phases_info/0/constraints")
    client.post("/acrobatics/phases_info/0/constraints")

    with open(
        f"acrobatics_ocp/generated_examples/{position}/{position}_constraint_and_objective.txt",
        "r",
    ) as f:
        base_position_content = f.read()

    response = client.post("/acrobatics/generate_code", json={"model_path": "", "save_path": "saver/cheh.py"})
    assert response.status_code == 200, response
    data = response.json()
    assert data["new_models"][0][1] == f"saver/{position}-{position}.bioMod"
    assert data["new_models"][0][1] in data["generated_code"]

    # data = response.json()
    #
    # # filter out the bio_model line, because of absolute path that may vary between devs
    # data = "\n".join([line for line in data.split("\n") if not line.startswith("    bio_model")])
    # base_position_content = "\n".join(
    #     [line for line in base_position_content.split("\n") if not line.startswith("    bio_model")]
    # )
    #
    # assert data == base_position_content


@pytest.mark.parametrize("position", ["straight", "pike", "tuck"])
@pytest.mark.parametrize(
    ("with_visual_criteria", "non_collision", "with_spine", "folder"),
    [
        (True, True, False, "with_collision_and_visual"),
        (True, False, False, "with_visual"),
        (False, True, False, "with_collision"),
        (False, False, False, "vanilla"),
        (True, True, True, "everything"),
    ],
)
def test_generate_code_2_phase_position_objective_and_constraint(
    position, with_visual_criteria, non_collision, with_spine, folder
):
    # using base data and a position model (16 degrees of freedom)
    model_path = Path(f"test_biomods/{folder}/good/{position}.bioMod").absolute()
    client.put("/acrobatics/model_path", json={"model_path": str(model_path)})

    if with_visual_criteria:
        response = client.put("/acrobatics/with_visual_criteria", json={"with_visual_criteria": True})
        assert response.status_code == 200, response

    if non_collision:
        response = client.put("/acrobatics/collision_constraint", json={"collision_constraint": True})
        assert response.status_code == 200, response

    if with_spine:
        response = client.put("/acrobatics/with_spine", json={"with_spine": True})
        assert response.status_code == 200, response

    response = client.put("/acrobatics/position", json={"position": f"{position}"})
    assert response.status_code != 400, response

    client.put("/acrobatics/nb_somersaults", json={"nb_somersaults": 2})

    client.post("/acrobatics/phases_info/0/constraints")
    client.post("/acrobatics/phases_info/0/constraints")
    client.post("/acrobatics/phases_info/1/constraints")
    client.post("/acrobatics/phases_info/1/constraints")

    with open(
        f"acrobatics_ocp/generated_examples/{position}/{position}_two_phases_obj_constraints.txt",
        "r",
    ) as f:
        base_position_content = f.read()

    response = client.post("/acrobatics/generate_code", json={"model_path": "", "save_path": "saver/cheh.py"})
    assert response.status_code == 200, response
    data = response.json()
    assert data["new_models"][0][1] == f"saver/{position}-{position}.bioMod"
    assert data["new_models"][0][1] in data["generated_code"]

    # data = response.json()
    #
    # # filter out the bio_model line, because of absolute path that may vary between devs
    # data = "\n".join([line for line in data.split("\n") if not line.startswith("    bio_model")])
    # base_position_content = "\n".join(
    #     [line for line in base_position_content.split("\n") if not line.startswith("    bio_model")]
    # )
    #
    # assert data == base_position_content


@pytest.mark.parametrize("position", ["straight", "pike", "tuck"])
@pytest.mark.parametrize(
    ("with_visual_criteria", "non_collision", "with_spine", "folder"),
    [
        (True, True, False, "with_collision_and_visual"),
        (True, False, False, "with_visual"),
        (False, True, False, "with_collision"),
        (False, False, False, "vanilla"),
        (True, True, True, "everything"),
    ],
)
def test_generate_code_modified_objective_and_constraint(
    position, with_visual_criteria, non_collision, with_spine, folder
):
    # using base data and a position model (16 degrees of freedom)
    model_path = Path(f"test_biomods/{folder}/good/{position}.bioMod").absolute()
    client.put("/acrobatics/model_path", json={"model_path": str(model_path)})

    if with_visual_criteria:
        response = client.put("/acrobatics/with_visual_criteria", json={"with_visual_criteria": True})
        assert response.status_code == 200, response

    if non_collision:
        response = client.put("/acrobatics/collision_constraint", json={"collision_constraint": True})
        assert response.status_code == 200, response

    response = client.put("/acrobatics/position", json={"position": f"{position}"})
    assert response.status_code != 400, response

    client.post("/acrobatics/phases_info/0/constraints")
    response = client.put(
        "acrobatics/phases_info/0/constraints/0/quadratic",
        json={"quadratic": False},
    )
    assert response.status_code == 200

    response = client.put("acrobatics/phases_info/0/constraints/0/expand", json={"expand": False})
    assert response.status_code == 200
    response = client.put(
        "acrobatics/phases_info/0/constraints/0/multi_thread",
        json={"multi_thread": True},
    )
    assert response.status_code == 200
    response = client.put(
        "acrobatics/phases_info/0/constraints/0/derivative",
        json={"derivative": True},
    )
    assert response.status_code == 200
    response = client.put(
        "acrobatics/phases_info/0/constraints/0/target",
        json={"target": [5.5, 3.14]},
    )
    assert response.status_code == 200
    response = client.put(
        "acrobatics/phases_info/0/constraints/0/integration_rule",
        json={"integration_rule": "approximate_trapezoidal"},
    )
    assert response.status_code == 200

    response = client.put(
        "acrobatics/phases_info/0/objectives/0/quadratic",
        json={"quadratic": False},
    )
    assert response.status_code == 200
    response = client.put("acrobatics/phases_info/0/objectives/0/expand", json={"expand": False})
    assert response.status_code == 200
    response = client.put(
        "acrobatics/phases_info/0/objectives/0/multi_thread",
        json={"multi_thread": True},
    )
    assert response.status_code == 200
    response = client.put(
        "acrobatics/phases_info/0/objectives/0/derivative",
        json={"derivative": True},
    )
    assert response.status_code == 200
    response = client.put("acrobatics/phases_info/0/objectives/0/target", json={"target": [1.0, 0.0]})
    assert response.status_code == 200
    response = client.put(
        "acrobatics/phases_info/0/objectives/0/integration_rule",
        json={"integration_rule": "midpoint"},
    )
    assert response.status_code == 200

    with open(
        f"acrobatics_ocp/generated_examples/{position}/{position}_modified_objectives_constraints.txt",
        "r",
    ) as f:
        base_position_content = f.read()

    response = client.post("/acrobatics/generate_code", json={"model_path": "", "save_path": "saver/cheh.py"})
    assert response.status_code == 200, response
    data = response.json()
    assert data["new_models"][0][1] == f"saver/{position}-{position}.bioMod"
    assert data["new_models"][0][1] in data["generated_code"]

    # data = response.json()
    #
    # # filter out the bio_model line, because of absolute path that may vary between devs
    # data = "\n".join([line for line in data.split("\n") if not line.startswith("    bio_model")])
    # base_position_content = "\n".join(
    #     [line for line in base_position_content.split("\n") if not line.startswith("    bio_model")]
    # )
    #
    # assert data == base_position_content
